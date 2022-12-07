import sys

class Dir:
	def __init__(self, name, parent) -> None:
		self.name = name 
		self.files = []
		self.dirs = {'..': parent}
		self.size = 0
		self.parent = parent

	def ls(self):
		return list(self.dirs.keys()) + self.files
	
	def mkfile(self, file, size):
		self.files.append((file, size))
		self.__update_size(size)
	def mkdir(self, dir):
		self.dirs[dir.name] = dir
	def __update_size(self, size):
		self.size += size
		if self.parent:
			self.parent.__update_size(size)

def make_fs(data):
	fs = Dir('/', None)
	curr = fs
	for inst in data:
		tmp = inst.split(' ')
		if tmp[0] == "$":
			if len(tmp) == 3:
				i_1, i_2 = tmp[1], tmp[2]
			else:
				i_1, i_2 = tmp[1], None
			if i_1 == "cd":
				curr = curr.dirs[i_2]
			elif i_1 == "ls":
				print(curr.ls())
		else:	
			i_1, i_2 = tmp
			if i_1 == "dir":
				curr.dirs[i_2] = Dir(i_2, curr)
			elif i_1.isnumeric():
				curr.mkfile(i_2, int(i_1))
	return fs

def p2(dir, pot):
	if dir.size >= 8381165 and dir.size < pot.size:
		pot = dir
	for n, d in dir.dirs.items():
		if n == '..': continue
		pot = p2(d, pot)
	return pot

if __name__ == '__main__':
	input = open(sys.argv[1] if len(sys.argv) > 1 else 'input.in').read().split('\n')[1:-1]
	fs = make_fs(input)
	print("Part 2: ", p2(fs, fs).size)

