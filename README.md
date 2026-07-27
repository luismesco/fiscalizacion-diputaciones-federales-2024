# Observaciones de fiscalización del PEF 2023–2024

Reporte analítico sobre la fiscalización federal de precampaña y campaña para
Presidencia, senadurías y diputaciones. Responde, con fuentes primarias del INE
y del TEPJF:

1. qué partido acumuló más bloques únicos de observación;
2. cuál de esos casos trascendió a expedientes jurisdiccionales;
3. qué cadena terminó en sanciones confirmadas;
4. cómo fueron designadas las autoridades que intervinieron y qué respaldo
   partidista puede probarse con fuentes oficiales.

## Resultados centrales

- **A:** Movimiento Ciudadano, con 316 observaciones comprobadas.
- **B:** Movimiento Ciudadano, en `SUP-RAP-342/2024` y
  `SUP-RAP-400/2024`.
- **C:** Movimiento Ciudadano: 30 conclusiones sancionatorias confirmadas y
  seis revocadas para nueva valoración por la Sala Superior.
- **Designaciones:** no se verificó que el conjunto de autoridades
  intervinientes fuera designado por PAN, PRI, PRD o Nueva Alianza. Para la
  cohorte del INE de 2017 existe una acusación de reparto PRI–PAN–PRD registrada
  en tribuna, no una afiliación probada.

PAN y PVEM tienen cobertura parcial en campaña por límites de acceso a archivos
ZIP de más de 2 GiB y no se presentan como cero.

## Archivos

- [`index.html`](index.html): reporte web de doce páginas, con texto
  seleccionable y enlaces a documentos oficiales.
- [`reporte_observaciones_pef_2023_2024.pdf`](reporte_observaciones_pef_2023_2024.pdf):
  PDF descargable generado desde el mismo HTML.
- [`data/analisis_pef_2023_2024.json`](data/analisis_pef_2023_2024.json):
  matriz de conteos, respuestas y fuentes.
- [`scripts/build_pdf.sh`](scripts/build_pdf.sh): conversión reproducible a PDF
  Carta horizontal.
- [`tests/test_report.py`](tests/test_report.py): controles de datos,
  estructura y PDF.
- [`research/relaciones_servidores_publicos/NOMBRAMIENTOS.md`](research/relaciones_servidores_publicos/NOMBRAMIENTOS.md):
  análisis jurídico y documental de las designaciones desde 2014.
- [`research/relaciones_servidores_publicos/salidas/nombramientos_y_respaldo.csv`](research/relaciones_servidores_publicos/salidas/nombramientos_y_respaldo.csv):
  matriz persona por persona.

La tipografía Montserrat se sirve localmente desde `assets/fonts/`, de modo que
el HTML y el PDF usan la misma familia aun si el dispositivo no la tiene
instalada.

## Consulta

Versión pública:
<https://luismesco.github.io/fiscalizacion-diputaciones-federales-2024/>

Repositorio:
<https://github.com/luismesco/fiscalizacion-diputaciones-federales-2024>
