
class LanternFish:
    def __init__(self, initial_time, parent):
        self.Internal_clock = initial_time
        self.parent = parent
        self.children = list()


def parse():
    with open("input.txt", 'r') as raw:
        root = LanternFish(None, None)
        for line in raw:
            for numb in line.strip().split(','):
                root.children.append(LanternFish(int(numb), root))

    return root


def simulate_lantern_fish(root):
    lantern_fish = 1 if root.parent is not None else 0

    for children in root.children:
        lantern_fish += simulate_lantern_fish(children)

    if root.Internal_clock is not None:
        if root.Internal_clock != 0:
            root.Internal_clock -= 1
        else:
            root.Internal_clock = 6
            root.children.append(LanternFish(8, root))

    return lantern_fish

def main():
    dummy_root = parse()
    for generation in range(19+1):
        print(f"Generation {generation}: {simulate_lantern_fish(dummy_root)}")


if __name__ == "__main__":
    main()