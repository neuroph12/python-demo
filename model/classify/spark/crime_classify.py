#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : crime_classify.py
# @Author: wu gang
# @Date  : 2018/8/30
# @Desc  : 利用PySpark的多类文本分类：将旧金山犯罪描述分为33个预定义类别。
# 参考：Multi-Class Text Classification with PySpark
# 地址：https://towardsdatascience.com/multi-class-text-classification-with-pyspark-7d78d022ed35
# @Contact: 752820344@qq.com

from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark.sql.functions import col
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


# 很明显Logistic回归将是我们在这个实验中的模型，具有交叉验证。
# def main():
if __name__ == '__main__':

    sc = SparkContext()
    sqlContent = SQLContext(sc)

    # load data
    data = sqlContent.read.format('com.databricks.spark.csv') \
        .options(header='true', inferschema='true') \
        .load('../../../data/crime/train.csv')
    data.show(5)
    # 剔除下面列名的数据
    drop_list = ['Dates', 'DayOfWeek', 'PdDistrict', 'Resolution', 'Address', 'X', 'Y']
    data = data.select([column for column in data.columns if column not in drop_list])
    # 查看前5行
    data.show(5)
    # 输出schema DataFrame中的数据结构信息
    data.printSchema()
    # 前20个犯罪类别
    data.groupBy("Category").count().orderBy(col("count").desc()).show()
    # 前20个犯罪描述：
    data.groupBy("Descript").count().orderBy(col("count").desc()).show()

    # Spark Machine Learning Pipelines API is similar to Scikit-Learn.
    # 正则表达式
    regexTokenizer = RegexTokenizer(inputCol="Descript", outputCol="words", pattern="\\W")
    # stop words
    add_stopwords = ["http", "https", "amp", "rt", "t", "c", "the"]
    stopwordsRemover = StopWordsRemover(inputCol="words", outputCol="filtered").setStopWords(add_stopwords)
    # bag of words count
    # 计数向量 CountVectorizer 参考： https://www.jianshu.com/p/bbf4d3811222
    countVectors = CountVectorizer(inputCol="filtered", outputCol="features", vocabSize=10000, minDF=5)

    # StringIndexer将字符串类型的标签列，编码为按标签频率排序的[0，numLabels] 标签索引列。
    # 标签列（类别）将被编码为标签索引，从0到32; 最常见的标签（LARCENY / THEFT）将被索引为0。
    label_stringIdx = StringIndexer(inputCol="Category", outputCol="label")
    pipeline = Pipeline(stages=[regexTokenizer, stopwordsRemover, countVectors, label_stringIdx])
    # Fit the pipeline to training documents.
    pipelineFit = pipeline.fit(data)
    dataset = pipelineFit.transform(data)
    dataset.show(5)

    # Partition Training & Test sets 训练集和测试集分割
    # set seed for reproducibility
    (trainingData, testData) = dataset.randomSplit([0.7, 0.3], seed=100)
    print("Training Dataset Count: " + str(trainingData.count()))
    print("Test Dataset Count: " + str(testData.count()))

    # Model Training and Evaluation
    # Logistic Regression using Count Vector Features 使用计数向量特征的逻辑回归
    # 模型将在测试集上进行预测和评分; 展示概率Top10预测。
    lr = LogisticRegression(maxIter=20, regParam=0.3, elasticNetParam=0)
    lrModel = lr.fit(trainingData)
    predictions = lrModel.transform(testData)
    predictions.filter(predictions['prediction'] == 0) \
        .select("Descript", "Category", "probability", "label", "prediction") \
        .orderBy("probability", ascending=False) \
        .show(n=10, truncate=30)

    # accuracy
    evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
    evaluator.evaluate(predictions)

    # Logistic Regression using TF-IDF Features 使用TF-IDF特征的逻辑回归
    from pyspark.ml.feature import HashingTF, IDF

    hashingTF = HashingTF(inputCol="filtered", outputCol="rawFeatures", numFeatures=10000)
    # minDocFreq: remove sparse terms
    idf = IDF(inputCol="rawFeatures", outputCol="features", minDocFreq=5)
    pipeline = Pipeline(stages=[regexTokenizer, stopwordsRemover, hashingTF, idf, label_stringIdx])
    pipelineFit = pipeline.fit(data)
    dataset = pipelineFit.transform(data)
    (trainingData, testData) = dataset.randomSplit([0.7, 0.3], seed=100)
    lr = LogisticRegression(maxIter=20, regParam=0.3, elasticNetParam=0)
    lrModel = lr.fit(trainingData)
    predictions = lrModel.transform(testData)
    predictions.filter(predictions['prediction'] == 0) \
        .select("Descript", "Category", "probability", "label", "prediction") \
        .orderBy("probability", ascending=False) \
        .show(n=10, truncate=30)
    evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
    evaluator.evaluate(predictions)

    # Cross-Validation 交叉验证
    # 尝试交叉验证来调整我们的超参数，只调整计数向量Logistic回归。
    pipeline = Pipeline(stages=[regexTokenizer, stopwordsRemover, countVectors, label_stringIdx])

    pipelineFit = pipeline.fit(data)
    dataset = pipelineFit.transform(data)
    (trainingData, testData) = dataset.randomSplit([0.7, 0.3], seed=100)

    lr = LogisticRegression(maxIter=20, regParam=0.3, elasticNetParam=0)

    from pyspark.ml.tuning import ParamGridBuilder, CrossValidator

    # Create ParamGrid for Cross Validation
    paramGrid = (ParamGridBuilder()
                 .addGrid(lr.regParam, [0.1, 0.3, 0.5])  # regularization parameter
                 .addGrid(lr.elasticNetParam, [0.0, 0.1, 0.2])  # Elastic Net Parameter (Ridge = 0)
                 #            .addGrid(model.maxIter, [10, 20, 50]) #Number of iterations
                 #            .addGrid(idf.numFeatures, [10, 100, 1000]) # Number of features
                 .build())

    # Create 5-fold CrossValidator
    cv = CrossValidator(estimator=lr, estimatorParamMaps=paramGrid, evaluator=evaluator, numFolds=5)

    cvModel = cv.fit(trainingData)

    predictions = cvModel.transform(testData)
    # Evaluate best model
    evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
    evaluator.evaluate(predictions)

    print("naive bayes: ")
    # naive_bayes(trainingData, testData)


# Naive Bayes 朴素贝叶斯
def naive_bayes(trainingData, testData):
    from pyspark.ml.classification import NaiveBayes

    nb = NaiveBayes(smoothing=1)
    model = nb.fit(trainingData)
    predictions = model.transform(testData)
    predictions.filter(predictions['prediction'] == 0) \
        .select("Descript", "Category", "probability", "label", "prediction") \
        .orderBy("probability", ascending=False) \
        .show(n=10, truncate=30)

    evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
    evaluator.evaluate(predictions)


# Random Forest 随机森林
# 随机森林是一种非常好的，强大而通用的方法，但对于高维稀疏数据来说，它并不是最好的选择。
def random_forest(trainingData, testData):
    from pyspark.ml.classification import RandomForestClassifier

    rf = RandomForestClassifier(labelCol="label", \
                                featuresCol="features", \
                                numTrees=100, \
                                maxDepth=4, \
                                maxBins=32)
    # Train model with Training Data
    rfModel = rf.fit(trainingData)
    predictions = rfModel.transform(testData)
    predictions.filter(predictions['prediction'] == 0) \
        .select("Descript", "Category", "probability", "label", "prediction") \
        .orderBy("probability", ascending=False) \
        .show(n=10, truncate=30)
    evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
    evaluator.evaluate(predictions)
