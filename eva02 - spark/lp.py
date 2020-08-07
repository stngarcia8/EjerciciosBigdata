# Ejercicio01: Largo del titulo de la pelicula
# Alumnos: Carla Alvarez, Daniel Garcia, Juan Carlos Lopez, Carlos Mellado
# Ejecutar con: spark-submit lp.py > lp.txt
# Visualizar resultado: cat lp.txt
# Consideraciones: archivo 'peliculas.txt' debe haber sido cargado a hdfs en la raiz

import re
from pyspark.context import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.session import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType

# Definiendo el contexto para el script (en pyspark no es necesario) y cargando los datos
sc = SparkContext()
spark = SparkSession(sc)
schema = StructType([StructField('Id', IntegerType(), True), StructField('NombrePelicula', StringType(), False), StructField('Fecha', DateType(), True)])
data = spark.read.format('csv').option('header', 'False').option('sep', '\t').option('mode', 'DROPMALFORMED').load('peliculas.txt', schema=schema)

# Buscando el titulo con la maxima cantidad de caracteres
titulos = data.rdd.map(lambda fila: re.sub(r'\([0-9{4})]*\)', '', fila.NombrePelicula).lower().strip())
titulos = titulos.map(lambda x: (str(x), len(str(x))))
resultado = titulos.takeOrdered(1, key = lambda x: -x[1])

# Mostrando resultados
print('La pelicula con el titulo mas largo es:')
print('Pelicula: {0}'.format(str(resultado[0][0])))
print('Largo: {0}'.format(str(resultado[0][1])))
