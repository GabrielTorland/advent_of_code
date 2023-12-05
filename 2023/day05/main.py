import numpy as np
import re

class CategoryMapper:
    """A class to map a number or a range of numbers from one category to another."""
    def __init__(self, target_category, source_category, destination_ranges_start, source_ranges_start, length_ranges) -> None:
        self.target_category = target_category
        self.source_category = source_category 
        self.destination_ranges_start = destination_ranges_start 
        self.source_ranges_start = source_ranges_start
        self.length_ranges = length_ranges
    
    @property
    def __number_of_ranges(self):
        return len(self.destination_ranges_start)

    def map_number(self, number):
        """Maps a number from the source category to the target category."""
        for i in range(self.__number_of_ranges):
            if number >= self.source_ranges_start[i] and number < self.source_ranges_start[i] + self.length_ranges[i]:
                return self.destination_ranges_start[i] + number - self.source_ranges_start[i]
        return number

    def map_range(self, value_range):
        """Maps a range of numbers from the source category to the target category."""
        start, end = value_range
        new_ranges = []
        for i in range(self.__number_of_ranges):
            if start >= self.source_ranges_start[i] and start < self.source_ranges_start[i] + self.length_ranges[i]:
                if end <= self.source_ranges_start[i] + self.length_ranges[i]:
                    new_ranges.append((self.destination_ranges_start[i] + start - self.source_ranges_start[i], self.destination_ranges_start[i] + end - self.source_ranges_start[i]))
                    start = end
                else:
                    new_ranges.append((self.destination_ranges_start[i] + start - self.source_ranges_start[i], self.destination_ranges_start[i] + self.length_ranges[i]))
                    start = self.source_ranges_start[i] + self.length_ranges[i]
        if start < end:
            new_ranges.append((start, end))
        return new_ranges
        

def parse_input(input_path): 
    raw_maps = open(input_path, 'r').read().split('\n\n')
    numbers = re.findall(r'\d+', raw_maps[0])
    seeds = np.array([int(number) for number in numbers])
    category_mappers = []
    for raw_map in raw_maps[1:]:
        rows = raw_map.split('\n')
        source_category, destination_category = re.search(r"(\w+)-to-(\w+)", rows[0]).groups()
        destination_ranges_start = np.array([int(row.strip().split()[0]) for row in rows[1:]])
        source_ranges_start = np.array([int(row.strip().split()[1]) for row in rows[1:]])
        length_ranges = np.array([int(row.strip().split()[2]) for row in rows[1:]])
        category_mappers.append(CategoryMapper(destination_category, source_category, destination_ranges_start, source_ranges_start, length_ranges))
    return seeds, category_mappers

def part_1(seeds, category_mappers):
    """Finding the seed with the smallest location value. This approach is for small numbers of seeds."""
    locations = []
    for seed in seeds:
        value = seed
        for category_mapper in category_mappers:
            value = category_mapper.map_number(value)
        locations.append(value)
    return min(locations)

def part_2(seeds, category_mappers):
    """Finding the seed with the smallest location value. This approach is for large ranges of seeds."""
    updated_seeds = [(seeds[i], seeds[i]+seeds[i+1]) for i in range(0, len(seeds), 2)]
    location_ranges = []
    for seed_range in updated_seeds:
        current_ranges = [seed_range]
        for category_mapper in category_mappers:
            next_ranges = []
            while len(current_ranges) != 0:
                next_ranges += category_mapper.map_range(current_ranges.pop())
            current_ranges = next_ranges 
        location_ranges += current_ranges
    return min(location_ranges, key=lambda x: x[0])[0]
            


def main():
    seeds, category_mappers = parse_input("input.txt")
    print("Part 1: ", part_1(seeds, category_mappers)) # 331445006
    print("Part 2: ", part_2(seeds, category_mappers)) # 6472060
    

if __name__ == "__main__":
    main()