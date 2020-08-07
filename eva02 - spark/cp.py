# Ejercicio02: Contar palabras
# Alumno: Carla Alvarez, Daniel Garcia, Juan Carlos Lopez, Carlos Mellado
# Ejecutar con: spark-submit cp.py > cp.txt
# Visualizar resultado: cat cp.txt
# Consideraciones: archivo 'peliculas.txt' debe haber sido cargado a hdfs en la raiz
import re
from pyspark.context import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.session import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType

# Definiendo el contexto para el script (en pyspark no es necesario) y cargando datos
sc = SparkContext()
spark = SparkSession(sc)
schema = StructType([StructField('Id', IntegerType(), True), StructField('NombrePelicula', StringType(), False), StructField('Fecha', DateType(), True)])
data = spark.read.format('csv').option('header', 'False').option('sep', '\t').option('mode', 'DROPMALFORMED').load('peliculas.txt', schema=schema)

# Trabajando con los titulos de las pelis
titulos = data.rdd.map(lambda fila: str(re.sub(r'\([0-9{4})]*\)', '', fila.NombrePelicula).lower().strip())).collect()
texto = ''.join(titulos).lower()
titulos = sc.parallelize(list(texto.split(' ')))

# Contando palabras y filtrando 
palabras = titulos.map(lambda palabra: (palabra, 1)).reduceByKey(lambda a,b:a +b)
especiales = ['', ' ', 'the', 'and']
palabras = palabras.filter(lambda x: x[0] not in especiales)
resultados = palabras.takeOrdered(10, key = lambda x: -x[1])

# Mostrando las 10 palabras mas usadas
print('Las palabras mas frecuentes son:')
for resultado in resultados:
	print('[{0}] ==> {1}'.format(resultado[0], resultado[1]))
