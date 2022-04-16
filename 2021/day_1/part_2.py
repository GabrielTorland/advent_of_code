

def main():
    with open("input.txt", 'r') as raw:
        numbers = [int(line.strip()) for line in raw]

    increased = 0
    for i in range(len(numbers)-3):
        if sum(numbers[i+1:i+4:]) > sum(numbers[i:i+3:]):
            increased += 1
        if i+4 == len(numbers):
            print()
    print(f"Times increased: {increased}")


if __name__ == "__main__":
    main()
