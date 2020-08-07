-- Pregunta 02
-- Item 1: Analisis de incidentes
-- Orden de los resultados:
-- Cantidad de incidentes periodo 85-99
-- Cantidad de incidentes periodo 00-14
-- Total de incidentes de la muestra

-- Cargando datos
data = load 'asathor/airline-safety.csv' using PigStorage(',') as (
aerolinea:chararray, km_semanal:biginteger,
incidentes_85_99:int, fatales_85_99:int, muertes_85_99:int,
incidentes_00_14:int, fatales_00_14:int, muertes_00_14:int);

-- Extrayendo columnas a calcular
new_data = FOREACH data GENERATE incidentes_85_99, incidentes_00_14;

-- Agrupando datos para calculo
grouped = GROUP new_data all;

-- Realizando las sumas
calculated = FOREACH grouped GENERATE SUM(new_data.incidentes_85_99), SUM(new_data.incidentes_00_14), SUM(new_data.incidentes_85_99)+SUM(new_data.incidentes_00_14);

-- Mostrando los resultados
dump calculated;