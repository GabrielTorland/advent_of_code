from collections import defaultdict


def parse_input():
    result = defaultdict(lambda: list())
    with open("input.txt", 'r') as raw:
        for line in raw:
            codes = line.strip().split('-')
            result[codes[0]].append(codes[1])
            result[codes[1]].append(codes[0])
    return result


def find_paths(paths, current, visited):
    count = 0
    for path in paths[current]:
        if path in visited:
            if path.isupper():
                count += find_paths(paths, path, visited)

        else:
            if path == "end":
                count += 1
            else:
                visited.add(path)
                count += find_paths(paths, path, visited)
                visited.remove(path)
    return count


def main():
    paths = parse_input()
    print(find_paths(paths, "start", {"start"}))


if __name__ == "__main__":
    main()
