from collections import defaultdict


def parse_input():
    result = defaultdict(lambda: list())
    with open("input.txt", 'r') as raw:
        for line in raw:
            codes = line.strip().split('-')
            if codes[1] != "start":
                result[codes[0]].append(codes[1])
            if codes[0] != "start":
                result[codes[1]].append(codes[0])
    return result


def find_paths(paths, current, visited, second_visited):
    count = 0
    for path in paths[current]:
        if path in visited:
            if path.isupper():
                count += find_paths(paths, path, visited, second_visited)
            elif path not in second_visited and len(second_visited) == 0:
                second_visited.add(path)
                count += find_paths(paths, path, visited, second_visited)
                second_visited.remove(path)
        else:
            if path == "end":
                count += 1
            else:
                visited.add(path)
                count += find_paths(paths, path, visited, second_visited)
                visited.remove(path)
    return count


def main():
    paths = parse_input()
    print(find_paths(paths, "start", set(), set()))


if __name__ == "__main__":
    main()
