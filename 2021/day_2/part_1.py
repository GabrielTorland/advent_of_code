class Submarine:
    def __init__(self):
        self.depth = 0
        self.horizontal = 0

    def move_up(self, value):
        self.depth -= value

    def move_down(self, value):
        self.depth += value

    def move_forward(self, value):
        self.horizontal += value

    def multiply(self):
        return self.depth*self.horizontal


def main():
    with open("input.txt", 'r') as raw:
        moves = [line.strip().split(' ') for line in raw]

    submarine = Submarine()
    for move in moves:
        if move[0] == "down":
            submarine.move_down(int(move[1]))
        elif move[0] == "up":
            submarine.move_up(int(move[1]))
        else:
            submarine.move_forward(int(move[1]))

    print(f"Final horizontal position * final depth is {submarine.multiply()}")


if __name__ == "__main__":
    main()
