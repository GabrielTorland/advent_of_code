import sys
from collections import defaultdict

# The tiles are all white on one side and black on the other. They start with the white side facing up.

def parse():
    infile = sys.argv[1] if len(sys.argv) > 1 else "input.in" 
    return [line.strip() for line in open(infile).readlines()]
    
def flip_tiles(tiles):
    tiles_map = defaultdict(lambda: "white")
    max_x = 0
    max_y = 0
    for tile in tiles:
        i = 0
        pos = [0, 0]
        while i < len(tile):
            dir = tile[i:i+2]
            i += 2
            if dir == "ne":
                pos[0] += 1
                pos[1] -= 1
            elif dir == "nw":
                pos[1] -= 1
            elif dir == "sw":
                pos[0] -= 1
                pos[1] += 1
            elif dir == "se":
                pos[1] += 1
            else:
                dir = tile[i-2]
                if dir == 'e':
                    pos[0] += 1
                else:
                    pos[0] -= 1
                i -= 1
        max_x = abs(pos[0]) if abs(pos[0]) > max_x else max_x
        max_y = abs(pos[1]) if abs(pos[1]) > max_y else max_y

        pos = tuple(pos)
        tiles_map[pos] = "black" if tiles_map[pos] == "white" else "white"
    return tiles_map, max_x, max_y

def simulate(tiles_map, rounds, round, max_x, max_y):
    if round == rounds:
        return tiles_map
    new_tiles_map = tiles_map.copy()
    adjecent_dirs = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
    for x in range(-max_x-1, max_x+2):
        for y in range(-max_y-1, max_y+2):
            pos = (x, y)
            if tiles_map[pos] == "black":
                adjecent_blacks = sum([1 for dir in adjecent_dirs if tiles_map[(pos[0]+dir[0], pos[1]+dir[1])] == "black"])
                if adjecent_blacks == 0 or adjecent_blacks > 2:
                    new_tiles_map[pos] = "white"
            else:
                adjecent_blacks = sum([1 for dir in adjecent_dirs if tiles_map[(pos[0]+dir[0], pos[1]+dir[1])] == "black"])
                if adjecent_blacks == 2:
                    new_tiles_map[pos] = "black"

    print(list(new_tiles_map.values()).count("black"))
    return simulate(new_tiles_map, 100, round+1, max_x+1, max_y+1)



tiles_map, max_x, max_y = flip_tiles(parse())
ans = [col for col in simulate(tiles_map,100, 0, max_x, max_y).values() if col == "black"]
print(f"Part 2: {len(ans)}")


