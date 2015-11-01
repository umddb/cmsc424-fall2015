from pyspark import SparkContext, SparkConf

textFile = sc.textFile("README.md")

counts = textFile.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

print counts.sort().take(100)

counts.saveAsTextFile("output")
