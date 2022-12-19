from aocd import get_data
import re

class Valve:
	def __init__(self, id, rate, neighbours) -> None:
		self.id = id
		self.rate = rate
		self.neighbours = neighbours
	
	def update_neighbours(self, valves):
		new_neigbours = []
		for neigbour in self.neighbours:
			new_neigbours.append(valves[neigbour])
		self.neighbours = new_neigbours
	
	def __repr__(self) -> str:
		return self.id
	
class Worker:
	def __init__(self, _type, pressure, time, valve) -> None:
		self._type = _type 
		self.re_pressure = pressure
		self.time = time
		self.valve = valve

	@property	
	def neighbours(self):
		return self.valve.neighbours

	def __repr__(self) -> str:
		return self._type
		

def parse(raw):
	valves = {}
	for line in raw:
		id, rate, raw_neighbours = re.search(r'([A-Z]{2}).*rate=(\d+).*valves? (.*)', line).groups()
		valves[id] = Valve(id, int(rate), raw_neighbours.split(', ') if ',' in raw_neighbours else [raw_neighbours])
	for valve in valves.values():
		valve.update_neighbours(valves)
	return valves

def is_pressure_promising(valves, max_pressure, w_1, w_2, activated):
	t1, t2 = w_1.time, w_2.time
	pos_pre = w_1.re_pressure + w_2.re_pressure
	valves_left = sorted(set(valves.values()) - {valves[id] for id in activated}, key=lambda x: x.rate)
	for _ in range(len(valves_left)):
		if t1 > t2:
			t1 -= 2	
			if t1 > 0:
				pos_pre += valves_left.pop().rate * t1	
		else:
			t2 -= 2
			if t2 > 0:
				pos_pre += valves_left.pop().rate * t2
		if t1 + t2 <= 0:
			break
	return pos_pre > max_pressure	

def steps_worker(queue, worker, other, activated):
	pref = []
	for neighbour in worker.neighbours:
		if neighbour.id not in activated and neighbour.rate != 0:
			new_activated = activated.union({neighbour.id})
			pref.append([Worker(worker._type, worker.re_pressure + neighbour.rate*(worker.time - 2), worker.time - 2, neighbour), other, new_activated])
		queue.append([Worker(worker._type, worker.re_pressure, worker.time - 1, neighbour), other, activated])
	queue.extend(pref)

def minimal_pressure(valves, time):
	queue = [[Worker("person", 0, time-4, valves["AA"]), Worker("elephant", 0, time-4, valves["AA"]), set()]]
	max_pressure = 0
	while len(queue) > 0:
		w_1, w_2, activated = queue.pop()
		if not is_pressure_promising(valves, max_pressure, w_1, w_2, activated): continue

		if (w_1.time - 2 <= 0 and w_2.time - 2 <= 0) or len(activated) == len(valves):
			max_pressure = max(max_pressure, w_1.re_pressure + w_2.re_pressure)
			print(max_pressure)
		elif (w_1.time - 2) <= 0:
			w_1.time = 0
			steps_worker(queue, w_2, w_1, activated)
		elif (w_2.time - 2) <= 0:
			w_2.time = 0
			steps_worker(queue, w_1, w_2, activated)
		else:
			for neighbour in w_1.neighbours:
				if neighbour.id not in activated and neighbour.rate != 0:
					new_activated = activated.union({neighbour.id})
					steps_worker(queue, w_2, Worker(w_1._type, w_1.re_pressure + neighbour.rate*(w_1.time-2), w_1.time - 2, neighbour), new_activated)
				steps_worker(queue, w_2, Worker(w_1._type, w_1.re_pressure, w_1.time - 1, neighbour), activated)
	return max_pressure


if __name__ == '__main__':
	raw = get_data(day=16, year=2022).splitlines()
	valves = parse(raw)
	print("Part 2: ", minimal_pressure(valves, 30))