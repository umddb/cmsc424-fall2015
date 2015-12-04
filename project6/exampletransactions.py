from disk_relations import *
from transactions import *
import time

#####################################################################################################
####
#### A Few Pre-Defined Transactions
####
#####################################################################################################

# Transaction 1 adds 10 to the value of A given a primary id
def Transaction1(relation, primary_id, sleeptime = 10):
	tstate = TransactionState()
	if tstate.getXLockTuple(relation, primary_id):
		time.sleep(sleeptime)

		tup = relation.getTuple(primary_id)
		oldval = tup.getAttribute("A")
		newval = str(int(oldval) + 10)

		LogManager.createUpdateLogRecord(tstate.transaction_id, relation.fileName, primary_id, "A", oldval, newval)
		tup.setAttribute("A", newval)

		time.sleep(sleeptime)

		tstate.commitTransaction()

# Transaction 2 doubles the value of A for the given tuple ID
def Transaction2(relation, primary_id, sleeptime = 10):
	tstate = TransactionState()
	if tstate.getXLockTuple(relation, primary_id):
		time.sleep(sleeptime)

		tup = relation.getTuple(primary_id)
		oldval = tup.getAttribute("A")
		newval = str(int(oldval) * 2)

		LogManager.createUpdateLogRecord(tstate.transaction_id, relation.fileName, primary_id, "A", oldval, newval)
		tup.setAttribute("A", newval)

		time.sleep(sleeptime)

		tstate.commitTransaction()

# Transaction 3 moves 10 from one tuple to another
def Transaction3(relation, primary_id1, primary_id2, sleeptime = 10):
	tstate = TransactionState()
	if tstate.getXLockTuple(relation, primary_id1): 
		time.sleep(sleeptime)

		if tstate.getXLockTuple(relation, primary_id2):
			tup1 = relation.getTuple(primary_id1)
			tup2 = relation.getTuple(primary_id2)
			oldval1 = tup1.getAttribute("A")
			oldval2 = tup2.getAttribute("A")
			newval1 = str(int(oldval1) - 10)
			newval2 = str(int(oldval2) + 10)
			LogManager.createUpdateLogRecord(tstate.transaction_id, relation.fileName, primary_id1, "A", oldval1, newval1)
			LogManager.createUpdateLogRecord(tstate.transaction_id, relation.fileName, primary_id2, "A", oldval2, newval2)
			tup1.setAttribute("A", newval1)
			tup2.setAttribute("A", newval2)
			tstate.commitTransaction()

# Transaction 4 moves 20% from one tuple to another
def Transaction4(relation, primary_id1, primary_id2, sleeptime = 10, abort = False):
	tstate = TransactionState()
	if tstate.getXLockTuple(relation, primary_id1): 
		time.sleep(sleeptime)

		if tstate.getXLockTuple(relation, primary_id2):
			tup1 = relation.getTuple(primary_id1)
			tup2 = relation.getTuple(primary_id2)
			oldval1 = tup1.getAttribute("A")
			oldval2 = tup2.getAttribute("A")
			movevalue = int(oldval1)/5 + 1
			newval1 = str(int(oldval1) - movevalue)
			newval2 = str(int(oldval2) + movevalue)
			LogManager.createUpdateLogRecord(tstate.transaction_id, relation.fileName, primary_id1, "A", oldval1, newval1)
			LogManager.createUpdateLogRecord(tstate.transaction_id, relation.fileName, primary_id2, "A", oldval2, newval2)
			tup1.setAttribute("A", newval1)
			tup2.setAttribute("A", newval2)

			time.sleep(sleeptime)

			if not abort:
				tstate.commitTransaction()
			else:
				tstate.abortTransaction()

# Transaction 5 is similar to 3 with some differences in when things are written out
def Transaction5(relation, primary_id1, primary_id2, sleeptime = 10):
	tstate = TransactionState()
	if tstate.getXLockTuple(relation, primary_id1): 
		tup1 = relation.getTuple(primary_id1)
		oldval1 = tup1.getAttribute("A")
		newval1 = str(int(oldval1) - 10)
		LogManager.createUpdateLogRecord(tstate.transaction_id, relation.fileName, primary_id1, "A", oldval1, newval1)
		tup1.setAttribute("A", newval1)

		time.sleep(sleeptime)

		if tstate.getXLockTuple(relation, primary_id2):
			tup2 = relation.getTuple(primary_id2)
			oldval2 = tup2.getAttribute("A")
			newval2 = str(int(oldval2) + 10)
			LogManager.createUpdateLogRecord(tstate.transaction_id, relation.fileName, primary_id2, "A", oldval2, newval2)
			tup2.setAttribute("A", newval2)
			tstate.commitTransaction()

