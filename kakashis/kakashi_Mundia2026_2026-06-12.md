# Kakashi — Mundia2026 — 2026-06-12

## Qué se hizo

Se construyó desde cero el sistema completo de grabación anti-spoilers del Mundial 2026.

**Estado de partida:** Solo existía `partidos.json` con los 101 partidos del torneo (fase de grupos hasta final, con hora en España).

**Lo que se construyó:**

### Arquitectura
- `config/channels.yaml` — registro de canales con sus URLs y métodos
- `config/config.yaml` — configuración principal (directorios, buffers, calidad)
- `src/recorder.py` — motor de grabación: yt-dlp → ffmpeg o ffmpeg directo con duración exacta
- `src/scheduler.py` — lee partidos.json, programa `threading.Timer` para cada partido futuro
- `src/display.py` — CLI con rich (tablas, colores, sin spoilers)
- `src/config.py` — carga de YAML/JSON
- `main.py` — CLI con click: `daemon`, `hoy`, `siguiente N`, `grabar ID`, `test CANAL`, `canales`, `archivos`
- `arrancar.sh` / `m26.sh` — scripts de arranque

### Investigación técnica RTVE — hallazgo crítico
RTVE La 1 usa **FairPlay SAMPLE-AES** en el stream `la1_main_dvr_drm.m3u8` → irrompible sin clave DRM.

**Solución:** El IPTV community list (iptv-org/iptv) reveló la URL del stream sin DRM:
- `https://rtvelivestream.rtve.es/rtvesec/la1/la1_main.m3u8`
- H264 720p, AAC español 48kHz, 3.7 Mbps — reproducible directamente con ffmpeg
- Geo-restringida a España (funciona sin VPN desde casa de David)

### Tests exitosos
- `rtve_la1` — 8s → 3.5 MB `.ts` válido (H264 720p + AAC spa) ✓
- `cadena_ser` — 5s → 0.1 MB `.mp3` válido ✓

### Canales configurados
- **España TV:** `rtve_la1` (720p, funcional), `rtve_la2`
- **España radio:** `cadena_ser` (funcional), `rne_radio1`
- **México TV:** `canal_once`, `canal_22`, `azteca_deportes` (pendiente test, posible geo-bloqueo)
- **Argentina/Paraguay:** `tv_publica_ar`, `snt_paraguay` (pendiente test, requieren VPN)

### Venv propio en el proyecto
`/home/david/Portfolio/Mundia2026/venv/` con: `yt-dlp 2026.06.09`, `streamlink 8.4.0`, `click`, `rich`, `PyYAML`

## Próximos pasos

1. **Probar canales mexicanos** — `./m26.sh test canal_once --segundos 10` (verificar geo-bloqueo desde España)
2. **Arrancar el daemon** — `./arrancar.sh &` — programa automáticamente todos los 101 partidos restantes
3. **Primer partido en 4h51m** — partido #1: USA vs Paraguay a las 03:00 del 13/06
   - El daemon lo grabará si está corriendo; o manualmente: `./m26.sh grabar 1`
4. **España vs Cabo Verde** — partido #10, 15/06 a las 19:00 — añadir `cadena_ser` como segundo canal
   - Editar `partidos.json` añadiendo `"canales": ["rtve_la1", "cadena_ser"]` al partido #10
5. **Disco externo** — cuando se monte `/media/david/2q`, cambiar `directorio` en `config.yaml` para ahorrar espacio en el SSD
6. **Testear el archivo grabado** — reproducir `/home/david/Portfolio/Mundia2026/grabaciones/tests/20260612_TEST_vs_rtve_la1_rtve_la1.ts` con VLC para confirmar que es reproducible

### Comando para añadir canales a un partido específico en partidos.json:
El scheduler usa el campo `"canales": ["rtve_la1", "cadena_ser"]` si existe en el partido. Si no existe, usa `canales_por_defecto` del config.yaml.

## Conversación completa

**David:** Vale, quiero que empecemos este proyecto, hemos empezado a coger esta base de datos, porque como vivo en España y los horarios de los partidos de fútbol son muy complicados, lo que quiero hacer es poder ver todos los partidos, vale, sin embargo tengo que mantener mi ritmo de sueño. Y he pensado que si desde por la mañana soy capaz de no escuchar noticias, puedo ver los partidos incluso sin saber cómo han terminado, vale. Ahora necesito ayuda y un programa porque lo que creo que vamos a hacer es que por un lado voy a pensar en las, por ejemplo, una radio pública española, por ejemplo, la SER, que particularmente me gusta, y también de la COPPE para poder guardar las retrasmisiones en directo de todos los partidos del mundial. Y quiero de audio también, por si acaso, quiero dos o tres recomendaciones de audio en de, por ejemplo, de cadenas mexicanas, porque son sus presentadores tienen mucha cadidad, vale, todo de televisiones públicas, vale. Y a partir de ahí lo que quiero hacer es, porque por ejemplo en la radio, televisión española, pública, están poniendo algunos de los partidos. Y me gustaría poder grabarlos para mi uso personal en mi ordenador sin que eso vaya a ser compartido de ninguna manera, para que yo a la mañana siguiente pueda ver ese partido sin saber necesariamente cómo ha terminado, si no he visto nada, nada de prensa, vale. Como sé que hay otras páginas web que permiten la retrasmisión en directo de páginas públicas que permiten la distribución pública de contenido público, lo que quiero hacer es una búsqueda de qué canales puedo encontrar que sean públicos para hacer, para grabar en local, en mi disco duro local y sin ningún tipo de ánimo de lucro y solamente para poder ver. Yo, todo el mundial, en los canales públicos que lo retrasmiten, poder coger en varios de esas televisiones y que podamos guardar directamente en vídeo cuando eso se esté emitiendo, vale, de manera que puedo ver, pues, a lo mejor, en Francia emitirán los partidos de Francia, en Argentina emitirán los partidos de Argentina. En Estados Unidos no creo, pero en Paraguay, por ejemplo, seguro, en México también. Y todo eso es televisión pública, porque la televisión pública es un derecho que tenemos todos. Por lo tanto, ver si podemos hacer eso para poder ver yo tener todas las mañanas guardado en una carpeta en local el partido y el audio que quisiera poner para escuchar la retrasmisión de ese partido. Así que vamos a ver si trazamos un plan para poder hacer código para hacer todo esto.

**Khauron:** [Construyó el sistema completo — ver sección "Qué se hizo" arriba — tests exitosos de RTVE La 1 y Cadena SER, descubrimiento del stream sin DRM de RTVE]

---
*Estado al cerrar: sistema operativo. Primer partido en ~4h50m. Daemon no arrancado todavía.*
