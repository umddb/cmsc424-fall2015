# Project 5

Project 5 focuses on using Apache Spark for doing large-scale data analysis tasks. For this assignment, we will use relatively small datasets and  we won't run anything in distributed mode; however Spark can be easily used to run the same programs on much larger datasets.

## Getting Started with Spark

This guide is basically a summary of the excellent tutorials that can be found at the [Spark website](http://spark.apache.org).

[Apache Spark](https://spark.apache.org) is a relatively new cluster computing framework, developed originally at UC Berkeley. It significantly generalizes
the 2-stage Map-Reduce paradigm (originally proposed by Google and popularized by open-source Hadoop system); Spark is instead based on the abstraction of **resilient distributed datasets (RDDs)**. An RDD is basically a distributed collection 
of items, that can be created in a variety of ways. Spark provides a set of operations to transform one or more RDDs into an output RDD, and analysis tasks are written as
chains of these operations.

Spark can be used with the Hadoop ecosystem, including the HDFS file system and the YARN resource manager. 

### Installing Spark

Spark is already installed on the virtual machines. However, since there has been a significant version change since then, we will install and use the latest version.

1. Download the Spark package at http://spark.apache.org/downloads.html. We will use **Version 1.5.1, Pre-built for CDH 4**.
2. Move the downloaded file to the `/home/terrapin/spark` directory (or somewhere else), and uncompress it using: 
`tar zxvf spark-1.5.1-bin-cdh4.tgz`
3. This will create a new directory: `spark-1.5.1-bin-cdh4`. 
4. Set the SPARKHOME variable: `export SPARKHOME=/home/terrapin/spark/spark-1.5.1-bin-cdh4` (modify accordingly if you uncompressed it somewhere else)
5. If you want to reduce the amount of output that SPARK is producing, copy the `log4j.properties` file into `$SPARKHOME/conf`.

We are ready to use Spark. 

### Spark and Python

Spark primarily supports three languages: Scala (Spark is written in Scala), Java, and Python. We will use Python here -- you can follow the instructions at the tutorial
and quick start (http://spark.apache.org/docs/latest/quick-start.html) for other languages. The Java equivalent code can be very verbose and hard to follow. The below
shows a way to use the Python interface through the standard Python shell; I will also later post instructions to use iPython (that is more involved, but you can 
do more fun things with it like draw plots and visualizations). 

### PySpark Shell

1. `$SPARK_HOME/bin/pyspark`: This will start a Python shell (it will also output a bunch of stuff about what Spark is doing). The relevant variables are initialized in this python
shell, but otherwise it is just a standard Python shell.

2. `>>> textFile = sc.textFile("README.md")`: This creates a new RDD, called `textFile`, by reading data from a local file. The `sc.textFile` commands create an RDD
containing one entry per line in the file.

3. You can see some information about the RDD by doing `textFile.count()` or `textFile.first()`, or `textFile.take(5)` (which prints an array containing 5 items from the RDD).

4. We recommend you follow the rest of the commands in the quick start guide (http://spark.apache.org/docs/latest/quick-start.html). Here we will simply do the Word Count
application.

#### Word Count Application

The following command (in the pyspark shell) does a word count, i.e., it counts the number of times each word appears in the file `README.md`. Use `counts.take(5)` to see the output.

`>>> counts = textfile.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)`

Here is the same code without the use of `lambda` functions.

```
def split(line): 
    return line.split(" ")
def generateone(word): 
    return (word, 1)
def sum(a, b):
    return a + b

textfile.flatMap(split).map(generateone).reduceByKey(sum)
```

The `flatmap` splits each line into words, and the following `map` and `reduce` do the counting (we will discuss this in the class, but here is an excellent and detailed
description: [Hadoop Map-Reduce Tutorial](http://hadoop.apache.org/docs/r1.2.1/mapred_tutorial.html#Source+Code) (look for Walk-Through).

The `lambda` representation is more compact and preferable, especially for small functions, but for large functions, it is better to separate out the definitions.

### Running it as an Application

Instead of using a shell, you can also write your code as a python file, and *submit* that to the spark cluster. The `project5` directory contains a python file `wordcount.py`,
which runs the program in a local mode. To run the program, do:
`$SPARKHOME/bin/spark-submit wordcount.py`

### More...

We encourage you to look at the [Spark Programming Guide](https://spark.apache.org/docs/latest/programming-guide.html) and play with the other RDD manipulation commands. 
You should also try out the Scala and Java interfaces.

## Assignment Details

We have provided a Python file: `assignment.py`, that initializes the folllowing RDDs:
* An RDD consisting of lines from a Shakespeare play (`play.txt`)
* An RDD consisting of lines from a log file (`NASA_logs_sample.txt`)
* An RDD consisting of 2-tuples indicating friends relationships from a Social Network (`livejournal_sample.txt`)

The file also contains 3 examples of operations on these RDDs. 

Your tasks are to fill out the 5 functions that are defined in the `functions.py` file (starting with `task`). The amount of code that you 
write would be very small (the first one would be a one-liner).

* **Task 1**: This takes as input the playRDD and a list of words, and should count the number of different lines in which each of those words appeared.

* **Task 2**:  [Bigrams](http://en.wikipedia.org/wiki/Bigram) are sequences of two consecutive words. For example, the previous sentence contains the following bigrams: "Bigrams
are", "are simply", "simply sequences", "sequences of", etc.
Your task is to write a **Bigram Counting** application that can be composed as a two stage Map-Reduce job. 
	- The first stage counts bigrams.
	- The second stage MapReduce job takes the output of the first stage (bigram counts) and computes for each word the top 5 bigrams by count that it is a part of, and the bigram count associated with each.
Only count bigrams that appear within a single line (i.e., don't worry about bigrams where one word is the end of one line and the second word is the beginning of next.
The return value should be an PairRDD where the key is a word, and the value is the top 5 bigrams by count that it is a part of.

* **Task 3**: Here the goal is to count the [Jaccard Index](https://en.wikipedia.org/wiki/Jaccard_index) between two given hosts. In other words, find the set of the URLs visited by each of the two hosts, count the size of the
intersection of the two sets and divide by the size of the union of the two sets (don't forget to use `distinct()` to remove duplicates from the sets). The format of the log entries should be self-explanatory, but here are more details if you need: [NASA Logs](http://ita.ee.lbl.gov/html/contrib/NASA-HTTP.html)

* **Task 4**: For the logsRDD, count the top 5 URLs that have been visited.  You will first need to figure out how to parse the log lines appropriately to extract the URLs. The return should just be the list of 5 URLs.

* **Task 5**: `task5_pagerank` should implement one iteration of the standard algorithm for computing PageRanks (see [Wikipedia Page](https://en.wikipedia.org/wiki/PageRank) for more details on PageRank). This is an iterative algorithm that uses the values computed in the previous iteration to re-compute the values for the next iteration. Specifically, you should implement the formula described in the above Wikipedia page in the section `Damping Factor`. Use the damping factor of 0.85. The result should be an RDD that looks very similar to `initial_pageranks` but with new values (note that since RDDs are immutable, you have to construct a new RDD and return it).

You can use spark-submit to run the `assignment.py` file, but it would be easier to develop with pyspark (by copying the commands over). We will also shortly post iPython instructions.

### Submission

Submit the `functions.py` file.
