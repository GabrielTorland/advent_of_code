
class Passport:
    def __init__(self):
        self.byr = None
        self.iyr = None
        self.eyr = None
        self.hgt = None
        self.hcl = None
        self.ecl = None
        self.pid = None
        self.cid = None
        self.inserted = 0
        self.valid = None
    def insert_byr(self, byr):
        if int(byr) >= 1920 and int(byr) <= 2002:
            self.byr = byr
            self.inserted += 1
    def insert_iyr(self, iyr):
        if int(iyr) >= 2010 and int(iyr) <= 2020:
            self.iyr = iyr
            self.inserted += 1
    def insert_eyr(self, eyr):
        if int(eyr) >= 2020 and int(eyr) <= 2030:
            self.eyr = eyr
            self.inserted += 1
    def insert_hgt(self, hgt):
        if hgt[-2:] == "cm":
            if int(hgt[:-2]) >= 150 and int(hgt[:-2]) <= 193:
                self.hgt = hgt
                self.inserted += 1
        elif hgt[-2:] == "in":
            if int(hgt[:-2]) >= 59 and int(hgt[:-2]) <= 76:
                self.hgt = hgt
                self.inserted += 1
    def insert_hcl(self, hcl):
        if hcl[0] == "#":
            if len(hcl) == 7:
                self.hcl = hcl
                self.inserted += 1
    def insert_ecl(self, ecl):
        if ecl == "amb" or ecl == "blu" or ecl == "brn" or ecl == "gry" or ecl == "grn" or ecl == "hzl" or ecl == "oth":
            self.ecl = ecl
            self.inserted += 1
    def insert_pid(self, pid):
        if len(pid) == 9 and pid.isdigit():
            self.pid = pid
            self.inserted += 1
    def insert_cid(self, cid):
        self.cid = cid
        self.inserted += 1
    def insert_data(self, header, data):
        if header == "byr":
            self.insert_byr(data)
        elif header == "iyr":
            self.insert_iyr(data)
        elif header == "eyr":
            self.insert_eyr(data)
        elif header == "hgt":
            self.insert_hgt(data)
        elif header == "hcl":
            self.insert_hcl(data)
        elif header == "ecl":
            self.insert_ecl(data)
        elif header == "pid":
            self.insert_pid(data)
        else:
            self.insert_cid(data)
    def validate(self):
        if self.inserted == 7 and self.cid == None:
            self.valid = True
            return True
        if self.inserted == 8:
            self.valid = True
            return True
        else:
            self.valid = False
            return False

def part_1():
    with open("input.txt", 'r') as raw:
        passports = set()
        passport = Passport()
        for line_ in raw.readlines():
            line = line_.strip()
            if line == "":
                if passport.validate():
                    passports.add(passport)
                passport = Passport()
                continue
            entries = line.split(" ")
            for entry in entries:
                data = entry.split(":")
                passport.insert_data(data[0], data[1])
        if passport.validate():
            passports.add(passport)
    return passports

passports = part_1()
print(len(passports))