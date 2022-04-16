
def change_waypoints(original_waypoints, waypoints_copy, instruction, new_direction):
    for key, value in original_waypoints.items():
        if value != 0:
            waypoints_copy[new_direction[key][instruction]] = value
    return waypoints_copy


def main():
    with open('input.txt', 'r') as raw:
        instructions = raw.read().splitlines()

    navigation_instructions = {'N': 0,
                               'S': 0,
                               'E': 0,
                               'W': 0,
                               }
    waypoints = {'N': 1,
                 'E': 10,
                 'S': 0,
                 'W': 0
                 }
    change_waypoint = {'N': {'L90': 'W', 'R90': 'E', 'L180': 'S', 'R180': 'S', 'L270': 'E', 'R270': 'W'},
                       'E': {'L90': 'N', 'R90': 'S', 'L180': 'W', 'R180': 'W', 'L270': 'S', 'R270': 'N'},
                       'S': {'L90': 'E', 'R90': 'W', 'L180': 'N', 'R180': 'N', 'L270': 'W', 'R270': 'E'},
                       'W': {'L90': 'S', 'R90': 'N', 'L180': 'E', 'R180': 'E', 'L270': 'N', 'R270': 'S'}}

    for instruction in instructions:
        if instruction[0] == 'F':
            for key in navigation_instructions:
                navigation_instructions[key] += int(instruction[1:])*waypoints[key]
        elif instruction[0] == 'R' or instruction[0] == 'L':
            waypoints = change_waypoints(waypoints, waypoints.copy(), instruction, change_waypoint)
        else:
            waypoints[instruction[0]] += int((instruction[1:]))
    print(
        f"The Manhattan distance is {abs(navigation_instructions['N'] - navigation_instructions['S']) + abs(navigation_instructions['E'] - navigation_instructions['W'])}.")


if __name__ == "__main__":
    main()
