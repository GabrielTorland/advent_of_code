from itertools import combinations
from functools import lru_cache 
import math
import sys

# Each scanner is capable of detecting all beacons in a large cube centered on the scanner; 
# beacons that are at most 1000 units away from the scanner in each of the three axes (x, y, and z) have their precise position determined relative to the scanner.
# scanners cannot detect other scanners.
# he scanners also don't know their rotation or facing direction.

class Scanner:
    def __init__(self, index):
        self.index = index
        self.beacons = list()
        self.pos = None
        self.adj = list()
        self.visited = False

def parse():
    infile = sys.argv[1] if len(sys.argv) > 1 else "input.in"
    with open(infile, 'r') as raw:
        index = 0
        scanners = list()
        for line_ in raw.readlines():
            line = line_.strip()
            if line == "":
                scanners.append(scanner)
                index += 1
                continue
            if "scanner" in line:
                scanner = Scanner(index)
                continue
            pos = line.split(',')
            scanner.beacons.append((int(pos[0]), int(pos[1]), int(pos[2])))
        scanners[0].pos = (0, 0, 0)
        scanners.append(scanner)
        return scanners

@lru_cache(None)
def compose(rot1, rot2):
    a = rotations(rotations((1, 2, 3))[rot1])[rot2]
    for comp_rot in range(24):
        if rotations((1, 2, 3))[comp_rot] == a:
            return comp_rot

@lru_cache(None)
def rotations(point):
    # https://i.imgur.com/Ff1vGT9.png
    x, y, z = point
    return [
        (x, y, z), (x, z, -y), (x, -y, -z), (x, -z, y),
        (-x, -y, z), (-x, z, y), (-x, y, -z), (-x, -z, -y),
        (y, z, x), (y, x, -z), (y, -z, -x), (y, -x, z),
        (-y, -z, x), (-y, x, z), (-y, z, -x), (-y, -x, -z),
        (z, x, y), (z, y, -x), (z, -x, -y), (z, -y, x),
        (-z, -x, y), (-z, y, x), (-z, x, -y), (-z, -y, -x)
    ]

# Two vectors with the same length will allways have the same fingerprint regardless of the rotation and displacement.
# This method prevents working with floats.
@lru_cache(None)
def fingerprint(v):
    return tuple(sorted([abs(c) for c in v]))

@lru_cache(None)
def inv(rot):
    a = rotations((1, 2, 3))[rot]
    for inv_rot in range(24):
        if rotations(a)[inv_rot] == (1, 2, 3):
            return inv_rot

# Vector between two beacons.
def sub(v1, v2):
    return (v1[0]-v2[0], v1[1]-v2[1], v1[2]-v2[2])

# Add two vectors.
def add(v1, v2):
    return (v1[0]+v2[0], v1[1]+v2[1], v1[2]+v2[2])

def neg(a):
    return (-a[0], -a[1], -a[2])

# Brute force to find displacement vector and rotation.
def orient(a, b, base_index, rots):

    a_set = set(a.beacons)

    for rot in rots:
        other_beacons = [rotations(beacon)[rot] for beacon in b.beacons]
        for other_base in other_beacons:
            translate = sub(a.beacons[base_index], other_base)
            other_beacons_translated = set([add(beacon, translate) for beacon in other_beacons])

            if len(a_set.intersection(other_beacons_translated)) >= 12:
                # Noice
                return translate, rot
    return None


def distances_set(beacons):
    return {fingerprint(sub(a, b)) for a, b in combinations(beacons, r=2)}

# Using ncr(12, 2) = 66, which is the amount of equal lengths needed to test if they might overlap.
def might_overlap(a, b):
       if len(distances_set(a.beacons).intersection(distances_set(b.beacons))) >= 66: 
            return True
       return False
        
def have_overlap(a, b):
    if not might_overlap(a, b): return False 
    for i, j in combinations(range(len(a.beacons)), r=2):
        for k, l in combinations(range(len(b.beacons)), r=2):
            va = sub(a.beacons[i], a.beacons[j])
            vb = sub(b.beacons[k], b.beacons[l])
            if not fingerprint(va) == fingerprint(vb): continue

            # Determine the rotation and offset
            rots = list()

            rot_vb = rotations(vb)
            for r in range(24):
                if rot_vb[r] == va:
                    rots.append(r)
            
            if len(rots) == 0: continue

            return orient(a, b, i, rots)
            
    return False


def find_overlapping(scanners):
    for i in range(len(scanners)):
        for j in range(i+1, len(scanners)):
            x = have_overlap(scanners[i], scanners[j])
            if x:
                scanners[i].adj.append((j, x[0], x[1]))
                scanners[j].adj.append((i, rotations(neg(x[0]))[inv(x[1])], inv(x[1])))


def map_beacons(scanners):
    beacons = set()
    stack = [(0, (0, 0, 0), 0)]
    
    while len(stack) > 0:
        i, trans, rot = stack.pop()
        scan = scanners[i]

        if scan.visited: continue
        scan.visited = True
        beacons = beacons.union({add(rotations(beacon)[rot], trans) for beacon in scan.beacons})
        scan.pos = trans

        for s in scan.adj:
            if scanners[s[0]].visited: 
                continue
            new_trans = add(trans, rotations(s[1])[rot])
            new_rot = compose(s[2], rot)
            stack.append((s[0], new_trans, new_rot))
    return beacons


def manhattan_distances(scanners):
    dists = set()
    for scanner in scanners:
        for other_scanner in scanners:
            dists.add(sum(sub(scanner.pos, other_scanner.pos)))
    return dists



if __name__ == "__main__":
    scanners = parse()
    find_overlapping(scanners)
    beacons = map_beacons(scanners)
    print("Part 1: ", len(beacons))
    print("Part 2: ", max(manhattan_distances(scanners)))