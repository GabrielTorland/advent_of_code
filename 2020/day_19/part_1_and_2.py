from operator import ge
import sys, re


infile = sys.argv[1] if len(sys.argv) > 1 else "input.in"
rules_raw, msgs = open(infile).read().split("\n\n")

rules = {}
for rule in rules_raw.split("\n"):
    num, r = rule.split(": ")
    rules[num] = [s.split() for s in r.split(" | ")]

# Creating regular expression
def gen_regex(r=r'0', depth=15):
    if depth == 0:
        return ""
    if rules[r][0][0].startswith('"'):
        return rules[r][0][0].strip('""')
    return "(" + "|".join(["".join([gen_regex(sub, depth-1) for sub in subrule]) for subrule in rules[r]]) + ")"

# Part 1 
r1 = re.compile(gen_regex(r"0"))
res = [r1.fullmatch(msg) for msg in msgs.split('\n')]
print(f"part 1: {len([x for x in res if x])}")

# part 2
rules['8'] = [['42'], ['42', '8']]
rules['11'] = [['42', '31'], ['42', '11', '31']]
r2 = re.compile(gen_regex("0"))
res = [r2.fullmatch(msg) for msg in msgs.split('\n')]
print(f"part 2: {len([x for x in res if x])}")