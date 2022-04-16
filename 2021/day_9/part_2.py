
def parse_text():
    with open("input.txt", 'r') as raw:
        points = list()
        for line in raw:
            temp_points = list()
            for point in line.strip():
                temp_points.append(int(point))
            points.append(temp_points)

    return points


def main():
    points = parse_text()
    basin = list()
    for row in range(len(points)):
        for col in range(len(points[row])):

            if (col+1 < len(points[row])) and (points[row][col] >= points[row][col+1]):
                continue

            elif (col-1 >= 0) and (points[row][col] >= points[row][col-1]):
                continue

            elif (row+1 < len(points)) and (points[row][col] >= points[row+1][col]):
                continue

            elif (row-1 >= 0) and (points[row][col] >= points[row-1][col]):
                continue
            prev_downhill_points = set()
            downhill_points = {(row, col)}
            while len(downhill_points) != 0:
                point = downhill_points.pop()

                if points[point[0]][point[1]] == 9:
                    continue

                prev_downhill_points.add(point)

                if (point[1] - 1 >= 0) and ((point[0], point[1] - 1) not in prev_downhill_points):
                    downhill_points.add((point[0], point[1] - 1))
                if (point[0] - 1 >= 0) and ((point[0] - 1, point[1]) not in prev_downhill_points):
                    downhill_points.add((point[0] - 1, point[1]))
                if (point[0] + 1 < len(points)) and ((point[0] + 1, point[1]) not in prev_downhill_points):
                    downhill_points.add((point[0] + 1, point[1]))
                if (point[1] + 1 < len(points[0])) and ((point[0], point[1] + 1) not in prev_downhill_points):
                    downhill_points.add((point[0], point[1] + 1))
            basin.append(len(prev_downhill_points))
    basin.sort(reverse=True)
    answer = 1
    for size in basin[:3:]:
        answer *= size
    print(answer)


if __name__ == "__main__":
    main()