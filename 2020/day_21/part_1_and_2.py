import sys


ingredient_list = []
all_allergens = dict()

def parse():
    global ingredient_list
    global all_allergens
    infile = sys.argv[1] if len(sys.argv) > 1 else "input.in"
    with open(infile) as f:
        data = f.read().strip().split(")\n")
    for line in data:
        temp = line.replace('\n', ' ').split("(")
        allergens = temp[1].replace("contains ", '').replace(')', '').split(", ")
        ingredients = temp[0].strip().split(' ')
        ingredient_list += ingredients
        for allergen in allergens:
            if allergen in all_allergens.keys():
                # Intersect the two sets
                all_allergens[allergen] &= set(ingredients)
            else:
                all_allergens[allergen] = set(ingredients)


def find_dangerous_allergen(allergens_and_ingredients):
    state = True
    while state:
        state = False
        for allergen_1 in allergens_and_ingredients.keys():
            if len(allergens_and_ingredients[allergen_1]) == 1:
                for allergen_2 in allergens_and_ingredients.keys():
                    if allergen_1 != allergen_2 and len(allergens_and_ingredients[allergen_2]) > 1:
                        state = True
                        allergens_and_ingredients[allergen_2] -= allergens_and_ingredients[allergen_1]

parse()

# Part 1
allergen_ingredients = set([ingredient for ingredients in all_allergens.values() for ingredient in ingredients])
print(len(([ingredient for ingredient in ingredient_list if ingredient not in allergen_ingredients])))

# Part 2
find_dangerous_allergen(all_allergens)
allergens_sorted = sorted(list(all_allergens.keys()))
result = [all_allergens[allergens_sorted[i]].pop() for i in range(len(all_allergens.keys()))]
print(",".join(result))

