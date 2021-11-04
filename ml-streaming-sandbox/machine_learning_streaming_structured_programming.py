import sys
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.sql.functions import *
from pyspark.ml.classification import LogisticRegression, DecisionTreeClassifier, RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.sql.types import *


if __name__ == "__main__":
    #inicio sesion spark
    spark=SparkSession.builder.appName('MachineLearningStreaming').getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    sch1 = StructType([StructField('Arrest', BooleanType(), True),
                        StructField('Domestic', BooleanType(), True),
                        StructField('Beat', IntegerType(), True),
                        StructField('District', FloatType(), True),
                        StructField('Community Area', FloatType(), True),
                        StructField('X Coordinate', FloatType(), True),
                        StructField('Y Coordinate', FloatType(), True),
                        StructField('IUCR_index', FloatType(), True),
                        StructField('Location Description_index', FloatType(), True),
                        StructField('FBI Code_index', FloatType(), True),
                        StructField('Block_index', FloatType(), True),
                        StructField('mesDel', IntegerType(), True),
                        StructField('diaDel', IntegerType(), True),
                        StructField('horaDel', IntegerType(), True),
                        StructField('minutoDel', IntegerType(), True),
                        StructField('timestamp', TimestampType(), True)])
    sch2 = StructType([StructField('id', IntegerType(), True),
                        StructField('name', StringType(), True),
                        StructField('age', IntegerType(), True),
                        StructField('profession', StringType(), True),
                        StructField('city', StringType(), True),
                        StructField('salary', DoubleType(), True)])

    #carga de datos
    df = spark.readStream.format('csv').schema(sch1).option("header", True).option("includeTimestamp", True).load("/user/maria_dev/ml-streaming/data/cleanedData")

    query = df.select((df.Beat).alias("Beat"), (df.timestamp).alias("time")).groupBy(window("time", "1 minutes")).count().sort(desc("window"))

    result = query.writeStream.outputMode("complete").format("console").start(truncate=False)
    
    result.awaitTermination()