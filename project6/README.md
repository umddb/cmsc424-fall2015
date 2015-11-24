## Project 6: Transactions, CMSC424, Fall 2015

*The assignment is to be done by yourself.*

### Overview

In this project, you will modify a very simple database system that we have written to illustrate some of the transactions functionality
The database system is written in Python and attempts to simulate how a database system would work, including what blocks it would read from disk, etc.

**NOTE**: This codebase is different from the Project 4 codebase, with simpler relation schema and querying interface, but a more complex Buffer Pool Manager, and file management.
See some details below.

**Another Important Note:** We have taken a few shortcuts in this code to simplify it, which unfortunately means that there may be important synchronization failures we missed. Let me know if you see any unexpected behavior.

#### `disk_relations.py` 
A `Relation` is backed by a file in the file system, i.e., all the data in the relation is written to a file and is read from a file. If a Relation is created with a non-existing fileName, then a new Relation is created with pre-populated 100 tuples. The file is an ASCII file -- the reading and writing is using `json` module. 
You can open the file and see the contents of it. 

`disk_relations.py` also contains a LRU Buffer Pool Implementation, with a fixed size Buffer Pool. 

#### `transactions.py`

This contains the implementaion of the Lock Table, a Log Manager, and a few Transactions. *More details to be posted.*

#### `testing.py`

This contains some code for testing. You should be able to run: `python testing.py` to get started. Note that the first time you run it, it will create the
two files `relation1` and `logfile`, but after you kill it, the logfile will be inconsistent (we never write out CHECKPOINT
records in normal course). So the second time you run it, it will error out since the restartRecovery code is not implemented. So if you want to work on the other
two tasks, you should remove those two files every time.

Currently the only way to stop testing.py is through killing it through Ctrl-C. If that doesn't work, try stopping it (Ctrl-Z), and then killing it using `kill %`.

### Your Task

Your task is to finish a few of the unfinished pieces in the two files (1 point for the first one, and 2 points each for the latter two).
* Implementing IX Locks in `transactions.py`: Currently the code supports S, X, and IS locks. So if a transaction needs to lock a tuple in the X mode, the entire relation 
is locked. This
is of course not ideal and we would prefer to use IX locks (on the relation) to speed up concurrency. The code for this will largely mirror the code for IS. You will 
have to change the `getXLockTuple()` function and also the `compatibility_list` appropriately. 
* Function `detectDeadlocks()` in `transactions.py`: The deadlock detection code is called once every few seconds. You should analyze the `waits-for` graph and figure out 
if there are any deadlocks and decide which transactions to abort to resolve it. This code only needs to call `signalAbortTransaction` on the appropriate transaction -- our
code handles the actual abort.
* Function `restartRecovery()` in `transaction.py`: This function is called if the log file indicates an inconsistecy (specifically if the logfile does not end with an empty CHECKPOINT record). If that's the case, then you must analyze the logfile and do a recovery on that.

### Submission
You should submit modified `transactions.py` file. We will test your functionality in a (partially) automated fashion, using a set of test cases.
We will provide additional information (including a sample dataset) later.

You shouldn't need to change anything in `disk_relations.py`. If you see any need for that, let us know and we can modify and commit changes to that file
if we decide that is needed.
