from collections import defaultdict
from dis import dis
from itertools import permutations
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
        self.distances = defaultdict(lambda: list())
        self.pos = None # Unknown
        self.overlapping = list() # Unknown
        self.overlapping_beacons = list() # Unknown
        self.validated = False

    def calculate_distances(self):
        for i in range(len(self.beacons)):
            for j in range(len(self.beacons)):
                if j > i:
                    self.distances[math.sqrt((self.beacons[i][0] - self.beacons[j][0])**2 + (self.beacons[i][1] - self.beacons[j][1])**2 + (self.beacons[i][2] - self.beacons[j][2])**2)] += [self.beacons[i], self.beacons[j]]
def parse():
    infile = sys.argv[1] if len(sys.argv) > 1 else "input.in"
    with open(infile, 'r') as raw:
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
        scanners[0].pos = (0, 0, 0)
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
                scanners[i].overlapping.append(scanners[j])
                scanners[j].overlapping.append(scanners[i])
    return scanners

def calculate_distance(x_1, x_0, y_1, y_0, z_1, z_0):
    distance = math.sqrt((x_1 - x_0)**2 + (y_1 - y_0)**2 + (z_1 - z_0)**2)
    return distance

def reconstruct(scanner):
    not_validated = 0
    scanner.validated = True
    for i, scanner_ in enumerate(scanner.overlapping):
        if not scanner.validated:
            not_validated += 1
            continue
        orientations = list(permutations([1, 2, 3]))+list(permutations([-1, 2, 3]))+list(permutations([1, -2, 3]))+list(permutations([1, 2, -3]))
        for orientation in orientations:
            new_overlap_beacons = list()
            for beacon in scanner.overlapping_beacons[i]:
                new_overlap_beacons.append(
                    (
                        -beacon[abs(orientation[0])-1] if orientation[0] < 0 else beacon[orientation[0]-1], 
                        -beacon[abs(orientation[1])-1] if orientation[1] < 0 else beacon[orientation[1]-1],
                        -beacon[abs(orientation[2])-1] if orientation[2] < 0 else beacon[orientation[2]-1]
                    )
                )
            scanner.overlapping_beacons = new_overlap_beacons
            reconstruct(scanner_)
    if len(scanner.overlapping) == not_validated:
        for scanner_ in scanner.overlapping:
            reconstruct(scanner_)






if __name__ == "__main__":
    scanners = parse()
    scanners = region_grouping(scanners)
    reconstruct(scanners[0])