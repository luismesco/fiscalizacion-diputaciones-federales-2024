# Fiscalización federal 2024: hallazgos auditables

## Alcance

Proceso Electoral Federal Ordinario 2023-2024, etapas de precampaña y
campaña, cargos de Presidencia, senadurías y diputaciones federales. Los
partidos se cuentan de manera individual; las coaliciones se conservan en el
inventario, pero no se mezclan con el ranking de partidos.

## Unidad de análisis

Una observación es cada bloque único `ID` + `Observación` del dictamen
individual del INE. No se cuentan como observaciones:

- conclusiones sancionatorias;
- hallazgos o registros contenidos dentro de anexos;
- montos;
- testigos;
- filas de operaciones;
- procedimientos oficiosos como si fueran nuevas observaciones.

El conteo se reproduce con:

```sh
python3 research/scripts/analyze_observations.py
```

## Resultado corregido

Entre los cinco partidos con dictámenes completos ya extraídos:

| Partido | Precampaña | Campaña | Total | Cobertura |
|---|---:|---:|---:|---|
| Movimiento Ciudadano | 73 | 243 | **316** | Completa |
| Morena | 57 | 231 | **288** | Completa |
| PT | 24 | 175 | **199** | Completa |
| PRD | 30 | 132 | **162** | Completa |
| PRI | 37 | 120 | **157** | Completa |
| PAN | 59 | pendiente | pendiente | Parcial |
| PVEM | 29 | pendiente | pendiente | Parcial |

Los dictámenes de campaña de PAN y PVEM están dentro de ZIP oficiales de
3.108 GB y 2.559 GB, respectivamente. El servidor del INE rechaza rangos cuyo
inicio supera 2 GiB; por ello ambos se marcan expresamente como pendientes y
no como cero.

## Respuestas A, B y C

### A. Partido más observado

El resultado documentado es **Movimiento Ciudadano**, con 316 observaciones:
73 de precampaña y 243 de campaña. Supera por 28 a Morena.

### B. Partido más observado que trascendió a un expediente del TEPJF

También es **Movimiento Ciudadano**. Impugnó el dictamen INE/CG1928/2024 y la
resolución INE/CG1929/2024 en los recursos SUP-RAP-342/2024 y
SUP-RAP-400/2024, acumulados. La materia escindida produjo además
SM-RAP-168/2024 y SM-RAP-170/2024, acumulados.

### C. Partido más observado con expediente resuelto y sanciones subsistentes

También es **Movimiento Ciudadano**. El 4 de septiembre de 2024, la Sala
Superior:

- revocó siete conclusiones para efectos de que el INE emitiera una nueva determinación;
- confirmó treinta conclusiones sancionatorias.

El 8 de octubre de 2024, la Sala Regional Monterrey confirmó la parte de la
controversia que le fue remitida.

Precisión jurídica: las sanciones fueron impuestas por el Consejo General del
INE. El TEPJF resolvió las impugnaciones y confirmó o revocó las
determinaciones; no fue la autoridad que originó las multas.

## Fuentes rectoras

- INE/CG212/2024, dictamen consolidado de precampaña:
  https://repositoriodocumental.ine.mx/xmlui/handle/123456789/166305
- INE/CG213/2024, resolución de precampaña:
  https://repositoriodocumental.ine.mx/xmlui/handle/123456789/166317
- INE/CG1928/2024, dictamen consolidado de campaña:
  https://repositoriodocumental.ine.mx/xmlui/handle/123456789/175380
- INE/CG1929/2024, resolución de campaña:
  https://repositoriodocumental.ine.mx/xmlui/handle/123456789/175375
- SUP-RAP-342/2024 y SUP-RAP-400/2024 acumulados:
  https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-0342-2024
- SM-RAP-168/2024 y SM-RAP-170/2024 acumulados:
  https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SM-RAP-0168-2024-

## Límite de publicación de los OEO

Las fichas del repositorio del INE publican los dictámenes, resoluciones,
anexos y testigos en paquetes ZIP. Los oficios de errores y omisiones y sus
respuestas aparecen identificados en los dictámenes, pero el universo de PDF
de los oficios y escritos de respuesta no está publicado como una colección
abierta y separada en esas fichas; parte de ese intercambio reside en el SIF.
El inventario distingue por ello entre documento identificado, archivo
internamente listado y archivo efectivamente recuperado.
