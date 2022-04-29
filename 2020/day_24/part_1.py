import sys
from collections import defaultdict

# The tiles are all white on one side and black on the other. They start with the white side facing up.

def parse():
    infile = sys.argv[1] if len(sys.argv) > 1 else "input.in" 
    return [line.strip() for line in open(infile).readlines()]
    
def flip_tiles(tiles):
    tiles_map = defaultdict(lambda: "white")
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
            
        pos = tuple(pos)
        tiles_map[pos] = "black" if tiles_map[pos] == "white" else "white"
    return tiles_map
ans = [col for col in flip_tiles(parse()).values() if col == "black"]
print(f"Part 1: {len(ans)}")