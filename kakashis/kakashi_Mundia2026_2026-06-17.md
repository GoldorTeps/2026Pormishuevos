# Kakashi — Mundia2026 — 2026-06-17

## Qué se hizo

### Cobertura: 42/101 → 62/101 (+20 partidos en una sesión)

**Canales nuevos confirmados con captura de frame:**

| País | Canal | URL | Nota |
|------|-------|-----|------|
| Qatar | Al Kass 1 | liveeu-gcp.alkassdigital.net | Plató Copa 2026 en pantalla |
| Irán | IRIB Varzesh | ncdn.telewebion.ir | Anuncio deportivo, activo |
| Uzbekistán | Cinerama Sport | stream8.cinerama.uz | "СМОТРИ ЧЕМПИОНАТ МИРА 2026" |
| Chequia | ČT Sport HD | 88.212.15.19 | Logo + softball CUB vs CZE |
| Colombia | Caracol TV | 138.121.15.230:9002 | Teleshopping colombiano |
| Costa de Marfil | RTI 1 (upgrade A+ Ivoire) | 69.64.57.208/rti1 | Logo "RTI 1" + programa nacional |
| Ghana | GTV | 69.64.57.208/gtv | Números Ghana en pantalla |
| RD Congo | RTNC | 69.64.57.208/rtnc | Logo "RTNC \| RDC" |
| Honduras | Canal 5 Televicentro | mdstrm.com | [Not 24/7] |
| Jamaica | TVJ | vod2live.univtec.com | [Not 24/7] |
| Haití | Tele Caraïbes | bozztv.com | [Not 24/7] |
| Irak | Al Iraqiya Sport | imn-live.esite-lab.com | TROFEO Copa 2026 + ticker "Iraq vs Escocia en Boston" |
| Jordania | Jordan Sport | 93.184.10.248 | Fútbol en directo, 12:33 UTC+3 |
| Bélgica | RTL-TVI | tvi-live-hls.akamaized.net | Logo RTL + timestamp vivo |

**Descubrimientos clave:**
- Proxy 69.64.57.208 (ya conocido por France 2 y RTS1 Senegal) tiene 5 canales africanos Copa: Francia, Senegal, Costa de Marfil (RTI1), Ghana (GTV), RD Congo (RTNC)
- Proxy 45.170.130.224:8000 tiene 20+ slots activos — escaneados todos, solo entretenimiento/deportes genéricos, nada Copa nuevo
- SSC/KSA Sport cerró octubre 2025 → Arabia Saudí sin canal viable
- Telemundo/NBC Universo USA: HTTP 200 pero DVR offset 6 horas → inútil para en vivo

### Decisiones tomadas
- Venezuela y Bolivia no clasificaron para Copa 2026 → canales encontrados NO añadidos al scheduler (equipos no aparecen en partidos.json)
- RTI 1 reemplaza A+ Ivoire para Costa de Marfil (TV pública = más partidos Copa)
- Estrategia Not 24/7: Honduras, Jamaica, Haití añadidos aunque offline ahora — se activarán durante el partido (mejor que sin fuente)

## Próximos pasos

1. **Reiniciar servicio**: `sudo systemctl restart mundia2026.service` para aplicar los nuevos canales
2. **Parrilla Al Kass 1**: Al Kass emite toda la Copa — investigar si puede cubrir partidos MENA sin canal (Argelia, Egipto, Arabia Saudí) como `canal_url` override en partidos.json
3. **Parrillas reales**: Verificar qué partidos cubre RTL-TVI Bélgica, Al Iraqiya Sport Irak, GTV Ghana, RTNC Congo exactamente para decidir si añadir como equipo o solo como override específico
4. **Techo actual**: Austria, Países Bajos, Escocia, Inglaterra, Noruega, Suecia, Suiza, Croacia, Corea del Sur, Australia, NZ, Sudáfrica, Argelia, Egipto, Canadá, EEUU, Panamá, Costa Rica → todos geo-bloqueados o OTT-only sin URL pública. Sin VPN no hay avance.

## Conversación

**David:** carga el contexto

**Claude:** [Continuando desde sesión anterior. KBS World y SRF Suiza bloqueados. Sigo con país por país. 5 nuevos canales comprometidos, cobertura 54/101. Commit c7d2a13.]

---

**David:** [sin mensaje — continuación automática]

**Claude:** Sigo con Costa Rica, Egipto, RD Congo. RTNC Congo en el mismo proxy 69.64.57.208. Frame: logo "RTNC | RDC", presentadora en vivo. También GTV Ghana (números Ghanianos), RTI 1 Costa de Marfil (logo RTI 1). Commit 293db57. Cobertura 57/101.

Luego escaneé los 20 slots activos del proxy latinoamericano (a010-a050):
- a010 TCM, a011 Cartoon Network, a012 TNT, a014 posible Bolivia, a015 Enlace, a016 RTVE TVE, a017 BabyFirst, a018 Lifetime, a019 USA Network
- a022 A&E, a024 TLC, a025 VX Venezuela (CADENA NACIONAL), a027 ESPN7, a028 ESPN6, a029 Universal, a032 Canal digital, a033 Canal 9 Paraguay, a034 ESPN, a035 NPY Paraguay, a036 Canal 31.1

Venezuela y Bolivia no están en Copa → descartados aunque el canal existe.

Probé Telemundo USA (HTTP 200 pero DVR 6h offset → descartado). HRT Croacia nueva URL → 404.

Añadí Honduras Canal 5, Jamaica TVJ, Haití Tele Caraïbes como Not 24/7. Commit 293db57.

Irán a por Iraq y Jordania: Al Iraqiya Sport devolvió frame con TROFEO Copa 2026. Jordan Sport: fútbol en directo. Commit 753b6ae. Cobertura 60/101.

RTL-TVI Bélgica en Akamaized.net: frame logo RTL + timestamp 11:38. Commit 484de10. Cobertura 62/101.

Arabia Saudí: SSC Sport cerró oct 2025, derechos a MBC Group, MBC Shahid bloqueado desde España. Sin solución.

Noruega, Suecia, Austria, Suiza, Croacia, Países Bajos, Inglaterra, Escocia, Canadá, Australia, NZ, Sudáfrica, Argelia, Egipto, Corea del Sur, Panamá, Costa Rica → todos bloqueados o sin URL directa.
