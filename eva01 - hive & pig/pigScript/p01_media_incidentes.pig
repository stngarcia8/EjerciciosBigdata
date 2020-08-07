-- Pregunta 01: Obtener media de los incidentes por tipo y periodo
-- Orden de los resultados
-- Promedio de incidentes periodo 85-99
-- Promedio accidentes periodo 85-99
-- Promedio incidentes periodo 85-99
-- Promedio accidentes periodo 00-14

-- Cargando datos
data = load 'asathor/airline-safety.csv' using PigStorage(',') as (
aerolinea:chararray, km_semanal:biginteger,
incidentes_85_99:int, fatales_85_99:int, muertes_85_99:int,
incidentes_00_14:int, fatales_00_14:int, muertes_00_14:int);
-- Extranyendo columnas a calcular
new_data = FOREACH data GENERATE incidentes_85_99, fatales_85_99, incidentes_00_14, fatales_00_14;

-- Agrupando datos para los calculos
grouped = GROUP new_data all;

-- Obteniendo los promedios
averaged = FOREACH grouped GENERATE ROUND_TO(AVG(new_data.incidentes_85_99),2), ROUND_TO(AVG(new_data.fatales_85_99),2), ROUND_TO(AVG(new_data.incidentes_00_14),2), ROUND_TO(AVG(new_data.fatales_00_14),2);

-- Mostrando resultados
dump averaged;