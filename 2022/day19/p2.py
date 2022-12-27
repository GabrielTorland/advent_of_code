from aocd import get_data
import re
import copy
from collections import defaultdict
import concurrent.futures
import time
from functools import reduce
from operator import mul

class Cost:
	def __init__(self, ore, clay, obsidian):
		self.materials = defaultdict(int)
		self.materials["ore"] = ore
		self.materials["clay"] = clay
		self.materials["obsidian"] = obsidian
class Earn(Cost):
	def __init__(self, ore, clay, obsidian, geode):
		super().__init__(ore, clay, obsidian)
		self.materials["geode"] = geode

class Robot:
	def __init__(self, type, cost, earn):
		self.type = type
		self.cost = cost
		self.earn = earn
		
class Blueprint:
	def __init__(self, id, ore_robot, clay_robot, obsidian_robot, geode_robot):
		self.id = id
		self.robots = {"ore" : ore_robot, "clay" : clay_robot, "obsidian": obsidian_robot, "geode" : geode_robot}
		self.max_costs = defaultdict(int)
		for robot in [ore_robot, clay_robot, obsidian_robot, geode_robot]:
			for material, cost in robot.cost.materials.items():
				self.max_costs[material] = max(self.max_costs[material], cost)

def cost_equal(a, b):
	for material, cost in a.materials.items():
		if cost > b[material]: return False
	return True
class Inventory:
	def __init__(self, time, ore, clay, obsidian, geode, blueprint):
		self.time = time 
		self.ore = ore
		self.clay = clay
		self.obsidian = obsidian
		self.geode = geode
		self.robots = defaultdict(int)
		self.blueprint = blueprint

	def get_children(self):
		if cost_equal(self.blueprint.robots["geode"].cost, self.robots):
			child = copy.deepcopy(self)
			child.geode += child.robots["geode"]*child.time + (child.time)*(child.time-1)//2
			child.robots["geode"] += child.time
			child.time = 0	
			return [child]
		children = []
		for robot in self.blueprint.robots.values():
			if robot.type != "geode" and not is_child_promising(self.blueprint, self, robot): continue
			child = copy.deepcopy(self)
			while child.time != 0:
				if child.buy(robot):
					child.earn()
					child.robots[robot.type] += 1
					child.time -= 1
					children.append(child)
					break
				else:
					child.earn()
					child.time -= 1
		return children
	
	def earn(self):
		for robot, count in self.robots.items():
			self.ore += self.blueprint.robots[robot].earn.materials["ore"]*count 
			self.clay += self.blueprint.robots[robot].earn.materials["clay"]*count
			self.obsidian += self.blueprint.robots[robot].earn.materials["obsidian"]*count 
			self.geode += self.blueprint.robots[robot].earn.materials["geode"]*count 

	def buy(self, robot):
		if self.ore >= robot.cost.materials["ore"] and self.clay >= robot.cost.materials["clay"] and self.obsidian >= robot.cost.materials["obsidian"]:
			self.ore -= robot.cost.materials["ore"]
			self.clay -= robot.cost.materials["clay"]
			self.obsidian -= robot.cost.materials["obsidian"]
			return True
		return False
	
	def __hash__(self) -> int:
		return hash((self.time, self.ore, self.clay, self.obsidian, self.geode, self.robots["ore"], self.robots["clay"], self.robots["obsidian"], self.robots["geode"]))
	def __eq__(self, other: object) -> bool:
		return self.time == other.time and self.ore == other.ore and self.clay == other.clay and self.obsidian == other.obsidian and self.geode == other.geode and self.robots["ore"] == other.robots["ore"] and self.robots["clay"] == other.robots["clay"] and self.robots["obsidian"] == other.robots["obsidian"] and self.robots["geode"] == other.robots["geode"]

def parse(raw):
	blueprints = []
	for line in raw.splitlines():
		raw_blueprint = re.search(r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.", line).groups()
		blueprints.append(Blueprint(int(raw_blueprint[0]),
		 Robot("ore", Cost(int(raw_blueprint[1]), 0, 0), Earn(1, 0, 0, 0)),
		 Robot("clay", Cost(int(raw_blueprint[2]), 0, 0), Earn(0, 1, 0, 0)),
		  Robot("obsidian", Cost(int(raw_blueprint[3]), int(raw_blueprint[4]), 0), Earn(0, 0, 1, 0)),
		   Robot("geode", Cost(int(raw_blueprint[5]), 0, int(raw_blueprint[6])), Earn(0, 0, 0, 1))))
	return blueprints

def is_child_promising(blueprint, child, robot):
	if (child.robots[robot.type] + 1) > blueprint.max_costs[robot.type]:
			return False
	return True
 
def is_inventory_promising(inventory, max_geodes):
	potential_geodes = inventory.geode + inventory.robots["geode"]*inventory.time + (inventory.time)*(inventory.time-1)//2
	return potential_geodes >= max_geodes 

def max_geodes(blueprint, time=32):
	stack = [Inventory(time, 0, 0, 0, 0, blueprint)]
	stack[0].robots["ore"] += 1
	max_geodes = 0
	while len(stack) != 0:
		inventory = stack.pop()
		if not is_inventory_promising(inventory, max_geodes): continue
		max_geodes = max(max_geodes, inventory.geode)
		if inventory.time == 0: continue
		stack += inventory.get_children()
	return max_geodes
		
if __name__ == "__main__":
	raw = get_data(day=19, year=2022)
	blueprints = parse(raw)
	quality_levels = []
	start = time.time()
	with concurrent.futures.ProcessPoolExecutor() as executor:
		for max_geodes in executor.map(max_geodes, blueprints[:3]):
			quality_levels.append(max_geodes)
	print("Duration: ", (time.time() - start)/60, " minutes") # 6.186095237731934  minutes
	print("Part 2: ", reduce(mul, quality_levels)) # 3003