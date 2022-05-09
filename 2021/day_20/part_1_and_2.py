from re import I
import sys
from collections import Counter, defaultdict

def parse():
    infile = sys.argv[1] if len(sys.argv) > 1 else 'input.in'
    with open(infile, 'r') as f:
        data = f.read().split('\n')
    return data[0], [['1' if elem == '#' else '0' for elem in tmp]for tmp in data[2:]]


def output_image(image, enhancement_alg, n):
    current_image = image
    for w in range(n):
        new_image = []

        for x in range(-1, len(current_image)+1):
            new_image.append([])
            for y in range(-1, len(current_image)+1):
                output_pixel = ""
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if 0 <= x + i <= len(current_image)-1 and 0 <= y + j <= len(current_image)-1:
                            output_pixel += current_image[x+i][y+j]
                        else:
                            # All prixels around switch between # and .
                            if w % 2 == 0:
                                output_pixel += '0'
                            else:
                                output_pixel += '1'
                new_image[x+1].append(enhancement_alg[int(output_pixel, 2)])
        
        current_image = new_image
    return current_image


if __name__ == '__main__':
    enhancement_alg, image = parse()
    outputs = [Counter([y for x in output_image(image, enhancement_alg.replace('#', '1').replace('.', '0'), i) for y in x])['1'] for i in [2, 50]]
    print("Part 1: ", outputs[0])
    print("Part 2: ", outputs[1])