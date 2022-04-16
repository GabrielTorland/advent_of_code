

def parse():
    with open("input.txt", 'r') as raw:
        coordinates = list()
        for line in raw:
            temp = line.split(" -> ")
            coordinates.append((temp[0].strip().split(','), temp[1].strip().split(',')))

    return coordinates


def main():
    # Init
    coordinates = parse()
    points_lookup = dict()

    for points in coordinates:
        x_1 = int(points[1][0])
        x_2 = int(points[0][0])
        y_1 = int(points[1][1])
        y_2 = int(points[0][1])
        if x_1 != x_2 and y_1 != y_2:
            continue

        for x in range(min(x_1, x_2), max(x_1, x_2)+1):

            for y in range(min(y_1, y_2), max(y_1, y_2)+1):
                try:
                    points_lookup[(x, y)] += 1
                except:
                    points_lookup[(x, y)] = 1

    print(f"The amount of points that overlap with at least two lines are {sum([1 if val >= 2 else 0 for val in points_lookup.values()])}")


if __name__ == "__main__":
    main()