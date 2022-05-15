import sys, re
from rtree import index

def volume(cuboids):
    return sum((
        (c[3] - c[0]) * (c[4] - c[1]) * (c[5] - c[2])
        for c in cuboids
    ))

def is_empty(c):
    return c[0] == c[3] or c[1] == c[4] or c[2] == c[5]

def intersects1d(c, d):
    (c1, c2), (d1, d2) = c, d
    return (c2 > d1 and d2 > c1)

def is_intersecting(c, d):
    (cx1,cy1,cz1, cx2,cy2,cz2) = c
    (dx1,dy1,dz1, dx2,dy2,dz2) = d

    return (
        intersects1d((cx1,cx2), (dx1,dx2))
        and intersects1d((cy1,cy2), (dy1,dy2))
        and intersects1d((cz1,cz2), (dz1,dz2))
    )

# Removing parts of the cuboid that intersect.
# Return's up to six cuboids representing the cuboid minus the intersection.
# This process will exponentially increase cs, but it's not a problem.
def subtract(c, inter):
    if not is_intersecting(c, inter): return [c]

    (cx1,cy1,cz1, cx2,cy2,cz2) = c
    (inter_x1, inter_y1, inter_z1, inter_x2, inter_y2, inter_z2) = inter

    # Intersection of two cuboids
    (inter_x1, inter_y1, inter_z1, inter_x2, inter_y2, inter_z2) = (
        max(cx1, inter_x1), max(cy1, inter_y1), max(cz1, inter_z1), 
        min(cx2, inter_x2), min(cy2, inter_y2), min(cz2, inter_z2)
    )

    spltd_cuboids = [
        (cx1,cy1,cz1, cx2,cy2,inter_z1), # down
        (cx1,cy1,inter_z2, cx2,cy2,cz2), # up
        (cx1,cy1,inter_z1, cx2, inter_y1, inter_z2), # front
        (cx1,inter_y2,inter_z1, cx2,cy2,inter_z2), # back
        (cx1,inter_y1,inter_z1, inter_x1,inter_y2,inter_z2), # left
        (inter_x2,inter_y1,inter_z1, cx2,inter_y2,inter_z2), # right
    ]
    return [cuboid for cuboid in spltd_cuboids if not is_empty(cuboid)]


def rem_inter(cs, inters):
    for inter in inters:
        cs = sum([subtract(c, inter) for c in cs], [])
    return cs

if __name__ == '__main__':
    # r tree
    p = index.Property()
    p.dimension = 3
    ix = index.Index(properties=p)
    
    cuboids = list()
    total = 0
    infile = sys.argv[1] if len(sys.argv) > 1 else 'input.in'
    lines = open(infile).read().split('\n')
    pattern = re.compile(r"(on|off).{3}(-?\d+)\.\.(-?\d+).{3}(-?\d+)\.\.(-?\d+).{3}(-?\d+)\.\.(-?\d+)")
    for line in reversed(lines): 
        state, *cords = pattern.match(line).groups()
        x1,x2, y1,y2, z1,z2 = map(int, cords)
        cuboid = (x1,y1,z1, x2+1,y2+1,z2+1)
        if state == "on":
            total += volume(rem_inter([cuboid], [cuboids[i] for i in ix.intersection(cuboid)]))
        ix.insert(len(cuboids), cuboid)
        cuboids.append(cuboid)
    print("Part 2: ", total)
        

