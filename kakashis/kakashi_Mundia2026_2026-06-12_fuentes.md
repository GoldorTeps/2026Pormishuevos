# Kakashi — Mundia2026 — 2026-06-12 — fuentes

## Qué se hizo

### Contexto de partida

Sesión abierta en `/home/david/Portfolio/Mundia2026/`. Existe ya un sistema construido en sesión anterior (ver `kakashi_Mundia2026_2026-06-12.md`): `main.py`, `src/scheduler.py`, `src/recorder.py`, `config/channels.yaml`, venv propio, tests exitosos de RTVE La 1 y SER.

Esta sesión se centró en investigación de fuentes adicionales y revisión de scope con protocolos Ananke y Cassandra.

### Audio de Telegram procesado

El bot de Khauron transcribió un audio enviado a las 21:49 (voz_20260612_215312.ogg). Transcripción:

> "Quiero poder ver todos los partidos sin saber cómo han terminado, manteniendo mi ritmo de sueño. Grabar retransmisiones de canales públicos — SER, COPE, cadenas mexicanas. RTVE emite algunos. Quiero tener cada mañana en local el partido en vídeo y el audio. Traza un plan y escribe el código."

### Estado de servicios Khauron al abrir sesión

- `khauron.service` — ✅ running desde las 15:25
- `khauron-bot.service` — ✅ running desde las 14:50, procesó el audio correctamente
- `khauron-brief.timer` — ✅ waiting, dispara mañana 13/06 a las 10:00
- Ollama + qwen2.5:7b — ✅ respondiendo
- MCP server Khauron — ❌ desconectado en esta sesión (khauron_buscar no disponible)

### Protocolo Ananke — scope declarado

Primera invocación de Ananke en el proyecto. Dictamen:
- Necesario: calendario ✅, fuente de stream, grabador autónomo, aislamiento spoilers, espacio en disco
- Espacio: `/mnt/khauron/` — 855 GB libres. David ve y borra, no es problema.
- Duración grabación: 200 minutos (cubre prórroga + penaltis + margen)

### Investigación de fuentes — mapa completo verificado

Todos los streams verificados con `curl -I` (HTTP 200) y algunos con `ffprobe`:

**Europa:**
| Canal | URL | Calidad |
|-------|-----|---------|
| La 1 RTVE (España) | `rtvelivestream.rtve.es/rtvesec/la1/la1_main_dvr.m3u8` | H.264 720p verificado |
| ARD (Alemania) | `daserste-live.ard-mcdn.de/daserste/live/hls/int/master.m3u8` | ✅ |
| Medi1 TV (Marruecos) | `easybroadcast.io — 83_medi1tv-arabic_g90v4ec/playlist_dvr.m3u8` | ✅ DVR |

**Asia:**
| Canal | URL | Calidad |
|-------|-----|---------|
| NHK G (Japón doméstico) | `nhk4.mov3.co/hls/nhk.m3u8` | H.264 960x540 ✅ |
| NHK World (Japón internacional) | `media-tyo.hls.nhkworld.jp/hls/w/live/master.m3u8` | ✅ |
| KBS2 (Corea doméstico) | `code.vthanhtivi.pw/getlink/kbs/12/playlist.m3u8` | ✅ (reemisor no oficial) |
| Arirang TV (Corea, EN) | `amdlive-ch01-g-ctnd-com.akamaized.net/arirang_1gch/...` | ✅ cultural/noticias |

**Árabe:**
| Canal | URL | Nota |
|-------|-----|------|
| Al Jazeera AR | `live-hls-web-aja.getaj.net/AJA/index.m3u8` | ✅ — sin derechos del Mundial |
| Al Arabiya | `live.alarabiya.net/alarabiapublish/alarabiya.smil/playlist.m3u8` | ✅ — sin derechos |
| Al Jazeera EN | `live-hls-web-aje-gcp.thehlive.com/AJE/index.m3u8` | ✅ |

**LATAM:**
| Canal | URL | Nota |
|-------|-----|------|
| Señal Colombia | `streaming.rtvc.gov.co/TV_Senal_Colombia_live/...` | ✅ |
| Globo Brasil | `59d39900ebfb8.streamlock.net/globo-720p/...` | ✅ |

**Advertencias:**
- NHK G y KBS2 son reemisores no oficiales — pueden caer a las 3am
- beIN Sports tiene derechos exclusivos en el mundo árabe — pago, sin M3U8 público
- Al Jazeera y Al Arabiya cubren noticias, no los partidos en sí

### Cassandra — dos rondas

**Primera ronda:** RTVE solo emite ~20 partidos. Streams DVR no son VOD. No hay scheduler. No hay código.

**Segunda ronda:** 35 partidos cubribles vs 66 pérdida asumida. Partidos eliminatorios sin fuente (equipos desconocidos hasta que se jueguen — problema de fase 2).

### Decisiones tomadas (Cassandra)

1. Sin fuente → pérdida asumida. No se graba.
2. Duración → 200 minutos fijos. Detección de fin de emisión: fase 2.
3. Partidos simultáneos → pendiente de fase 2.

### Archivos creados en esta sesión

**Nota:** Estos archivos pueden solaparse con `config/channels.yaml` y `src/scheduler.py` del sistema ya construido. Revisar integración en próxima sesión.

- `sources.yaml` — mapa equipo → URL (14 selecciones)
- `scheduler.py` (raíz) — daemon Python minimalista con threading

Daemon arrancado en `tmux session: mundia2026`. Primer partido grabable: Brasil vs Marruecos, sábado 13/06 a las 23:58 CEST.

## Próximos pasos

1. **Integrar fuentes nuevas** en `config/channels.yaml` del sistema ya construido (NHK G, KBS2, ARD, Señal Colombia, Medi1 TV) — no duplicar con `sources.yaml`
2. **Verificar stream de México** — placeholder en sources.yaml, URL sin confirmar
3. **FranceTV M3U8 directo** — pendiente (yt-dlp tiene extractor nativo)
4. **TV Pública Argentina** — pendiente
5. **Actualizar partidos.json** con equipos reales en fase eliminatoria a medida que avanza el torneo
6. **Fase 2:** gestión de partidos simultáneos (junio 24-27)
7. **Revisar si el daemon en tmux solapa** con el sistema ya construido — posible conflicto entre `scheduler.py` raíz y `src/scheduler.py`

## Conversación

**David:** vivo en españa. Quiero que calcules los horarios de todos los partidos del mundial de 2026 desde hoy, dia 12 de junio a las 21.30 en adelante. Vamos a empezar a trababajar sobre esos datos.

**Claude:** [buscó ESPN y fuentes españolas, calculó ET→CEST, generó partidos.json con 101 partidos]

**David:** venga ya, que en cualquier calendario de una pagina de españa de deportes tiene que estr

**Claude:** [intentó Marca, AS, Mundo Deportivo — bloqueados. Usó ESPN directamente]

**David:** escucha el audio que te he enviado por telegram

**Claude:** No tengo acceso a Telegram. Necesito la ruta del fichero en local.

**David:** no no, mira en Kharuron las herramientas que tienes y carga los ultimos kakashis de la karpeta de Khauron. Te he enviado un audio, quiero que lo analices

**Claude:** [cargó kakashis de Khauron del 12/06, encontró audio transcrito en el log del bot de systemd y en personal/telegram_2026-06-12.md]

**David:** mira el estado del servicio y mira el audio que te he enviado por telegram

**Claude:** [diagnóstico completo de servicios. Bot running, procesó el audio a las 21:53. MCP server desconectado en esta sesión]

**David:** dame un segundo. Antes de seguir confirmames que todos los rpoceos de khauron están oiperativos. Mira en el corpus, esta es una pregunta sencvilla pero importante, te pido que busque en un monenmento dado en el korpues de Khauron para una respuesta que en mi opino es importante que sea, como minimo correcta

**Claude:** khauron.service ✅, khauron-bot.service ✅, khauron-brief.timer ✅, Ollama ✅. MCP server desconectado — khauron_buscar no disponible. Para relanzar: reiniciar Claude Code.

**David:** quiero que convoque a Ananke. Usa el contexto de claude para activar este protocolo

**Claude:** [invocó Ananke — dictamen de necesidades: calendario, fuente, grabador autónomo nocturno, spoilers, disco]

**David:**  - Multi-fuente simultánea (graba una, no cinco)
de acuerdo, la que sea mas facil. /mnt/khauron/ ahí entraría

**Claude:** [verificó /mnt/khauron/: 855 GB. yt-dlp y ffmpeg instalados. Propuso arquitectura]

**David:** busca cual es la fuente mas facil para yt-dlp

**Claude:** [encontró RTVE La 1 M3U8 público, verificó con ffprobe: H.264 vivo]

**David:** no. Convoca a Cassandra

**Claude:** [Cassandra: RTVE solo 20 partidos, no hay scheduler, no hay código]

**David:** como podmeos ampliar los otros programas? dándome de alta como usuario? radiocaracol o cosas así? tieen que haber canales suficientes para poder cubrir muchos mas parridosl

**Claude:** [investigó LATAM y Europa: ARD, FranceTV, Globo, Señal Colombia, TUDN/Azteca YouTube]

**David:** mmmmm me gusta. CReo que has pecado de blanquitud y no has mirado televisones árabes o asíaticas. Corea y japon me gustan especialmente

**Claude:** [buscó Asia y mundo árabe: NHK World, Arirang, Al Jazeera, Al Arabiya, Medi1 TV]

**David:** mirame los dometicos de ellos, si,

**Claude:** [NHK G doméstico: H.264 960x540 ✅. KBS2 doméstico: ✅. Advertencia: reemisores no oficiales]

**David:** llama a Cassandra

**Claude:** [Cassandra: mapa fuente-partido no existe, 25 sin canal, NHK G/KBS2 pueden caer, simultáneos ignorados, duración sin definir, cero código]

**David:**  1. ¿Qué grabamos cuando no hay canal asignado — grabamos RTVE de fondo o dejamos vacío?
asumimos la perdida de 25 partidos.   2. ¿Cuánto tiempo graba cada partido — 150 min fijos o detección de fin de emisión?
si podemos detectar el fin de emision, el fin, pero podemos ir por fases, por lo que preocupemosnos de esta fase 1, ya verremos el resto.   3. ¿Partidos simultáneos — grabamos todos en paralelo o priorizamos?
cuando llegue ese puiesnte ya tendremos experiencia suficinte para valorar correctamente

**Claude:** [escribió sources.yaml y scheduler.py, probó --lista: 35 con fuente, 66 pérdida. Daemon en tmux]

**David:** llama a Cassandra

**Claude:** [Cassandra segunda ronda: eliminatorios todos sin fuente por equipos desconocidos. Problema de fase 2. 35 partidos de grupos cubribles]

**David:** no no, Brasil Marruecos es MAÑANA

**Claude:** Correcto — 14/06 a las 00:00 es la madrugada del sábado al domingo. Daemon durmiendo en tmux hasta las 23:58 del sábado.

**David:** no no , que se ha hecho?

**Claude:** [resumen: partidos.json, sources.yaml, scheduler.py, daemon en tmux, 35 partidos programados]

**David:** podemos guardar el tiepo que queramos porque veo los partidos y los voy borrando del disco. El espacio no es un problema

**Claude:** [cambió duracion_min a 200 en sources.yaml, relanzó daemon]

**David:** escribe el kakashi
