from disk_relations import *

# We will implement our operators using the iterator interface
# discussed in Section 12.7.2.1
class Operator:
	def init(self):
		return
	def get_next(self):
		return
	def close(self):
		return

# We will only support equality predicate for now
class Predicate:
	def __init__(self, attribute, value):
		self.attribute = attribute
		self.value = value
	def satisfiedBy(self, t):
		return t.getAttribute(self.attribute) == self.value

class SequentialScan(Operator):
	def __init__(self, relation, predicate = None):
		self.relation = relation
		self.predicate = predicate
	# Typically the init() here would open the appropriate file, etc. In our 
	# simple implementation, we don't need to do anything, especially when we
	# use "yield"
	def init(self):
		return

	# This is really simplified because of "yield", which allows us to return a value, 
	# and then continue where we left off when the next call comes
	def get_next(self):
		for i in range(0, len(self.relation.blocks)):
			b = self.relation.blocks[i]
			if Globals.printBlockAccesses:
				print "Retrieving " + str(b)
			for j in range(0, len(self.relation.blocks[i].tuples)):
				t = b.tuples[j]
				if t is not None and (self.predicate is None or self.predicate.satisfiedBy(t)):
					yield t
	# Typically you would close any open files etc.
	def close(self):
		return

# We will only support Equality joins
class NestedLoopsJoin(Operator):
	INNER_JOIN = 0
	LEFT_OUTER_JOIN = 1
	def __init__(self, left_child, right_child, left_attribute, right_attribute, jointype = INNER_JOIN):
		self.left_child = left_child
		self.right_child = right_child
		self.left_attribute = left_attribute
		self.right_attribute = right_attribute
		self.jointype = jointype

	# Call init() on the two children
	def init(self):
		self.left_child.init()
		self.right_child.init()

	# Again using "yield" greatly simplifies writing of this code -- otherwise we would have 
	# to keep track of current pointers etc
	def get_next(self):
		for l in self.left_child.get_next():
			foundAMatch = False
			for r in self.right_child.get_next():
				if l.getAttribute(self.left_attribute) == r.getAttribute(self.right_attribute):
					foundAMatch = True
					output = list(l.t)
					output.extend(list(r.t))
					yield Tuple(None, output)
			# If we are doing LEFT_OUTER_JOIN, we need to output a tuple if there is no match
			if self.jointype == NestedLoopsJoin.LEFT_OUTER_JOIN and not foundAMatch:
				output = list(l.t)
				for i in range(0, len(self.right_child.relation.schema)):
					output.append("NULL")
				yield Tuple(None, output)
			# NOTE: RIGHT_OUTER_JOIN is not easy to do with NestedLoopsJoin, so you would swap the children
			# if you wanted to do that

	# Typically you would close any open files etc.
	def close(self):
		return

# We will only support Equality joins
# Inner Hash Joins are very simple to implement, especially if you assume that the right relation fits in memory
# We start by loading the tuples from the right input into a hash table, and then for each tuple in the second
# input (left input) we look up matches
#
# You are supposed to implement the two outer hash join versions of this
class HashJoin(Operator):
	INNER_JOIN = 0
	LEFT_OUTER_JOIN = 1
	RIGHT_OUTER_JOIN = 1
	def __init__(self, left_child, right_child, left_attribute, right_attribute, jointype):
		self.left_child = left_child
		self.right_child = right_child
		self.left_attribute = left_attribute
		self.right_attribute = right_attribute
		self.jointype = jointype

	# Call init() on the two children
	def init(self):
		self.left_child.init()
		self.right_child.init()

	# We will use Python "dict" data structure as the hash table
	def get_next(self):
		if self.jointype == self.INNER_JOIN:
			# First, we load up all the tuples from the right input into the hash table
			hashtable = dict()
			for r in self.right_child.get_next():
				key = r.getAttribute(self.right_attribute)
				if key in hashtable:
					hashtable[r.getAttribute(self.right_attribute)].append(r)
				else: 
					hashtable[r.getAttribute(self.right_attribute)] = [r]
			# Then, for each tuple in the left input, we look for matches and output those
			# Using "yield" significantly simplifies this code
			for l in self.left_child.get_next():
				key = l.getAttribute(self.left_attribute)
				if key in hashtable:
					for r in hashtable[key]:
						output = list(l.t)
						output.extend(list(r.t))
						yield Tuple(None, output)

		elif self.jointype == self.LEFT_OUTER_JOIN:
			raise ValueError("Functionality to be implemented")
		elif self.jointype == self.RIGHT_OUTER_JOIN:
			raise ValueError("Functionality to be implemented")
		else:
			raise ValueError("This should not happen")

	# Typically you would close any open files, deallocate hash tables etc.
	def close(self):
		self.left_child.close()
		self.right_child.close()
		return

class GroupByAggregate(Operator):
	COUNT = 0
	SUM = 1
	MAX = 2
	MIN = 3
	@staticmethod
	def initial_value(aggregate_function):
		return (0, 0, None, None)[aggregate_function]
	@staticmethod
	def update_aggregate(aggregate_function, current_aggregate, new_value):
		if aggregate_function == GroupByAggregate.COUNT:
			return current_aggregate + 1
		elif aggregate_function == GroupByAggregate.SUM:
			return current_aggregate + int(new_value)
		elif aggregate_function == GroupByAggregate.MAX:
			if current_aggregate is None:
				return new_value
			else:
				return max(current_aggregate, new_value)
		elif aggregate_function == GroupByAggregate.MIN:
			if current_aggregate is None:
				return new_value
			else:
				return min(current_aggregate, new_value)
		else:
			raise ValueError("No such aggregate")

	def __init__(self, child, aggregate_attribute, aggregate_function, group_by_attribute = None):
		self.child = child
		self.group_by_attribute = group_by_attribute
		self.aggregate_attribute = aggregate_attribute
		# The following should be between 0 and 3, as interpreted above
		self.aggregate_function = aggregate_function

	def init(self):
		self.child.init()

	def get_next(self):
		if self.group_by_attribute is None:
			# We first use initial_value() to set up an appropriate initial value for the aggregate, e.g., 0 for COUNT and SUM
			aggr = GroupByAggregate.initial_value(self.aggregate_function)

			# Then, for each input tuple: we update the aggregate appropriately
			for t in self.child.get_next():
				aggr = GroupByAggregate.update_aggregate(self.aggregate_function, aggr, t.getAttribute(self.aggregate_attribute))

			# There is only one output here, but we must use "yield" since the "else" code needs to use "yield" (that code
			# may return multiple groups)
			yield aggr
		else:
			# for each different value "v" of the group by attribute, we should return a 2-tuple "(v, aggr_value)",
			# where aggr_value is the value of the aggregate for the group of tuples corresponding to "v"
			raise ValueError("Functionality to be implemented")

# You are supposed to implement this join operator
class SortMergeJoin(Operator):
	def __init__(self, left_child, right_child, left_attribute, right_attribute):
		self.left_child = left_child
		self.right_child = right_child
		self.left_attribute = left_attribute
		self.right_attribute = right_attribute

	# Call init() on the two children
	def init(self):
		self.left_child.init()
		self.right_child.init()

	# In your implementation, you can assume that the two inputs are small enough to fit into memory,
	# so there is no need to do external sort
	# You can load the two relations into arrays and use Python sort routines to sort them, and then merge
	# Make sure to use "yield" to simplify your code
	def get_next(self):
		raise ValueError("Functionality to be implemented")

	# Typically you would close any open files, deallocate hash tables etc.
	def close(self):
		self.left_child.close()
		self.right_child.close()
