# 2026 Por Mis Huevos

Grabador automático del Mundial 2026 desde televisiones públicas de todo el mundo.

---

## Por qué existe esto

El fútbol es cultura. El Mundial es el evento más visto del planeta. Y sin embargo, en 2026, ver un partido sin pagar se ha convertido en un acto de resistencia.

Las televisiones públicas — financiadas con impuestos de todos los ciudadanos — tienen la obligación de emitir eventos de interés general. Muchas lo hacen. RTVE en España. ARD en Alemania. Globo en Brasil. NHK en Japón. Qatar TV. SNT en Paraguay. Son emisoras públicas, de acceso libre, que retransmiten el Mundial porque es un derecho de sus ciudadanos verlo.

Este programa graba esas retransmisiones. Nada más.

No descarga contenido de pago. No rompe DRM. No distribuye nada. Graba lo mismo que captaría una antena apuntando a un satélite público, o que vería cualquier ciudadano abriendo su navegador. La única diferencia es que lo hace automáticamente, a las 3 de la mañana, para que puedas verlo a las 9 sin que nadie te haya destripado el resultado.

El derecho a ver el deporte de tu país sin pagar una suscripción existe. Este programa lo ejerce.

---

## Qué hace

- Lee el calendario completo del Mundial 2026 (101 partidos, grupos hasta final)
- Asigna a cada partido la televisión pública de uno de los equipos que juega
- Para partidos sin televisión pública accesible, usa TUDN México (derechos completos del torneo, señal abierta)
- Graba vídeo + audio de la Cadena SER + audio de W Radio Colombia en paralelo, todo en castellano
- Cada partido queda en su propia carpeta: `YYYY-MM-DD_HHhMM_GrpX_Local_vs_Visitante/`
- Arranca automáticamente como servicio systemd. Si el ordenador se reinicia, sigue grabando

---

## Canales públicos utilizados

| País | Canal | Idioma |
|------|-------|--------|
| España | RTVE La 1 | Castellano |
| Alemania | ARD Das Erste | Alemán |
| Brasil | Globo | Castellano (feed internacional) |
| Japón | NHK G | Japonés |
| Marruecos | Medi1 TV | Árabe |
| Qatar | Qatar Television | Árabe |
| Corea del Sur | Arirang TV | Inglés |
| Colombia / Ecuador | Señal Colombia (reemisor) | Castellano |
| Paraguay | SNT | Castellano |
| México (comodín) | TUDN | Castellano |

Audio en castellano para todos los partidos: **Cadena SER** + **W Radio Colombia**

---

## Requisitos

```bash
python3 -m venv venv
source venv/bin/activate
pip install pyyaml pytz
# ffmpeg instalado en el sistema
```

## Uso

```bash
python scheduler.py --lista     # ver qué partidos se grabarán y con qué canal
python scheduler.py             # arrancar el daemon
```

## Servicio systemd

```bash
sudo cp mundia2026.service /etc/systemd/system/
sudo systemctl enable --now mundia2026.service
```

---

*Uso personal. Sin ánimo de lucro. Sin distribución. La televisión pública es un derecho.*
