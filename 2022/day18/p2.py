from aocd import get_data
import sys
import matplotlib.pyplot as plt
import matplotlib
import numpy as np



def lava(world, x, y, z) -> None:
	world[x][y][z] = 2
	if (x+1) < len(world) and world[x+1][y][z] == 0:
		lava(world, x+1, y, z)
	if (x-1) >= 0 and world[x-1][y][z] == 0:
		lava(world, x-1, y, z)
	if (y+1) < len(world[0]) and world[x][y+1][z] == 0:
		lava(world, x, y+1, z)
	if (y-1) >= 0 and world[x][y-1][z] == 0:
		lava(world, x, y-1, z)
	if (z+1) < len(world[0][0]) and world[x][y][z+1] == 0:
		lava(world, x, y, z+1)
	if (z-1) >= 0 and world[x][y][z-1] == 0:
		lava(world, x, y, z-1)


	


if __name__ == "__main__":
	lava_droplets = [tuple(int(elem) for elem in coord.split(',')) for coord in get_data(day=18, year=2022).splitlines()]

	matplotlib.use('TKagg')
	ax = plt.axes(projection='3d')

	x_data = [x for x, y, z in lava_droplets]
	y_data = [y for x, y, z in lava_droplets]
	z_data = [z for x, y, z in lava_droplets]
	ax.scatter3D(x_data, y_data, z_data, c=z_data, cmap='Greens')
	plt.show()

	exposed_sides = 0

	x_max = max(x_data)
	y_max = max(y_data)
	z_max = max(z_data)


	# initialize world
	world = np.zeros((x_max+2, y_max+2, z_max+2))
	for x, y, z in lava_droplets:
		world[x][y][z] = 1
	sys.setrecursionlimit(999999999)
	lava(world, 0, 0, 0)

	for x, y, z in lava_droplets:
		exposed_sides += 1 if world[x+1][y][z] == 2 else 0
		exposed_sides += 1 if world[x-1][y][z] == 2 else 0
		exposed_sides += 1 if world[x][y+1][z] == 2 else 0
		exposed_sides += 1 if world[x][y-1][z] == 2 else 0
		exposed_sides += 1 if world[x][y][z+1] == 2 else 0
		exposed_sides += 1 if world[x][y][z-1] == 2 else 0

	print("Part 2: ", exposed_sides)