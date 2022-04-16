from collections import defaultdict
import math
from itertools import permutations

# Each scanner is capable of detecting all beacons in a large cube centered on the scanner; 
# beacons that are at most 1000 units away from the scanner in each of the three axes (x, y, and z) have their precise position determined relative to the scanner.
# scanners cannot detect other scanners.
# he scanners also don't know their rotation or facing direction.

class Scanner:
    def __init__(self, index):
        self.index = index
        self.beacons = list()
        self.distances = defaultdict(lambda: list())
        self.pos = None # Unknown
        self.overlapping = list() # Unknown
        self.overlapping_beacons = list() # Unknown

    def calculate_distances(self):
        for i in range(len(self.beacons)):
            for j in range(len(self.beacons)):
                if j > i:
                    self.distances[math.sqrt((self.beacons[i][0] - self.beacons[j][0])**2 + (self.beacons[i][1] - self.beacons[j][1])**2 + (self.beacons[i][2] - self.beacons[j][2])**2)].append(self.beacons[i])
                    self.distances[math.sqrt((self.beacons[i][0] - self.beacons[j][0])**2 + (self.beacons[i][1] - self.beacons[j][1])**2 + (self.beacons[i][2] - self.beacons[j][2])**2)].append(self.beacons[j])
def parse():
    with open("input.txt", 'r') as raw:
        index = 0
        scanners = list()
        for line_ in raw.readlines():
            line = line_.strip()
            if line == "":
                scanner.calculate_distances()
                scanners.append(scanner)
                index += 1
                continue
            if "scanner" in line:
                scanner = Scanner(index)
                continue
            pos = line.split(',')
            scanner.beacons.append((int(pos[0]), int(pos[1]), int(pos[2])))

        return scanners

def region_grouping(scanners):
    for i in range(len(scanners)):
        for j in range(len(scanners)):
            if j <= i:
                continue
            overlapping = set(scanners[i].distances.keys()).intersection(set(scanners[j].distances.keys()))
            if len(overlapping) >= 12: 
                scanners[i].overlapping_beacons.append(overlapping)
                scanners[j].overlapping_beacons.append(overlapping)
                scanners[i].overlapping.append(scanners[i])
                scanners[j].overlapping.append(scanners[j])
    return scanners

def count_beacons(scanner, pos):
    beacons = set()
    comparisons = []
    perms = []
    for perm in list(permutations(['x', 'y', 'z', '-x', '-y', '-z'], 3)):
        # Count occurrences of char in list
        if perm.count('x')+perm.count('-x') > 1:
            continue
        if perm.count('y')+perm.count('-y') > 1:
            continue
        if perm.count('z')+perm.count('-z') > 1:
            continue
        perms.append(perm)
    for i, ov_scanner in enumerate(scanner.overlapping):
        for dist in scanner.overlapping_beacons[i]:
            comparisons.append([])
            comparisons[i].append(scanner.distances[dist])
            comparisons[i].append(ov_scanner.distances[dist])
        for perm in perms:

            for j in range(len(comparisons[i])):
                for k in range(len(comparisons[i][j])):
                   pass
                   


count_beacons(region_grouping(parse())[0], (0,0,0))