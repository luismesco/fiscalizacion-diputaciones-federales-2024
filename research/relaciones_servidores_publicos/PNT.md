# Verificación en la Plataforma Nacional de Transparencia

## Alcance de la consulta

Consulta directa realizada el 26 de julio de 2026 en el buscador de
Información Pública de la Plataforma Nacional de Transparencia (PNT). Se
revisaron separadamente los ámbitos `Federación` y `Federación (Histórica)`,
porque la plataforma migró los sujetos obligados del extinto INAI a nuevas
autoridades garantes.

La PNT sirve en este proyecto para verificar declaraciones patrimoniales,
trayectorias y áreas de adscripción. La obligación denominada **Servidores
Públicos Sancionados** se refiere a sanciones administrativas de personas
servidoras públicas; no sustituye el repositorio de sentencias electorales del
TEPJF ni identifica, por sí misma, sanciones impuestas a partidos políticos.

## Resultados de la consulta

| Sujeto obligado | Ejercicio | Ámbito PNT | Registros | Obligaciones | Resultado patrimonial |
|---|---:|---|---:|---:|---|
| Instituto Nacional Electoral | 2024 | Federación | 123,806 | 25 | No aparece la obligación de declaraciones patrimoniales |
| TEPJF | 2024 | Federación (Histórica) | 12,240 | 27 | No aparece la obligación de declaraciones patrimoniales |
| TEPJF | 2025 | Federación (Histórica) | 49,663 | 32 | 2,822 registros de declaraciones patrimoniales |

La ausencia de la fracción patrimonial en la consulta actual del ejercicio
2024 **no demuestra que el INE o el TEPJF omitieran publicarla en 2024**. Los
Lineamientos Técnicos citados por el propio INE establecen que, para la
fracción XII del artículo 70, se conserva en el sitio la información del
ejercicio en curso y la correspondiente al anterior. En julio de 2026, el
ejercicio 2024 ya está fuera de esa ventana.

La resolución `DIT 0581/2023` documenta, además, que el TEPJF había cargado
1,618 registros de declaraciones en el SIPOT para el segundo trimestre de
2023 y que el INAI verificó el funcionamiento del hipervínculo publicado.
Esto confirma que el SIPOT/PNT funcionaba como índice de los PDF alojados por
el sujeto obligado.

## Personas localizadas en la PNT

Se descargó sin modificaciones el CSV de 2,822 registros del TEPJF para 2025.
La extracción de las magistraturas relevantes se encuentra en
`salidas/pnt_personas_tepjf_2025.csv`.

- Janine M. Otálora Malassis: modificación y conclusión.
- Felipe de la Mata Pizaña: modificación.
- Felipe Alfredo Fuentes Barrera: modificación.
- Mónica Aralí Soto Fregoso: modificación.
- Reyes Rodríguez Mondragón: modificación.

Los cinco PDF de modificación fueron descargados desde los hipervínculos
oficiales contenidos en el CSV de la PNT.

## Control de calidad

El registro de **Felipe Alfredo Fuentes Barrera** presenta una inconsistencia:
la columna de la PNT dice `Ponencia Magistrado De La Mata Pizaña Felipe`,
aunque identifica a Fuentes Barrera como la persona declarante. La declaración
PDF enlazada por el mismo registro señala como área actual `Sala Superior` y
como cargo `Magistrado de Sala Superior`.

Por tanto, para establecer áreas de adscripción se da mayor peso al documento
primario enlazado que al campo catalogado de la tabla. La anomalía se conserva
en la salida para que el error sea auditable y no se propague como una
coincidencia laboral falsa.

## Aportación al cruce de relaciones

- La PNT confirma mediante su hipervínculo documental la declaración de Janine
  Otálora. Combinada con la declaración pública de Claudia Zavala, permanece
  acreditado que Zavala fue Secretaria Instructora en la ponencia de Otálora
  entre el 16 de noviembre de 2016 y el 4 de abril de 2017.
- La declaración de Felipe de la Mata registra cargos en la Sala Superior del
  TEPJF entre 2009 y 2014. Esto coincide temporalmente, a nivel de institución,
  con la trayectoria oficial de Arturo Castillo Loza en el TEPJF entre 2009 y
  2013. No se acredita todavía una misma ponencia.
- La declaración de Mónica Soto registra dos empleos en el Instituto Federal
  Electoral entre 1994 y 2007. La de Reyes Rodríguez registra que fue asesor
  en la oficina del consejero Benito Nacif entre el 1 de diciembre de 2010 y el
  15 de abril de 2011. Son antecedentes institucionales IFE/INE; no prueban una
  relación personal con quienes aprobaron la resolución de fiscalización en
  2024.

Estas coincidencias no prueban por sí mismas interés personal, dependencia
vigente, parcialidad, impedimento ni conflicto de interés.

