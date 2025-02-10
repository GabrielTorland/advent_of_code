

def parse(input_file="input.txt"):
    stones_list = [number for number in open(input_file).read().strip().split()]
    stones_dict = {}
    for stone in stones_list:
        if stone in stones_dict:
            stones_dict[stone] += 1
        else:
            stones_dict[stone] = 1
    return stones_dict


def get_number_of_stones(stones):
    return sum(stones.values())

def simulate_stones(stones, k):
    number_of_stones = [get_number_of_stones(stones)]
    print(f"Round 0: {number_of_stones[-1]} stones")
    for i in range(k):
        new_stones = {}
        for stone in stones.keys():
            if stone == '0':
                new_stones['1'] = new_stones.get('1', 0) + stones['0']
            elif len(stone) % 2 == 0:
                mid = len(stone) // 2
                left_stone = stone[:mid]
                right_stone = stone[mid:]
                # Remove leading zeros
                while right_stone[0] == '0' and len(right_stone) != 1:
                    right_stone = right_stone[1:]
                new_stones[left_stone] = new_stones.get(left_stone, 0) + stones[stone]
                new_stones[right_stone] = new_stones.get(right_stone, 0) + stones[stone]
            else:
                new_stone = str(int(stone)*2024)
                new_stones[new_stone] = new_stones.get(new_stone, 0) + stones[stone]
        stones = new_stones
        number_of_stones.append(get_number_of_stones(stones))
        print(f"Round {i+1}: {number_of_stones[-1]} stones. Increase: {number_of_stones[-1] - number_of_stones[-2]}")
    return stones


def p1(stones):
    stones = simulate_stones(stones, 25)
    count = get_number_of_stones(stones)
    return count

def p2(stones):
    stones = simulate_stones(stones, 75)
    count = get_number_of_stones(stones)
    return count

if __name__ == "__main__":
    stones = parse()
    print("Part 1:", p1(stones))
    print("Part 2:", p2(stones))