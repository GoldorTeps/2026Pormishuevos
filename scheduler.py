#!/usr/bin/env python3
"""
Mundia2026 — scheduler de grabaciones
Lee partidos.json + sources.yaml y lanza ffmpeg a la hora exacta de cada partido.

Uso:
    python scheduler.py           # arranca el daemon, graba todo lo que queda
    python scheduler.py --lista   # muestra qué partidos tienen fuente y cuáles no
"""
import json
import yaml
import subprocess
import unicodedata
import os
import re
import sys
import threading
import time
import logging
from datetime import datetime
import pytz

SPAIN_TZ = pytz.timezone('Europe/Madrid')
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))


def _setup_log():
    log_path = os.path.join(BASE_DIR, 'mundia.log')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s  %(levelname)-8s  %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger(__name__)


PIDFILE = os.path.join(BASE_DIR, 'mundia.pid')
YTDLP   = os.path.join(BASE_DIR, 'venv/bin/yt-dlp')
log = logging.getLogger(__name__)


# ── Carga ─────────────────────────────────────────────────────────────────────

def cargar():
    with open(os.path.join(BASE_DIR, 'sources.yaml')) as f:
        cfg = yaml.safe_load(f)
    with open(os.path.join(BASE_DIR, 'partidos.json')) as f:
        partidos = json.load(f)
    return cfg, partidos


# ── Resolución de fuente ───────────────────────────────────────────────────────

def resolver_fuente(partido, canales, comodin=None):
    # Override por partido tiene máxima prioridad (RTVE, ARD específico, etc.)
    if partido.get('canal_url'):
        return partido['canal_url'], partido.get('canal_nombre', 'override')
    for equipo in [partido.get('local', ''), partido.get('visitante', '')]:
        if equipo in canales:
            return canales[equipo], equipo
    if comodin:
        return comodin, 'TUDN'
    return None, None


# ── Nomenclatura ───────────────────────────────────────────────────────────────

def slug(s):
    """Convierte cualquier texto Unicode a ASCII seguro para nombre de fichero."""
    # Descomponer caracteres acentuados y quedarse con la base ASCII
    s = unicodedata.normalize('NFKD', s)
    s = s.encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[^\w]', '_', s)[:20].strip('_')


def nombre_carpeta(partido):
    fecha = partido['fecha_es']
    hora  = partido['hora_es'].replace(':', 'h')
    local = slug(partido['local'])
    vis   = slug(partido['visitante'])
    grupo = partido.get('grupo') or partido.get('fase', 'KO')[:4]
    return f"{fecha}_{hora}_Grp{grupo}_{local}_vs_{vis}"


# ── Comprobación de grabación existente ───────────────────────────────────────

def _duracion_fichero(ruta):
    """Devuelve la duración en segundos del fichero, o 0 si no existe o falla."""
    if not os.path.exists(ruta):
        return 0
    try:
        out = subprocess.check_output(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', ruta],
            stderr=subprocess.DEVNULL,
        )
        return float(out.strip())
    except Exception:
        return 0


def _ya_grabado(ruta, duracion_min):
    """True si el fichero existe y tiene al menos el 90% de la duración esperada."""
    dur = _duracion_fichero(ruta)
    return dur >= duracion_min * 60 * 0.9


# ── yt-dlp: obtener URL de stream en vivo ─────────────────────────────────────

def _ytdlp_get_url(url_canal):
    """Devuelve la URL M3U8 del stream en vivo, o None si el canal está offline."""
    try:
        out = subprocess.run(
            [YTDLP, '--get-url', '-f', 'best[height<=720]/best', url_canal],
            capture_output=True, text=True, timeout=30,
        )
        if out.returncode == 0:
            return out.stdout.strip().split('\n')[0]
    except Exception:
        pass
    return None


# ── Grabación con ffmpeg ───────────────────────────────────────────────────────

def _ffmpeg_grabar(url, ruta, duracion_seg, log_ruta, extra_flags=None):
    cmd = ['ffmpeg', '-y', '-i', url, '-t', str(duracion_seg), '-c', 'copy']
    if extra_flags:
        cmd += extra_flags
    cmd.append(ruta)
    with open(log_ruta, 'w') as lf:
        return subprocess.run(cmd, stdout=lf, stderr=lf)


def grabar_partido(partido, url, cfg):
    duracion_min   = cfg['duracion_min']
    duracion_seg   = duracion_min * 60
    antelacion_seg = cfg['antelacion_min'] * 60
    destino_base   = cfg['destino']
    canales_audio  = cfg.get('audio', {})
    comodin        = cfg.get('comodin')

    fecha    = partido['fecha_es']
    hora     = partido['hora_es']
    dt_naive = datetime.strptime(f"{fecha} {hora}", '%Y-%m-%d %H:%M')
    dt_es    = SPAIN_TZ.localize(dt_naive)
    ts_inicio = dt_es.timestamp() - antelacion_seg

    carpeta     = nombre_carpeta(partido)
    dir_partido = os.path.join(destino_base, carpeta)
    ruta_video  = os.path.join(dir_partido, 'video.mkv')

    ahora  = time.time()
    espera = ts_inicio - ahora

    # Partido ya terminado hace más de duracion_min → skip
    if espera < -duracion_seg:
        log.debug(f"SKIP (finalizado): {carpeta}")
        return

    # Vídeo ya grabado con duración suficiente → skip
    if _ya_grabado(ruta_video, duracion_min):
        log.info(f"YA EXISTE — omitiendo: {carpeta}")
        return

    if espera > 0:
        log.info(f"PROGRAMADO en {espera/3600:.1f}h → {carpeta}")
        time.sleep(espera)

    os.makedirs(dir_partido, exist_ok=True)
    log.info(f"▶ INICIO: {carpeta}")

    hilos = []

    # Vídeo principal (canal de país)
    hilos.append(threading.Thread(
        target=_ffmpeg_grabar,
        args=(url, ruta_video, duracion_seg,
              os.path.join(dir_partido, 'video.log'), None),
        daemon=True,
        name=f"{carpeta}-video",
    ))

    # Backup CazéTV vía yt-dlp (si está en vivo) o TUDN si no lo está
    comodin_ytdlp = cfg.get('comodin_ytdlp')
    ruta_caze     = os.path.join(dir_partido, 'video_caze.mkv')
    if not _ya_grabado(ruta_caze, duracion_min):
        url_caze = None
        if comodin_ytdlp:
            log.info(f"  Intentando CazéTV ({comodin_ytdlp})…")
            url_caze = _ytdlp_get_url(comodin_ytdlp)
            if url_caze:
                log.info(f"  CazéTV en vivo ✓")
            else:
                log.info(f"  CazéTV offline — usando TUDN como backup")
        backup_url = url_caze or (comodin if comodin and url != comodin else None)
        backup_nombre = 'caze' if url_caze else 'tudn'
        if backup_url and backup_url != url:
            hilos.append(threading.Thread(
                target=_ffmpeg_grabar,
                args=(backup_url, ruta_caze, duracion_seg,
                      os.path.join(dir_partido, f'video_{backup_nombre}.log'), None),
                daemon=True,
                name=f"{carpeta}-backup",
            ))

    # Audios en paralelo
    for nombre_radio, url_audio in canales_audio.items():
        ruta_audio = os.path.join(dir_partido, f"{nombre_radio}.mp3")
        if _ya_grabado(ruta_audio, duracion_min):
            log.info(f"  Audio ya existe — omitiendo: {nombre_radio}")
            continue
        hilos.append(threading.Thread(
            target=_ffmpeg_grabar,
            args=(url_audio, ruta_audio, duracion_seg,
                  os.path.join(dir_partido, f"{nombre_radio}.log"), None),
            daemon=True,
            name=f"{carpeta}-{nombre_radio}",
        ))

    for t in hilos:
        t.start()
    for t in hilos:
        t.join()

    # Verificar resultados
    if _ya_grabado(ruta_video, duracion_min):
        size_mb = os.path.getsize(ruta_video) / 1_048_576
        log.info(f"✓ VIDEO OK ({size_mb:.0f} MB): {carpeta}")
    else:
        log.error(f"✗ VIDEO FALLO: {carpeta} — ver {dir_partido}/video.log")

    if _ya_grabado(ruta_caze, duracion_min):
        size_mb = os.path.getsize(ruta_caze) / 1_048_576
        log.info(f"✓ VIDEO BACKUP OK ({size_mb:.0f} MB): {carpeta}")
    elif os.path.exists(ruta_caze):
        log.error(f"✗ VIDEO BACKUP FALLO: {carpeta} — ver {dir_partido}/video_*.log")

    for nombre_radio in canales_audio:
        ruta_audio = os.path.join(dir_partido, f"{nombre_radio}.mp3")
        if _ya_grabado(ruta_audio, duracion_min):
            size_mb = os.path.getsize(ruta_audio) / 1_048_576
            log.info(f"✓ AUDIO {nombre_radio} OK ({size_mb:.0f} MB): {carpeta}")
        else:
            log.error(f"✗ AUDIO {nombre_radio} FALLO: {carpeta} — ver {dir_partido}/{nombre_radio}.log")


# ── Modo lista ─────────────────────────────────────────────────────────────────

def modo_lista(partidos, canales, comodin=None):
    print(f"\n{'FECHA':<12} {'HORA':<6} {'LOCAL':<22} {'VISITANTE':<22} {'CANAL'}")
    print("─" * 90)
    con_fuente = sin_fuente = 0
    for p in partidos:
        url, canal = resolver_fuente(p, canales, comodin)
        local = p['local'][:20]
        vis   = p['visitante'][:20]
        if url:
            print(f"{p['fecha_es']:<12} {p['hora_es']:<6} {local:<22} {vis:<22} {canal}")
            con_fuente += 1
        else:
            print(f"{p['fecha_es']:<12} {p['hora_es']:<6} {local:<22} {vis:<22} — sin fuente")
            sin_fuente += 1
    print(f"\nCon fuente: {con_fuente}  |  Sin fuente (pérdida asumida): {sin_fuente}\n")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    cfg, partidos = cargar()
    canales = cfg['canales']
    comodin = cfg.get('comodin')

    global log
    log = _setup_log()

    if '--lista' in sys.argv:
        modo_lista(partidos, canales, comodin)
        return

    # Instancia única — abortar si ya hay un scheduler corriendo
    if os.path.exists(PIDFILE):
        try:
            pid = int(open(PIDFILE).read().strip())
            os.kill(pid, 0)  # lanza OSError si el proceso no existe
            print(f"ERROR: ya hay un scheduler corriendo (PID {pid}). Abortando.")
            sys.exit(1)
        except (OSError, ValueError):
            pass  # proceso muerto — el pidfile es huérfano, continuar

    with open(PIDFILE, 'w') as f:
        f.write(str(os.getpid()))

    import atexit
    atexit.register(lambda: os.path.exists(PIDFILE) and os.remove(PIDFILE))

    os.makedirs(cfg['destino'], exist_ok=True)

    hilos = []
    programados = perdidos = 0

    for p in partidos:
        url, canal = resolver_fuente(p, canales, comodin)
        if url is None:
            perdidos += 1
            continue
        programados += 1
        t = threading.Thread(
            target=grabar_partido,
            args=(p, url, cfg),
            daemon=False,
            name=f"partido-{p['id']}",
        )
        t.start()
        hilos.append(t)

    log.info(f"Daemon arrancado — programados: {programados} | pérdida asumida: {perdidos}")

    for t in hilos:
        t.join()

    log.info("Todos los partidos procesados. Daemon terminado.")


if __name__ == '__main__':
    main()
