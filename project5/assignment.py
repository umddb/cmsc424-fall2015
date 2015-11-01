from pyspark import SparkContext
import re
from functions import *

sc = SparkContext("local", "Simple App")

## Load data into RDDs
playRDD = sc.textFile("play.txt")
logsRDD = sc.textFile("NASA_logs_sample.txt")
socialnetinputRDD = sc.textFile("livejournal_sample.txt")

## The following converts the socialnetRDD into 2-tuples with integers
socialnetRDD = socialnetinputRDD.map(lambda x: x.split("\t")).map(lambda x: (int(x[0]), int(x[1])))

## Word Count Application -- write out the output to a file
def example1(playRDD):
	counts = playRDD.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
	print counts.sortByKey().take(100)

## The following shows how to find all unique hosts making requests -- returns an RDD
def extractHost(logline):
	match = re.search('^(\S+) ', logline)
	if match is not None:
		return match.group(1)
	else:
		return None
def example2(logsRDD):
	hosts = logsRDD.map(extractHost).filter(lambda x: x is not None)
	hosts_distinct = hosts.distinct()
	print "In the {} log entries, there are {} unique hosts".format(hosts.count(), hosts_distinct.count())

## The following shows how to find the list of neighbors of each node, and also the degree of each node
def example3(socialnetRDD):
	# To compute degrees, we first use a map to output (u, 1) for every edge (u, v). Then we can compute the degrees using a reduceByKey and a sum reducer
	degrees = socialnetRDD.map(lambda x: (x[0], 1)).reduceByKey(lambda x, y: x + y)

	# Using groupByKey instead gives us a list of neighbors, but the list is returned as a pyspark.resultiterable.ResultIterable object
	neighbors_1 = socialnetRDD.groupByKey()

	# We can convert that into a list of neighbors as follows
	neighbors_2 = socialnetRDD.groupByKey().map(lambda x: (x[0], list(x[1])))

	print degrees.take(10)
	print neighbors_2.take(10)

example1(playRDD)
example2(logsRDD)
example3(socialnetRDD)

print task1_count_lines(playRDD, ['LEONATO', 'Messenger', 'BENEDICK', 'Arragon'])

task2_count_bigrams(playRDD)

host1 = '199.120.110.21'
host2 = 'd104.aa.net'
print "The Jaccard Similarity between hosts {} and {} is {}".format(host1, host2, task3_find_similarity(logsRDD, '199.120.110.21', 'd104.aa.net'))

print task4_top_5_URLs(logsRDD)

# The following creates an initial set of PageRanks to pass to the iterative function
vertices = socialnetRDD.map(lambda x: x[0]).distinct()
count_vertices = vertices.count()
initial_pageranks = vertices.map(lambda x: (x, 1.0/count_vertices))
print task5_pagerank(socialnetRDD, initial_pageranks).take(100)
