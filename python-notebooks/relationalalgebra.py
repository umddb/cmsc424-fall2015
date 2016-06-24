from itertools import chain, combinations

# Encodes a predicate to be evaluated against a single tuple
# We allow predicates of the form: attr OP constant, where OP can be ==, >=, <=, !=
class UnaryPredicate: 
	def __init__(self, attrname, op, const):
		self.op = op
		self.const = const
		self.attrname = attrname
	def evaluate(self, t):
		if self.op == '==':
			return t.getAttribute(self.attrname) == self.const
		if self.op == '>=':
			return t.getAttribute(self.attrname) >= self.const
		if self.op == '<=':
			return t.getAttribute(self.attrname) <= self.const
		if self.op == '!=':
			return t.getAttribute(self.attrname) != self.const
		raise ValueError("Unknown operator")

# Binary predicates are similar to above, but both their arguments are tuple attributes
# We allow predicates of the form: attr1 OP attr2, where OP can be ==, >=, <=, !=
# We allow the binary predicate to take two tuples as input or one tuple
class BinaryPredicate: 
	def __init__(self, attrname1, op, attrname2):
		self.op = op
		self.attrname1 = attrname1
		self.attrname2 = attrname2
	def evaluateUnary(self, t):
		if self.op == '==':
			return t.getAttribute(self.attrname1) == t.getAttribute(self.attrname2)
		if self.op == '>=':
			return t.getAttribute(self.attrname1) >= t.getAttribute(self.attrname2)
		if self.op == '<=':
			return t.getAttribute(self.attrname1) <= t.getAttribute(self.attrname2)
		if self.op == '!=':
			return t.getAttribute(self.attrname1) != t.getAttribute(self.attrname2)
		raise ValueError("Unknown operator")
	def evaluateBinary(self, t1, t2):
		if self.op == '==':
			return t1.getAttribute(self.attrname1) == t2.getAttribute(self.attrname2)
		if self.op == '>=':
			return t1.getAttribute(self.attrname1) >= t2.getAttribute(self.attrname2)
		if self.op == '<=':
			return t1.getAttribute(self.attrname1) <= t2.getAttribute(self.attrname2)
		if self.op == '!=':
			return t1.getAttribute(self.attrname1) != t2.getAttribute(self.attrname2)
		raise ValueError("Unknown operator")

# A simple Tuple class -- with the only main functionality of retrieving and setting the 
# attribute value through a brute-force search
class RelationTuple: 
	def __init__(self, schema, t):
		self.t = t
		self.schema = schema
	def __str__(self):
		return str(self.t)
	def getAttribute(self, attribute):
		for i,attr in enumerate(self.schema):
			if attr == attribute:
				return self.t[i] 
		raise ValueError("Should not reach here")

class Relation: 
	def __init__(self, name, schema):
		self.tuples = list()
		self.name = name
		self.schema = schema 
	def add(self, t):
		self.tuples.append(t)
	def printtuples(self):
		for t in self.tuples:
			print t
	def prettyprint(self):
		print "=========================="
		print "	".join(str(x) for x in self.schema)
		for t in self.tuples:
			print "	".join(str(x) for x in t.t)

r = Relation('r', ['A', 'B', 'C'])
r.add(RelationTuple(r.schema, [1, 2, 3]))
r.add(RelationTuple(r.schema, [2, 2, 3]))
r.add(RelationTuple(r.schema, [2, 2, 4]))
r.prettyprint()

s = Relation('s', ['C', 'D'])
s.add(RelationTuple(s.schema, [3, 4]))
s.add(RelationTuple(s.schema, [3, 5]))
s.add(RelationTuple(s.schema, [5, 5]))
s.prettyprint()

# A select (sigma) operation creates a new relation with only those tuples that satisfy the condition
def sigma(r, predicate):
	# Result relation will have the same schema
	result = Relation("", r.schema)
	for t in r.tuples:
		if predicate.evaluate(t):
			result.add(t) # We assume tuples are immutable here, otherwise a copy is warranted
	return result

pred1 = UnaryPredicate('A', '==', 1)
r1 = sigma(r, pred1)
r1.prettyprint()


# A project (pi) operation creates a new relation with only those tuples that satisfy the condition
def pi(r, attrlist):
	# Result relation will have the schema attrlist
	result = Relation("", attrlist)
	for t in r.tuples:
		newt = RelationTuple(result.schema, [t.getAttribute(attr) for attr in attrlist])
		result.add(newt) 
	return result
r2 = pi(r, ['A', 'B'])
r2.prettyprint()

# A cartesian (cross) product operation creates a new relation by pairing up every tuple in one relation with every tuple in another relation
def cartesian(r1, r2):
	# Result relation will have attributes from both the relations
	# To disambiguate, we will append the relation name to the attributes
	result = Relation("", [r1.name + "." + x for x in r1.schema] + [r2.name + "." + x for x in r2.schema])
	for t1 in r1.tuples:
		for t2 in r2.tuples:
			newt = RelationTuple(result.schema, t1.t + t2.t)
			result.add(newt) 
	return result

r3 = cartesian(r, s)
r3.prettyprint()

# A join is a cartesian product followed by a predicate
def join(r1, r2, predicate):
	# Result relation will have attributes from both the relations
	# To disambiguate, we will append the relation name to the attributes
	result = Relation("", [r1.name + "." + x for x in r1.schema] + [r2.name + "." + x for x in r2.schema])
	for t1 in r1.tuples:
		for t2 in r2.tuples:
			newt = RelationTuple(result.schema, t1.t + t2.t)
			if predicate.evaluateUnary(newt):
				result.add(newt) 
	return result

r4 = join(r, s, BinaryPredicate("r.C", "==", "s.C"))
r4.prettyprint()

# A full outer-join requires finding the tuples in both relations that don't have matches
# The below is the naive and highly inefficient implementation
# We will see better implementations when we discuss "query processing"
FULLOUTERJOIN = 1
LEFTOUTERJOIN = 2
RIGHTOUTERJOIN = 3
def fullouterjoin(r1, r2, predicate, outerjointype):
	# Result relation will have attributes from both the relations
	# To disambiguate, we will append the relation name to the attributes
	result = Relation("", [r1.name + "." + x for x in r1.schema] + [r2.name + "." + x for x in r2.schema])

	# First add the join results as above
	for t1 in r1.tuples:
		for t2 in r2.tuples:
			newt = RelationTuple(result.schema, t1.t + t2.t)
			if predicate.evaluateUnary(newt):
				result.add(newt) 

	# Now go over one relation and identify tuples that don't have a match
	for t1 in r1.tuples:
		match = False
		for t2 in r2.tuples:
			newt = RelationTuple(result.schema, t1.t + t2.t)
			if predicate.evaluateUnary(newt):
				match = True
				break
		if not match: 
			newt = RelationTuple(result.schema, t1.t + ["null" for x in r2.schema])
			result.add(newt)

	# Do the same for the other relation
	for t2 in r2.tuples:
		match = False
		for t1 in r1.tuples:
			newt = RelationTuple(result.schema, t1.t + t2.t)
			if predicate.evaluateUnary(newt):
				match = True
				break
		if not match: 
			newt = RelationTuple(result.schema, ["null" for x in r1.schema] + t2.t)
			result.add(newt)
	return result

r4 = fullouterjoin(r, s, BinaryPredicate("r.C", "==", "s.C"))
r4.prettyprint()
