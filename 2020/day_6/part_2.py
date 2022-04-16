from string import ascii_lowercase


def main():
    answer_data = []
    with open('input.txt', 'r') as answers:
        i = 0
        group = []
        person = []
        for line in answers:
            temp = line.strip()
            if temp == '':
                answer_data.append(group)
                i += 1
                group = []

            else:
                for char in temp:
                    person.append(char)
                group.append(person)
                person = []
        # adding one extra at the end, because the if statement doesnt register when it stops reading.
        answer_data.append(group)

        yes_answers = 0
        for group in answer_data:
            answer_count = {}
            for c in ascii_lowercase:
                answer_count[c] = []
            for person in group:
                for answer in person:
                    answer_count[answer].append(person)
            for valid_answers in answer_count.values():
                if len(valid_answers) == len(group):
                    yes_answers += 1
        print(f"The sum of the questions where everyone in the group answered yes : {yes_answers}")


if __name__ == "__main__":
    main()
