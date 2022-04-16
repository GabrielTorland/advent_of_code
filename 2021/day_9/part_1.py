
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
    risk_levels = list()

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

            risk_levels.append(points[row][col]+1)

    print(f"The sum of the risk levels of all low points on the heightmap is: {sum(risk_levels)}.")


if __name__ == "__main__":
    main()