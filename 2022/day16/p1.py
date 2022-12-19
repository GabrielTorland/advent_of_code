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
	def __init__(self, _type, pressure, time, valve, activated) -> None:
		self._type = _type 
		self.re_pressure = pressure
		self.time = time
		self.valve = valve
		self.activated = activated

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

def is_pressure_promising(valves, max_pressure, you):
	t = you.time 
	pos_pre = you.re_pressure 
	for valve in sorted(set(valves.values()) - {valves[id] for id in you.activated}, key=lambda x: x.rate, reverse=True):
		t -= 2
		if t <= 0: break
		pos_pre += valve.rate * t
	return pos_pre > max_pressure

def minimal_pressure(valves, time):
	queue = [Worker("person", 0, time, valves["AA"], set())]
	max_pressure = 0
	while len(queue) > 0:
		you = queue.pop()
		if you.time - 2 < 0:
			max_pressure = max(max_pressure, you.re_pressure)
			continue
		if not is_pressure_promising(valves, max_pressure, you): 
			continue
		for neighbour in you.neighbours:
			if neighbour.id not in you.activated and neighbour.rate != 0:
				new_acticated = you.activated.union({neighbour.id})
				queue.append(Worker("person", you.re_pressure + neighbour.rate*(you.time-2), you.time - 2, neighbour, new_acticated))
			
			queue.append(Worker("person", you.re_pressure, you.time - 1, neighbour, you.activated))

	return max_pressure

if __name__ == '__main__':
	raw = get_data(day=16, year=2022).splitlines()
	valves = parse(raw)
	print("Part 1: ", minimal_pressure(valves, 30))