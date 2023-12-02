import re
from collections import defaultdict

def parse(input):
    with open(input) as raw_input:
        lines = raw_input.readlines()
    games = []
    for line in lines:
        raw_bags = line.split(":")[-1].strip().split("; ")
        bags = []
        for raw_bag in raw_bags:
            color_values = re.findall(r"(\d+)\s+(\w+)", raw_bag)
            color_value_dict = defaultdict(int)
            for value, color in color_values:
                color_value_dict[color] = int(value)
            bags.append((color_value_dict["red"], color_value_dict["green"], color_value_dict["blue"]))
        games.append(bags)
    return games
     

def is_game_valid(game, limit):
    """Validate a game by using pre-defined limits."""
    for bag in game:
        red, green, blue = bag
        if red > limit[0] or green > limit[1] or blue > limit[2]:
            return False
    return True

def part_1(games, limit):
    """Find the indices of the valid games."""
    valid_games = []
    for i, game in enumerate(games):
        if not is_game_valid(game, limit):
            continue
        valid_games.append(i+1)
    return valid_games

def part_2(games):
    """Find the minimum limit for each game and then calculate the power."""
    power_games = []
    for game in games:
        min_red = max(game, key=lambda x: x[0])[0]
        min_green = max(game, key=lambda x: x[1])[1]
        min_blue = max(game, key=lambda x: x[2])[2]
        power_games.append(min_red*min_green*min_blue)
    return power_games


def main():
    limit = (12, 13, 14)
    games = parse("input.txt")
    print("Part 1: ", sum(part_1(games, limit))) # 2256
    print("Part 2: ", sum(part_2(games))) # 74229


if __name__ == "__main__":
    main()