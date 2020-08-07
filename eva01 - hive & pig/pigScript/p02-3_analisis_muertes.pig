-- Pregunta 02:
-- item 3: Analisis de muertes por periodo
-- orden de resultados:
-- cantidad fallecidos periodo 88-99
-- Cantidad fallecidos periodo 85-99
-- Total fallecidos en la muestra

-- Cargando datos
data = load 'asathor/airline-safety.csv' using PigStorage(',') as (
aerolinea:chararray, km_semanal:biginteger,
incidentes_85_99:int, fatales_85_99:int, muertes_85_99:int,
incidentes_00_14:int, fatales_00_14:int, muertes_00_14:int);

-- Extrayendo columnas a utilizar
new_data = FOREACH data GENERATE muertes_85_99, muertes_00_14;

-- Agrupando para realizar calculos
grouped = GROUP new_data all;

-- Calculando datos
calculated = FOREACH grouped GENERATE SUM(new_data.muertes_85_99), SUM(new_data.muertes_00_14), SUM(new_data.muertes_85_99)+SUM(new_data.muertes_00_14);

-- Mostrando resultados
dump calculated;