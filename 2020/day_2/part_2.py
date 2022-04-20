def parse():
    with open("input.txt", "r") as f:
        passwords = list()
        for line_ in f.readlines():
            line = line_.strip().split(" ")
            for i in range(len(line)):
                if i == 0:
                    numbers = line[i].split("-")
                    low = int(numbers[0])
                    high = int(numbers[1])
                elif i == 1:
                    c = line[i][0]
                else:
                    password = line[i]
            passwords.append({"low": low, "high": high, "c": c, "password": password})
        return passwords

def part_2(passwords):
    valid_passwords = 0
    for password in passwords:
        if (password['c'] == password["password"][password["low"]-1]):
            if (password['c'] != password["password"][password["high"]-1]):
                valid_passwords += 1
        elif (password['c'] == password["password"][password["high"]-1]):
            valid_passwords += 1
    return valid_passwords

print(part_2(parse()))

