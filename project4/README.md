## Project 4: Indexes and Query Processing Algorithms, CMSC424, Fall 2015

*The assignment is to be done by yourself.*

### Overview

In this project, you will modify a very simple database system that we have written to illustrate some of the B+-Tree and Query Processing algorithms. 
The database system is written in Python and attempts to simulate how a database system would work, including what blocks it would read from disk, etc.

* `disk_relations.py`: This module contains the classes Block, RelationBlock, Relation, and a few others helper classes like Pointer. A Block is a base class, 
that is subclassed by RelationBlock and BTreeBlock (in `btree.py` file). A RelationBlock contains a set of tuples, and a Relation contains a list of RelationBlocks. 
* `btree.py`: Code that implements some of the BTree functionality including search, insert, and delete (partially). The main class here is the BTreeBlock class, that 
captures the information stored in a BTree node.
* `queryprocessing.py`: This contains naive implementations of some of the query processing operators, including SequentialScan, NestedLoopsJoin, and HashJoin. The operators are written using the iterator `get_next` interface, which is discussed in Chapter 12.7.2.1.

There are a set of parameters that control how many tuples can be stored in each RelationBlock, how many key/ptrs can be stored in each BTreeBlock, etc. You can't set those directly, but you can set the "blockSize" and also the size of a key, etc. Those parameters are in the class `Globals`, and can be modified to constructs trees of different fanouts.

**Important Note: The B+-Tree code isn't fully debugged and there may be corner cases where it fails. Let me know if you see unexpected behavior.**

### How to Use the Files

The directory also contains two other files:
* `create_sample_databases.py`: Creates a sample database with 2 relations and 2 indexes.
* `testing.py`: Shows the execution of some simple tasks using the sample data. 

The simplest way you can run this is by just doing: `python testing.py`
That will run all the code in the `testing.py` file.

A better option is to do: `python -i testing.py`. This will execute all the code in `testing.py` file and then it will open a Python shell. In that shell, you can start doing more operations (e.g., you can play with the index to add/delete tuples, etc.)

### Your Task

Your task is to finish a few of the unfinished pieces in the `btree.py` and `queryprocessing.py` files.
* Function `redistributeWithBlock(self, otherBlock)` in `btree.py`: The delete code does not handle the case where an underfull node borrows entries from one of its siblings.
You are to implement this function.
* Function `SortMergeJoin.get_next()` in `queryprocessing.py`: Your task is to implement the SortMergeJoin algorithm
* Function `GroupByAggregate.get_next()` in `queryprocessing.py`: The GroupByAggregate only handles the case when there is no group by. Your task is to handle that case.
* Function `HashJoin.get_next()` in `queryprocessing.py`: The inner join works, but the two types of outer join are not currently handled. Your task is to implement those two.

You shouldn't have to modify any other code besides those functions.

### Submission
You should submit modified `btree.py` and `queryprocessing.py` files. We will test those in a (partially) automated fashion, using a set of test cases.
We will provide additional information (including a sample dataset) in a few days.

Note: Make sure to handle extreme cases (e.g., no input tuples for the joins, a single group for group by aggregate, etc.)
