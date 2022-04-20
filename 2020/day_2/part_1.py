
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

def part_1(passwords):
    valid_passwords = 0
    for password in passwords:
        if (password["password"].count(password["c"]) >= password["low"]) and (password["password"].count(password["c"]) <= password["high"]):
            valid_passwords += 1
    return valid_passwords

print(part_1(parse()))
