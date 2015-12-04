from disk_relations import *
from transactions import *
import time
from exampletransactions import *
import sys
import subprocess

if len(sys.argv) != 4:
	print "Need to specify the relation name, logfile to use and which test to run"
	os._exit(1)

if sys.argv[1] in ['test1-deadlocks', 'test2-deadlocks']:
	bpool = BufferPool()
	r = Relation(sys.argv[2])
	LogManager.setAndAnalyzeLogFile(sys.argv[3])

	if sys.argv[1] == 'test1-deadlocks':
		t = threading.Thread(target=Transaction3, args=(r, "0", "10"))
		t.start()
		t = threading.Thread(target=Transaction3, args=(r, "10", "20"))
		t.start()
		t = threading.Thread(target=Transaction3, args=(r, "20", "0"))
		t.start()
	elif sys.argv[1] == 'test2-deadlocks':
		t = threading.Thread(target=Transaction3, args=(r, "0", "10"))
		t.start()
		t = threading.Thread(target=Transaction3, args=(r, "10", "0"))
		t.start()
		t = threading.Thread(target=Transaction3, args=(r, "20", "30"))
		t.start()
		t = threading.Thread(target=Transaction3, args=(r, "30", "20"))
		t.start()

	time.sleep(5)
	print "Calling deadlock detection code..."
	print "Need to abort transactions: " + str(LockTable.detectDeadlocksAndChooseTransactionsToAbort())

	if sys.argv[1] == 'test1-deadlocks':
		print "Answer should be either: T1, or T2, or T3"
	elif sys.argv[1] == 'test2-deadlocks':
		print "Answer should contain one of T1 and T2, and one of T3 and T4"
	os._exit(0)
elif sys.argv[1] == 'test3-recovery':
	if not os.path.isfile(sys.argv[2]) or not os.path.isfile(sys.argv[3]):
		print "Provided logfile or relationfile does not exist.. can't test recovery code"
	else:
		bpool = BufferPool()
		r = Relation(sys.argv[2])
		print "Starting to analyze the logfile " + sys.argv[3]
		LogManager.setAndAnalyzeLogFile(sys.argv[3])
		print "Finished calling restart recovery code... the logfile {} should now end with a CHECKPOINT record and the relation file {} should be in a consistent state (compare with provided answer)".format(sys.argv[3], sys.argv[2])
elif sys.argv[1] == 'generate-tests':
	if os.path.isfile(sys.argv[2]) or os.path.isfile(sys.argv[3]):
		print "For generating the tests, new files should be provided..."
	else:
		bpool = BufferPool()
		r = Relation(sys.argv[2])
		LogManager.setAndAnalyzeLogFile(sys.argv[3])
		for primary_id in ["0", "10", "20"]:
			t = threading.Thread(target=Transaction1, args=(r, primary_id, 50))
			t.start()
		t = threading.Thread(target=Transaction4, args=(r, "1", "11", 2, True))
		t.start()
		t = threading.Thread(target=Transaction4, args=(r, "3", "31", 2, True))
		t.start()
		t = threading.Thread(target=Transaction5, args=(r, "2", "21", 50))
		t.start()
		t = threading.Thread(target=Transaction5, args=(r, "4", "24", 50))
		t.start()
		time.sleep(20)
		os._exit(0)
