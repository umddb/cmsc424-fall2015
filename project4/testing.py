import math
from disk_relations import *
from btree import *
from queryprocessing import *
from create_sample_databases import *

# Create a sample database
db1 = createDatabase1("univ")
db1.getRelation("instructor").printTuples()
db1.getRelation("department").printTuples()
db1.getIndex("instructor", "name").printTree()
db1.getIndex("instructor", "dept_name").printTree()

# Let's do a search -- we will print out the Blocks that were accessed during the search
# by setting Globals.printBlockAccesses
def searchExample():
	print "================================================================================"
	print "Searching for all instructors with names starting with M to R"
	Globals.printBlockAccesses = True
	results = db1.getIndex("instructor", "name").searchByRange("M", "S")
	if results is not None and len(results) != 0:
		print "Results: " + " ".join([str(ptr.getTuple()) for ptr in results])
	else:
		print "No results found"
	Globals.printBlockAccesses = False

# Find a record by key and delete the first tuple in the results -- print out the resulting trees
def deleteFromTree(deleteKey):
	print "================================================================================"
	print "Deleting the entry for key " + deleteKey
	index = db1.getIndex("instructor", "name")
	results = index.searchByKey(deleteKey)
	db1.getRelation("instructor").deleteTuple(results[0])
	# The BTrees should have been adjusted automatically
	index.printTree()
	db1.getIndex("instructor", "dept_name").printTree()

# Set up some simple operators manually: Nested Loops Join
def query1():
	scan1 = SequentialScan(db1.getRelation("instructor"))
	scan2 = SequentialScan(db1.getRelation("department"))
	nl_join = NestedLoopsJoin(scan1, scan2, "dept_name", "dept_name")
	print "==================== Executing Nested Loops Join ================"
	nl_join.init()
	for t in nl_join.get_next():
		print "---> " + str(t)

# Set up some simple operators manually: Aggregate
def query2():
	scan1 = SequentialScan(db1.getRelation("instructor"))
	aggr = GroupByAggregate(scan1, "salary", GroupByAggregate.SUM)
	print "==================== Executing An Aggregate Query ================"
	aggr.init()
	for t in aggr.get_next():
		print "---> " + str(t)

# Set up some simple operators manually: Inner Hash Join
def query3():
	scan1 = SequentialScan(db1.getRelation("instructor"))
	scan2 = SequentialScan(db1.getRelation("department"))
	hash_join = HashJoin(scan1, scan2, "dept_name", "dept_name", HashJoin.INNER_JOIN)
	print "==================== Executing An Inner Hash Join ================"
	hash_join.init()
	for t in hash_join.get_next():
		print "---> " + str(t)

# Example of a search can be found in searchExample() above
searchExample()

# A delete that works
deleteFromTree("Srinivasan")

# The following three operators work
query1()
query2()
query3()

##################################
### These next set of operators throw an error
deleteFromTree("Einstein")

# Trying to execute a sort merge join
def query4():
	scan1 = SequentialScan(db1.getRelation("instructor"))
	scan2 = SequentialScan(db1.getRelation("department"))
	sm_join = SortMergeJoin(scan1, scan2, "dept_name", "dept_name")
	print "==================== Executing Sort Merge Join ================"
	sm_join.init()
	for t in sm_join.get_next():
		print "---> " + str(t)

# Trying to execute a group by aggregate
def query5():
	scan1 = SequentialScan(db1.getRelation("instructor"))
	aggr = GroupByAggregate(scan1, "salary", GroupByAggregate.SUM, "dept_name")
	print "==================== Executing A Groupby Aggregate Query ================"
	aggr.init()
	for t in aggr.get_next():
		print "---> " + str(t)

# Left outer hash join
def query6():
	scan1 = SequentialScan(db1.getRelation("instructor"))
	scan2 = SequentialScan(db1.getRelation("department"))
	hash_join = HashJoin(scan1, scan2, "dept_name", "dept_name", HashJoin.LEFT_OUTER_JOIN)
	print "==================== Executing A Left Outer Hash Join ================"
	hash_join.init()
	for t in hash_join.get_next():
		print "---> " + str(t)

# Right outer hash join
def query7():
	scan1 = SequentialScan(db1.getRelation("instructor"))
	scan2 = SequentialScan(db1.getRelation("department"))
	hash_join = HashJoin(scan1, scan2, "dept_name", "dept_name", HashJoin.RIGHT_OUTER_JOIN)
	print "==================== Executing A Right Outer Hash Join ================"
	hash_join.init()
	for t in hash_join.get_next():
		print "---> " + str(t)

query4()
query5()
query6()
query7()
