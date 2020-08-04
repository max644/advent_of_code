class Node:
	def __init__(self, numbers):
		self.nbChildren = numbers[0]
		self.nbMetadata = numbers[1]
		self.size = 2
		self.nodes = []
		for childIdx in range(self.nbChildren):
			node = Node(numbers[self.size:])
			self.nodes.append(node)
			self.size += node.size
		self.metadata = numbers[self.size:self.size+self.nbMetadata]
		self.size += self.nbMetadata
		
	def metadataSum(self):
		return sum(self.metadata) + sum(node.metadataSum() for node in self.nodes)

	def metadataSum2(self):
		if len(self.nodes) > 0:
			return sum(self.nodes[idxMetadata-1].metadataSum2() for idxMetadata in self.metadata if idxMetadata <= len(self.nodes))
		else:
			return self.metadataSum()
		
if __name__ == "__main__":
	with open("8.txt", "r") as file:
		content = file.read()
		
	numbers = [int(x) for x in content.split()]
	
	root = Node(numbers)
	
	print root.metadataSum()
	print root.metadataSum2()