

def main():
    answer_data = []
    with open('input.txt', 'r') as answers:
        i = 0
        group = []
        for line in answers:
            temp = line.strip()
            if temp == '':
                answer_data.append(group)
                i += 1
                group = []
            else:
                for char in temp:
                    group.append(char)
        # adding one extra at the end, because the if statement doesnt register when it stops reading.
        answer_data.append(group)

        yes_answers = 0
        for group in answer_data:
            answer_count = {}
            for answer in group:
                answer_count[answer] = True
            yes_answers += len(answer_count)
        print(f"The sum of the count from each group is: {yes_answers}")


if __name__ == "__main__":
    main()
