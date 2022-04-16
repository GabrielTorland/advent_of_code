

def main():
    with open("input.txt", 'r') as raw:
        bit_strings = [line.strip() for line in raw]

    gamma_rate = ""
    epsilon_rate = ""
    for bit in range(len(bit_strings[0])):
        ones = 0
        zeros = 0
        for bits in bit_strings:
            if bits[bit] == "1":
                ones += 1
            else:
                zeros += 1
        gamma_rate += f"{1 if ones >= zeros else 0}"
    epsilon_rate = "".join(str((int(bit)+1) % 2) for bit in gamma_rate)
    power_consumption = int(gamma_rate, 2)*int(epsilon_rate, 2)

    print(f"The power consumption of the submarine is {power_consumption}")


if __name__ == "__main__":
    main()