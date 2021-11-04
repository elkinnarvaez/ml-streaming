import sys
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.sql.functions import *
from pyspark.ml.classification import LogisticRegression, DecisionTreeClassifier, RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator


if __name__ == "__main__":
    #inicio sesion spark
    spark=SparkSession.builder.appName('MachineLearning').getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    
    #carga de datos
    df = spark.read.csv("/user/maria_dev/ml-streaming/data/cleanedData/*.csv", sep=',', header= True, inferSchema=True)

    windowSize = 100000
    slide = 40
    # print(df)

    rows = df.collect()
    windowStart = 0
    i = 0
    window = []
    while(i < len(rows)):
        if(i - windowStart + 1 > windowSize):
            windowStart = i
            i = i - 1
            df = spark.createDataFrame(window)
            # df.show()
            vector = VectorAssembler(inputCols = ['Domestic', 'Beat', 'District', 'Community Area', 'X Coordinate', 'Y Coordinate', 
                                                'IUCR_index', 'Location Description_index', 'FBI Code_index', 'Block_index', 
                                                'mesDel', 'diaDel', 'horaDel', 'minutoDel'], outputCol = 'atributos')
            df = vector.transform(df)
            df = df.select('atributos', 'Arrest')
            df = df.selectExpr("atributos as atributos", "Arrest as label")

            #division del dataset 70% entrenamiento - 30% pruebas
            train, test = df.randomSplit([0.7, 0.3], seed = 2018)

            #instacia del evaluador
            evaluator = BinaryClassificationEvaluator()

            #random forest 
            rf = RandomForestClassifier(featuresCol = 'atributos', labelCol = 'label')
            rfModel = rf.fit(train)
            predictionsRf = rfModel.transform(test)
            accuracy3 = predictionsRf.filter(predictionsRf.label == predictionsRf.prediction).count() / float(predictionsRf.count())
            print("=========================================================================================================================")
            print("RANDOM FOREST") 
            print("Test Area Under ROC: " + str(evaluator.evaluate(predictionsRf, {evaluator.metricName: "areaUnderROC"}))) 
            print("presicion random forest: ", accuracy3)
            print("=========================================================================================================================")
            window = []
        else:
            window.append(rows[i])
        i += 1