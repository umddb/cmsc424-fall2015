from pyspark import SparkContext, SparkConf
import re

# Given the playRDD and a list of words: for each word, count the number of lines that contain it -- the return should be a list 
# with the same length as list_of_words containing the counts
def task1_count_lines(playRDD, list_of_words):
	return [0]

# The following function should solve the bigram counting problem; the return should be an RDD
def task2_count_bigrams(playRDD):
	return None

# Given two hosts (see example below), find the Jaccard Similarity Coefficient between them based on
# the URLs they visited. i.e., count the number of URLs that they both visited (ignoring duplicates),
# and divide by the total number of unique URLs visited by either
# The return value should be a Double
def task3_find_similarity(logsRDD, host1, host2):
	return -1

# The following function should find the top 5 URLs that were accessed most frequently in the provided logs
# The result should be simply a list with 5 strings, denoting the URLs
def task4_top_5_URLs(logsRDD):
	return None

# Implement one iteration of PageRank on the socialnetRDD. Specifically, the input is 2 RDDs, the socialnetRDD and another RDD containing the 
# current PageRank for the vertices
# Compute the new PageRank for the vertices and return that RDD
def task5_pagerank(socialnetRDDs, pagerankPreviousIterationRDD):
	return socialnetRDDs

