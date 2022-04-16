
def main():
    with open("input.txt", 'r') as raw:
        numbers = [int(line.strip()) for line in raw]

    increased = 0
    for i in range(len(numbers)-1):
        if numbers[i+1] > numbers[i]:
            increased += 1
    print(f"Times increased: {increased}")


if __name__ == "__main__":
    main()
