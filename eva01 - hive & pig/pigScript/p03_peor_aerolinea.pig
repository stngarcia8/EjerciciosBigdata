-- Pregunta 03:
-- Visualizar la aerolinea con la mayor cantidad de muertos
-- en el periodo 2000-2014

-- Cargando datos
data = load 'asathor/airline-safety.csv' using PigStorage(',') as (
aerolinea:chararray, km_semanal:biginteger,
incidentes_85_99:int, fatales_85_99:int, muertes_85_99:int,
incidentes_00_14:int, fatales_00_14:int, muertes_00_14:int);

-- Extranyendo los campos a visualizar
new_data = FOREACH data GENERATE aerolinea, muertes_00_14;

-- Ordenando los datos por cantidad de fallecidos
ordered = ORDER new_data BY muertes_00_14 DESC;

-- Limitando los resultados a 3 primeros
limited = LIMIT ordered 3;

-- Mostrando los resultados
dump limited;