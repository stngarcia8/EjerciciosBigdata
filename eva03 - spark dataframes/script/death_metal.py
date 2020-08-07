# Ejercicio: Analisis, exploracion de datos dataset death metall 
# Alumno: Daniel Garcia
# Ramo: Bigdata
# Seccion:002D
# Profesor: Daniel Montero
# Consideraciones: Archivos csv (albumes.csv, bands.csv y reviews.csv) deben estar en hdfs

from pyspark.context import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.session import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, FloatType
from pyspark.sql.functions import isnan, when, count, col, round

# Definiendo el contexto para el script (en pyspark no es necesario) y cargando datos
# sc = SparkContext('local')
spark = SparkSession(sc)


# Preparando schema para las bandas y cargando archivo csv
band_schema = StructType([
    StructField('id', IntegerType(), True), 
    StructField('name', StringType(), False), 
    StructField('country', StringType(), False), 
    StructField('status', StringType(), False), 
    StructField('formed_in', IntegerType(), True), 
    StructField('genre', StringType(), False), 
    StructField('theme', StringType(), False), 
    StructField('active', StringType(), False), 
    ])
bands_data = spark.read.format('csv').option('header', 'True').option('sep', ',').option('encoding', 'UTF-8').load('data/original/bands.csv', schema=band_schema)
print('Bandas cargadas {0}'.format(bands_data.count()))
bands_data.show(10, truncate=True)


# Preparando schema para los albumnes y cargando archivo csv
album_schema = StructType([
    StructField('id', IntegerType(), True), 
    StructField('band', IntegerType(), True), 
    StructField('title', StringType(), False), 
    StructField('year', IntegerType(), True), 
    ])
albums_data = spark.read.format('csv').option('header', 'True').option('sep', ',').option('encoding', 'UTF-8').load('data/original/albums.csv', schema=album_schema)
print('Discos cargados {0}'.format(albums_data.count()))
albums_data.show(10, truncate=True)


# Preparando schema para las reviews y cargando archivo csv
review_schema = StructType([
    StructField('id', IntegerType(), True), 
    StructField('album', IntegerType(), False), 
    StructField('title', StringType(), False), 
    StructField('score', FloatType(), False), 
    StructField('content', StringType(), False), 
    ])
reviews_data = spark.read.format('csv').option('header', 'True').option('sep', ',').option('encoding', 'UTF-8').load('data/original/reviews.csv', schema=review_schema)
print('Reviews cargadas {0}'.format(reviews_data.count()))
reviews_data.show(10, truncate=True)


# Eliminando columnas inecesarias de las bandas
cols = ['theme', 'active']
bands_data = bands_data.drop(*cols)
bands_data.printSchema()


# Eliminando columnas inecesarias de las reviews
cols = ['content']
reviews_data = reviews_data.drop(*cols)
reviews_data.printSchema()


 # Buscando elementos nulos
bands_data.select([count(when(isnan(c), c)).alias(c) for c in bands_data.columns]).show()
albums_data.select([count(when(isnan(c), c)).alias(c) for c in albums_data.columns]).show()
reviews_data.select([count(when(isnan(c), c)).alias(c) for c in reviews_data.columns]).show()


# mostrando estadistica descriptiva de las bandas
bands_data.describe().show(15, truncate=True)


# mostrando estadistica descriptiva de los albumes
albums_data.describe().show(15, truncate=True)

# mostrando estadistica descriptiva de las reviews
reviews_data.describe().show(15, truncate=True)


print('Mostrando valores unicos en bandas')
for col in bands_data:
    col_count = bands_data.select(col).distinct().count()
    print('{0}, valores unicos {1}'.format(col, col_count))

print('Mostrando valores unicos en los albums')
for col in albums_data:
    col_count = albums_data.select(col).distinct().count()
    print('{0}, valores unicos {1}'.format(col, col_count))


print('Mostrando valores unicos en las reviews')
for col in reviews_data:
    col_count = reviews_data.select(col).distinct().count()
    print('{0}, valores unicos {1}'.format(col, col_count))


# Mostrando los valores de columna status
value_counts = bands_data.groupBy('status').count().orderBy('count', ascending=False)
value_counts.show(10, truncate=True)

# relacion de estados de bandas versus año de formacion
bands_data.crosstab('formed_in', 'status').show(truncate=True)


# Uniendo los dataframes
albums_reviews = albums_data.join(reviews_data, albums_data.id == reviews_data.album)
albums_reviews.show(20, truncate=True)


# Eliminando columnas inecesarias
cols = ['id', 'album']
albums_reviews = albums_reviews.drop(*cols)
new_schema = ['band', 'title', 'year', 'titulo', 'score']
albums_reviews = albums_reviews.toDF(*new_schema)
cols = ['titulo']
albums_reviews = albums_reviews.drop(*cols)
albums_reviews.printSchema()


# uniendo las bandas y sus albumes
bands_albums = bands_data.join(albums_reviews, bands_data.id == albums_reviews.band)
cols = ['band']
bands_albums = bands_albums.drop(*cols)
bands_albums.show(15, truncate=True)
bands_albums.printSchema()

# calculando el promedio del score por banda
band_score = bands_albums.groupby('id', 'name', 'score').mean()
cols = ['name', 'score', 'avg(id)', 'avg(formed_in)', 'avg(year)']
band_score = band_score.drop(*cols)
band_score.show(15, truncate=True)


# Uniendo las bandas y su score
bands = bands_data.join(band_score, bands_data.id == band_score.id)
cols = ['id', 'score']
bands = bands.drop(*cols)
bands = bands.withColumnRenamed('avg(score)', 'score')
bands = bands.withColumn('score', round(bands['score'], 2))
bands.show(10, truncate=True)


# Prediciendo cual sera el genero predominante por status, fecha de formacion y score de la banda
from pyspark.ml import Pipeline
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import StringIndexer, VectorIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler


# indexando columnas
indexer = StringIndexer(inputCol="status", outputCol="statusIndex")
bands_indexed = indexer.fit(bands).transform(bands)
bands_indexed.show()


# construyendo el vector con las caracteristicas
vector_assembler = VectorAssembler(inputCols=["score", "formed_in", "statusIndex"],outputCol="features")
bands_temp = vector_assembler.transform(bands_indexed)


# Extrayendo datos de entrenamiento y test
(trainingData, testData) = bands_temp.randomSplit([0.8, 0.2])
# dt = DecisionTreeClassifier(labelCol="statusIndex", featuresCol="features")
rf = RandomForestClassifier(labelCol="statusIndex",featuresCol="features", numTrees=10)
bands_model = rf.fit(trainingData)
predictions = bands_model.transform(testData)
predictions.select("genre", "status", 'formed_in', 'country').show(3, truncate=True)



