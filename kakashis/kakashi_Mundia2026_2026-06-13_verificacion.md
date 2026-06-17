# Kakashi — Mundia2026 — 2026-06-13 — verificacion

## Qué se hizo

### Verificación del sistema en producción

Sesión corta de verificación. El sistema llevaba ~1h28min corriendo bajo systemd cuando se abrió la sesión.

**Estado confirmado:**
- `mundia2026.service` — active (running) desde las 02:09 CEST
- 3 procesos ffmpeg activos para EEUU vs Paraguay (video + SER + W Radio)
- Carpeta `/mnt/khauron/mundial2026/2026-06-13_03h00_GrpD_Estados_Unidos_vs_Paraguay/` existente y creciendo

**Problema detectado y corregido — vídeo no reproducible mientras graba:**

VLC daba `moov atom not found` al intentar abrir `video.mp4` durante la grabación. Causa: el formato MP4 escribe el índice (moov atom) al final del proceso. El flag `-movflags +faststart` solo lo mueve al principio cuando ffmpeg cierra el fichero, no durante la escritura.

Fix aplicado en `scheduler.py`:
- `video.mp4` → `video.mkv` (MKV no necesita índice al inicio, reproducible mientras crece)
- Eliminado `-movflags +faststart` (flag específico de MP4, innecesario en MKV)

El fix **no afecta la grabación en curso** (el proceso ffmpeg ya está en memoria con el código anterior). Se activará en el próximo arranque del servicio.

**Decisión de uso:** David ve los partidos en directo desde la app de RTVE cuando puede. El sistema de grabación es el backup nocturno para los partidos que se pierde durmiendo.

**Estado al cerrar:**
- Grabación EEUU vs Paraguay en curso, ~618 MB de vídeo, ~49 min grabados
- Finaliza ~06:20 CEST
- 100 partidos más programados bajo systemd
- David se va a dormir

## Próximos pasos

1. Mañana por la mañana: abrir `video.mp4` de EEUU vs Paraguay con VLC y verificar que es reproducible (sí lo será — el moov se escribe al terminar)
2. Reiniciar el servicio en algún momento sin partido en curso para que aplique el cambio a MKV
3. Verificar que el siguiente partido graba en `.mkv` y es reproducible mientras graba
4. Radio Marca — pendiente de encontrar el stream con DevTools durante un partido real
5. Actualizar `partidos.json` con equipos reales en fase eliminatoria (a partir del 28/06)

## Conversación

**David:** carga el contexto

**Claude:** [cargó khauron_recientes n=15 + los 3 kakashis de la carpeta del 12 y 13/06]

**David:** podemos comprobar si se está grabando el partido? puedo comprobarlo yo viendolo y/ o escuchando la grabacion ? o tenemos que dejar el proceso tranquilo ?

**Claude:** Está grabando ahora mismo. Tres procesos ffmpeg activos para EEUU vs Paraguay. [mostró ls -lh: 487 MB de vídeo, 38 MB SER, 19 MB W Radio]

**David:** dame los comansdos para intalar coreectamente vlc

**Claude:** sudo apt install vlc -y [instalación completada] vlc /mnt/khauron/mundial2026/2026-06-13_03h00_GrpD_Estados_Unidos_vs_Paraguay/video.mp4

**David:** [output de VLC — moov atom not found, buffer deadlock prevented]

**Claude:** El problema es el moov atom not found — MP4 no es reproducible mientras graba. Fix: cambiar a MKV. Ahora mismo puedes escuchar el audio con vlc ser.mp3. [aplicó fix en scheduler.py: mp4→mkv, eliminó -movflags +faststart]

**David:** no me importa verlo ahora, prefiero guardarlo

**Claude:** Perfecto. No toques el servicio — mataría la grabación. El fix se activa en el próximo reinicio. Termina ~06:20 CEST.

**David:** porque lo que pueda ver directamente, lo vere desde mi app de rtve

**Claude:** Tiene sentido — el sistema es el backup nocturno, no el reproductor principal.

**David:** está todo ok? me puedo ir a dormir?

**Claude:** [verificó: active, 618 MB vídeo, 48 MB SER, 24 MB W Radio] Todo OK. Vete a dormir.

**David:** llama a kakashi
