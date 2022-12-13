from aocd import get_data
import json
class Packet:
	def __init__(self, value):
		self.id = self.__create_tuple(value)
		self.value = value

	def __create_tuple(self, _value):
		value = _value.copy()
		for i, elem in enumerate(value):
			if isinstance(elem, list):
				value[i] = self.__create_tuple(elem)
		return tuple(value)

	def __hash__(self):
		return self.id

	def __comp_elems(self, a, b, out):
		if a == [[1], 4]:
			print()
		for i in range(min(len(a), len(b))):
			e1, e2 = a[i], b[i]
			# both elements are ints
			if isinstance(e1, int) and isinstance(e2, int):
				if e1 > e2: return 0 
				elif e1 < e2: return 1 
			# element 1 is an int and element 2 is a list
			elif isinstance(e1, int) and isinstance(e2, list): 
				state = self.__comp_elems([e1], e2, out)
				if not state: return 0 
				elif state == 1: return 1 
			# element 1 is a list and element 2 is an int
			elif isinstance(e1, list) and isinstance(e2, int): 
				state = self.__comp_elems(e1, [e2], out)
				if not state: return 0  
				elif state == 1: return 1 
			# both elements are lists
			elif isinstance(e1, list) and isinstance(e2, list): 
				state = self.__comp_elems(e1, e2, out)
				if not state: return 0 
				elif state == 1: return 1 
		if len(a) == len(b):
			return -1
		elif len(a) < len(b):
			return 1
		else:
			return 0
	def __eq__(self, other):
		if isinstance(other, Packet):
			return self.id == other.id
		else:
			return NotImplemented
	def __lt__(self, other):
		return self.__comp_elems(self.value, other.value, 1) == 1
	def __le__ (self, other):
		return self.__comp_elems(self.value, other.value, 1) in [1, -1]
	def __gt__(self, other):
		return self.__comp_elems(self.value, other.value, 0) == 0
	def __ge__(self, other):
		return self.__comp_elems(self.value, other.value, 0) in [0, -1]

if __name__ == '__main__':
	packets = [Packet(json.loads(elem)) for pair in get_data(day=13, year=2022).split("\n\n") for elem in pair.split('\n')] + [Packet([[2]]), Packet([[6]])]
	packets.sort()	
	print("Part 2: ", (packets.index(Packet([[2]])) + 1)*(packets.index(Packet([[6]])) + 1))