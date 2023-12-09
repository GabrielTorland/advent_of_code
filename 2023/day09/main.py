import numpy as np

def process_sample(sample):
    """Computes the differences of a sample until it reaches 0."""
    sample_processed = [sample.copy()]
    while np.any(sample_processed[-1] != 0):
        last_sample = sample_processed[-1]
        new_sample = np.diff(last_sample)
        sample_processed.append(new_sample)
    return sample_processed

def predict(sample_processed, prediction_type):
    """Predicts the next or previous value of a sample."""
    if prediction_type == 'future':
        sample_processed[-1] = np.append(sample_processed[-1], 0)
        for i in range(len(sample_processed) - 2, -1, -1):
            sample_processed[i] = np.append(sample_processed[i], sample_processed[i+1][-1] + sample_processed[i][-1])
        return sample_processed[0][-1]
    elif prediction_type == 'past':
        sample_processed[-1] = np.insert(sample_processed[-1], 0, 0)
        for i in range(len(sample_processed) - 2, -1, -1):
            new_value = sample_processed[i][0] - sample_processed[i+1][0]
            sample_processed[i] = np.insert(sample_processed[i], 0, new_value)
        return sample_processed[0][0]
    return None

def part_1(dataset):
    """Calculates the sum of extrapolated future values."""
    sum_predictions = 0
    for sample in dataset:
        sample_processed = process_sample(sample)
        sum_predictions += predict(sample_processed, 'future')
    return sum_predictions

def part_2(dataset):
    """Calculates the sum of extrapolated past values."""
    sum_predictions = 0
    for sample in dataset:
        sample_processed = process_sample(sample)
        sum_predictions += predict(sample_processed, 'past')
    return sum_predictions

def parse_input(input_path):
    with open(input_path, 'r') as file:
        data = [np.fromstring(line, dtype=int, sep=' ') for line in file]
    return data

def main():
    dataset = parse_input('input.txt')
    print("Part 1: ", part_1(dataset)) # 2008960228
    print("Part 2: ", part_2(dataset)) # 1097

if __name__ == '__main__':
    main()
