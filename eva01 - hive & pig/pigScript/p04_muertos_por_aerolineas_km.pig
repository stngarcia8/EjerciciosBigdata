-- Pregunta 04:
-- Listar las aerolineas que mas kilometraje tienen
-- y que mortandad poseen en el periodo 2000-2014

-- Cargando los datos
data = load 'asathor/airline-safety.csv' using PigStorage(',') as (
aerolinea:chararray, km_semanal:biginteger, 
incidentes_85_99:int, fatales_85_99:int, muertes_85_99:int,
incidentes_00_14:int, fatales_00_14:int, muertes_00_14:int);

-- Extrayendo solo los campos a procesar
new_data = FOREACH data GENERATE aerolinea, km_semanal, muertes_00_14;

-- Ordenando los datos
ordered = ORDER new_data BY km_semanal DESC, muertes_00_14 DESC;

-- Limitando los resultados a los 3 primeros
limited = LIMIT ordered 3;

-- Mostrando los resultados
dump limited;