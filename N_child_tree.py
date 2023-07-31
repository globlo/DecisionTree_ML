
# Node of a linked list
class Node:
	def __init__(self, data = None):
		self.key = data
		self.child = []


def numberOfChildren( root, x):

	# initialize the numChildren as 0
	numChildren = 0

	if (root == None):
		return 0

	# Creating a queue and appending the root
	q = []
	q.append(root)

	while (len(q) > 0) :
		n = len(q)

		# If this node has children
		while (n > 0):

			# Dequeue an item from queue and
			# check if it is equal to x
			# If YES, then return number of children
			p = q[0]
			q.pop(0)
			if (p.key == x) :
				numChildren = numChildren + len(p.child)
				return numChildren
			
			i = 0
			
			# Enqueue all children of the dequeued item
			while ( i < len(p.child)):
				q.append(p.child[i])
				i = i + 1
			n = n - 1

	return numChildren

# Driver program

# Creating a generic tree
root = Node(20)
(root.child).append(Node(2))
(root.child).append(Node(34))
(root.child).append(Node(50))
(root.child).append(Node(60))
(root.child).append(Node(70))
(root.child[0].child).append(Node(15))
(root.child[0].child).append(Node(20))
(root.child[1].child).append(Node(30))
(root.child[2].child).append(Node(40))
(root.child[2].child).append(Node(100))
(root.child[2].child).append(Node(20))
(root.child[0].child[1].child).append(Node(25))
(root.child[0].child[1].child).append(Node(50))

# Node whose number of
# children is to be calculated
x = 50

# Function calling
print( numberOfChildren(root, x) )

# This code is contributed by Arnab Kundu
