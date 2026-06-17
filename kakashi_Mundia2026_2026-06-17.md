# Kakashi — Mundia2026 · 2026-06-17

## Qué se hizo

### CazéTV integrado como fallback final en el scheduler

- `scheduler.py` — nueva función `extraer_url_youtube(yt_url, nombre)`: llama `yt-dlp --geo-bypass-country BR` en el momento del partido (no en el arranque del daemon, porque el stream solo existe en vivo)
- `resolver_fuente()` acepta nuevo parámetro `cazetv=`; lo devuelve como último recurso si no hay ningún canal asignado
- `grabar_partido()` detecta URLs YouTube y resuelve la URL HLS real justo antes de lanzar ffmpeg
- `modo_lista()` muestra columna separada "CazéTV (yt-dlp)" para no confundirla con canales directos
- `sources.yaml` — añadida entrada `cazetv: https://www.youtube.com/@cazeTv/live`
- Cobertura resultante: **62 canales directos | 39 CazéTV (yt-dlp) | 0 sin fuente** (101/101)
- Commit: `bbbd711`

### Alarma automática para el test de CazéTV antes del partido

- Partido esta noche: **Portugal vs RD Congo, 19:00h**
- `cazetv_alarm.py` creado — prueba yt-dlp y envía resultado por Telegram + escritorio GTK
- Proceso en background lanzado (PID 1260010, `sleep 18947`) para dispararlo a las **18:55h**
- Confirmado que el sistema Telegram funciona: mensaje de prueba llegó correctamente

### Sistema de alarmas integrado en Khauron (feature nueva)

Motivación: David quería que el resultado de la alarma CazéTV llegara también a la app GTK de escritorio que ya tenía en Debian (`khauron-validar.service`).

**Archivos modificados/creados:**

`Khauron/indexador/storage.py`:
- `encolar_alarma(mensaje, cuando, canal, contexto)` — programa alarma con `pospuesta_hasta`; canal puede ser `'desktop'`, `'telegram'` o `'ambos'`
- `obtener_alarmas_vencidas()` — devuelve alarmas cuyo `pospuesta_hasta` ya pasó y no han sido notificadas
- `marcar_alarma_notificada(pid)` — pone `fecha_enviada` para evitar disparos dobles

`Khauron/mcp_server/server.py`:
- Nuevo tool `khauron_alarma` — acepta `mensaje`, `cuando` (HH:MM, +Xmin, +Xh, ISO), `canal`, `contexto`

`Khauron/desktop/khauron_alarma_watcher.py` (nuevo):
- Detecta alarmas vencidas, envía Telegram directo (urllib, sin dependencias extras) y reinicia `khauron-validar.service` para GTK

`~/.config/systemd/user/khauron-alarma-watcher.service` + `.timer`:
- Timer activo cada 5 min — habilitado con `systemctl --user enable --now`

`cazetv_alarm.py` actualizado para usar `encolar_pregunta` + watcher en vez de Telegram directo.

**Prueba de alarma realizada:** alarma de test programada para las 14:09h, a las 14:06h. Watcher la disparará en ≤5 min vía escritorio + Telegram.

### Sistema de preguntas del corpus

- Identificado el sistema completo: `poblar_queue_desde_corpus(n, canal)` → `preguntas_queue` → bot Telegram `/validar` o app GTK (`khauron-validar.service`)
- Canal `telegram`: solo proyectos personales / Khauron / ZeroCog
- Canal `desktop`: todos los proyectos no encapsulados
- Ejecutado `poblar_queue_desde_corpus(n=5, canal='telegram')` y `canal='desktop'` — añadidas 6 preguntas nuevas al corpus
- Total en cola tras la sesión: 10 Telegram, 4+ desktop

## Próximos pasos

1. **18:55h** — la alarma de background dispara `cazetv_alarm.py` → resultado llega por Telegram + GTK. Verificar que ambos canales funcionan con el nuevo watcher.
2. Verificar partido Portugal vs RD Congo (19:00h) grabado correctamente por el scheduler.
3. Reiniciar el servicio `mundia2026.service` si no se ha hecho: `sudo systemctl restart mundia2026.service`
4. Commit + push en Khauron (storage.py, server.py, watcher, systemd).
5. Tests para `encolar_alarma` y `khauron_alarma_watcher` (Protocolo Cancerbero pendiente).

## Conversación completa

**David:** [continuación de sesión anterior — contexto cargado desde resumen]

**Claude:** [implementa CazéTV en scheduler, función `extraer_url_youtube`, `resolver_fuente` con parámetro `cazetv`, `modo_lista` actualizado. Cobertura 101/101.]

**David:** y usa las herramientas de kahruon. Tengo un sistema de preguntas que me llegan al escritorio, usa eses sistema para ponerme una alarma y que veamos si salta el proceso y funciona

**Claude:** [busca sistema de alarma en Khauron. Encuentra `cazetv_alarm.py` con Telegram. Lanza proceso en background PID 1260010 para las 18:55h. Envía confirmación por `khauron_preguntar`.]

**David:** ssabes como mandarme la alarma? haz una prueba

**Claude:** [ejecuta `cazetv_alarm.py` en modo test — CazéTV no está en vivo (lógico, el partido es a las 19:00). Telegram sí llegó.]

**David:** me ha llegado la alarma por telegram. GEnial

**Claude:** [confirma sistema funcionando. Explica flujo completo.]

**David:** vale, ahora quiero que busques el sistema de kharuon para lanzame en el escritorio preguntas que no se han validado en el corpus y que encuentres ese sistema

**Claude:** [llama `khauron_pendientes` — 199 eventos con preguntas abiertas. Explora Khauron, encuentra `preguntas_queue`, `poblar_queue_desde_corpus`, app GTK `khauron_validar.py`, `khauron-validar.service`. Puebla ambas colas. Envía aviso por Telegram.]

**David:** pero no solo telegram. Usamos tambien nu app que me manda notificacinoes al escritorio en forma de app ne mi debain

**Claude:** [encuentra `desktop/khauron_validar.py` — app GTK3 con tarjetas Sí/No/Más tarde. Encuentra `khauron-validar.service` + timer cada 30 min. Puebla canal desktop, reinicia servicio.]

**David:** y vamos a asuarlo tambien para la alarma

**Claude:** [intenta integrar escritorio en `cazetv_alarm.py`. Error en firma `encolar_pregunta` (kwarg `ctx` vs `contexto`).]

**David:** no no, actuliza khauron para poder integrar alarmas

**Claude:** [diseña e implementa sistema de alarmas completo en Khauron: `encolar_alarma`, `obtener_alarmas_vencidas`, `marcar_alarma_notificada` en storage.py; tool `khauron_alarma` en server.py; `khauron_alarma_watcher.py`; systemd timer cada 5 min; actualiza `cazetv_alarm.py`. Timer activado. Alarma de test programada para 14:09h.]

**David:** en qu e carptet has guardado esto?

**Claude:** [lista los tres directorios: Khauron, systemd, Mundia2026]

**David:** ok, genial, llama akakashi
