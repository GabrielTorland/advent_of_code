
def main():
    with open('input.txt', 'r') as raw:
        joltages = {int(line) for line in raw.read().splitlines()}

    adapter_count = {1: [],
                     3: []}
    current_joltage_level = 0
    for joltage in joltages:
        adapter_count[joltage-current_joltage_level].append(joltage)
        current_joltage_level = joltage
    adapter_count[3].append(current_joltage_level + 3)

    print(f"The differences multiplied with each other is: {len(adapter_count[1])*len(adapter_count[3])}.")


if __name__ == "__main__":
    main()

