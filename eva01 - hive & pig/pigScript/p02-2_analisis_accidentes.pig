-- Pregunta 02
-- Item 2: Analisis de accidentes por periodo
-- Orden de los resultados:
-- Cantidad accidentes periodo 85-99
-- Cantidad accidentes periodo 00-14
-- Total accidentes de la muestra

-- Cargando datos
data = load 'asathor/airline-safety.csv' using PigStorage(',') as (
aerolinea:chararray, km_semanal:biginteger,
incidentes_85_99:int, fatales_85_99:int, muertes_85_99:int,
incidentes_00_14:int, fatales_00_14:int, muertes_00_14:int);

-- Extrayendo columnas a utilizar
new_data = FOREACH data GENERATE fatales_85_99, fatales_00_14;

-- Agrupando datos para calculos
grouped = GROUP new_data all;

-- Calculando las sumas de accidentes
calculated = FOREACH grouped GENERATE SUM(new_data.fatales_85_99), SUM(new_data.fatales_00_14), SUM(new_data.fatales_85_99)+SUM(new_data.fatales_00_14);

-- Mostrando resultados
dump calculated;