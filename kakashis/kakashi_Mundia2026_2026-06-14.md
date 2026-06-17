# Kakashi — Mundia2026 — 2026-06-14

## Qué se hizo

### Estado al abrir sesión

Sistema corriendo bajo systemd desde el 13/06 a las 14:11 CEST. En el momento de abrir la sesión estaba grabando **Brasil vs Marruecos** (00:00 CEST, 14/06) con 4 procesos ffmpeg activos:
- `video.mkv` — Globo Brasil
- `video_tudn.mkv` — TUDN backup
- `ser.mp3` — Cadena SER
- `w_radio.mp3` — W Radio Colombia

Grabaciones anteriores completadas y verificadas por el log del sistema:
- EEUU vs Paraguay (13/06 03:00) — carpeta existente
- Qatar vs Suiza (13/06 21:00) — `✓ VIDEO OK (3163 MB)` + audios OK

### Reducción de duración — sources.yaml

Detectado que `duracion_min: 200` (3h20min) era excesivo para fase de grupos, donde no hay prórroga. Cambiado a `duracion_min: 120` (2h00min: 90 min de partido + 30 de margen para descuentos y pre/post).

Ahorro estimado: ~1.3 GB por partido solo en vídeo principal, más lo mismo en TUDN y audios.

El cambio **no afectó** a Brasil vs Marruecos (ffmpeg ya en memoria con -t 12000). Se aplica al siguiente partido.

### Git

```
commit 04dc060
sources.yaml: reducir duracion_min de 200 a 120 min para fase de grupos
```

`git push` completado → `e0e8d1c..04dc060 main -> main`

### Reinicio del servicio — pendiente

No se reinició porque Brasil vs Marruecos seguía grabando (los ffmpeg con -t 12000 terminan ~03:18 CEST). Haití vs Escocia arranca a las 03:00 — no hay ventana esta noche.

**Ventana para reiniciar:** mañana entre las 07:00 (termina Australia vs Turquía) y las 19:00 (empieza Alemania vs Curazao). 12 horas de margen.

## Próximos pasos

1. **Reiniciar el servicio** en ventana sin partido (mañana 07:00–19:00 CEST) para que aplique `duracion_min: 120`
2. **Verificar grabaciones** de Haití vs Escocia y Australia vs Turquía (primeros partidos con la nueva duración si el servicio se reinicia a tiempo)
3. **Buscar canales alternativos a TUDN** para partidos importantes sin fuente propia: Portugal, Noruega, Colombia, Croacia...
4. **Radio Marca** — stream pendiente de encontrar con DevTools durante un partido
5. **Fase eliminatoria** — actualizar `partidos.json` con equipos reales a partir del 28/06

## Conversación

**David:** carga el contexto

**Claude:** [cargó khauron_recientes n=15 + kakashis del 13/06]

**David:** mira si está grabando

**Claude:** mundia2026.service active (running) desde las 14:11 CEST. 4 ffmpeg activos para Brasil vs Marruecos. Qatar vs Suiza ya cerrado limpio: VIDEO OK 3163 MB + ambos audios OK. Brasil vs Marruecos: video.mkv 837 MB, video_tudn.mkv 868 MB, ser.mp3 52 MB, w_radio.mp3 26 MB. Lleva ~55 min grabados.

**David:** luego hay que pensar que todavía en esta fase solo hay noventa mimnutos mas el tiempo añadido, no? no se jueg a aú n próorogas

**Claude:** Exacto. sources.yaml tiene duracion_min: 200 para todos — 3h20min sin distinción. En grupos sobran 80 minutos. Lo correcto: 120 min para grupos, 200 para eliminatorias. ¿Lo ajusto?

**David:** solo estamos en fase de grupos, no hemos tocado códifo para ldespues, asique vamos a mejorar eso, para que tener video de mas

**Claude:** [cambió duracion_min de 200 a 120 en sources.yaml con comentario explicativo]

**David:** reinicia el servicio y haz git

**Claude:** Brasil vs Marruecos todavía grabando a la 01:03 CEST — si reinicio ahora mato los 4 ffmpeg. Hago el git, el reinicio lo dejamos para cuando terminen (~03:18 CEST). [commit 04dc060]

**David:** correcto, entonce haz slo git

**Claude:** Commit hecho. El reinicio cuando quieras — esta noche después de las 03:18 o mañana antes del siguiente partido.

**David:** y git push

**Claude:** [git push → e0e8d1c..04dc060 main -> main]

**David:** y

**Claude:** Brasil vs Marruecos todavía grabando. Haití vs Escocia arranca a las 02:58 CEST. No hay ventana para reiniciar esta noche — lo más seguro es mañana entre las 07:00 y las 19:00.

**David:** lisrto, cual es el partido que grba después?

**Claude:** Haití vs Escocia hoy a las 03:00 CEST, en menos de 2 horas.

**David:** recuerdeme los proximos partidos y horaRIOAS Y LOS QUE NO TENEMOS Y LKOS QUE SI TENEMOS PARA GRABAR ( tUDN NO ME DA NADA DECONDIANZA)

**Claude:** [listado completo — canales propios: Alemania 19:00, Japón 22:00, España mañana 19:00, Francia/Argentina/Inglaterra/Brasil/Marruecos según sus fechas. Todo lo demás TUDN]

**David:** nmada hicimos git push?

**Claude:** Sí, ya está hecho. e0e8d1c..04dc060 main -> main

**David:** llama a Kakahi
