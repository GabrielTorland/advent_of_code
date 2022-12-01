import os, sys


if __name__ == "__main__":
    print(max([sum([int(c) for c in l.split("\n")]) for l in open(sys.argv[1] if len(sys.argv) > 1 else "input.in", "r").read().split("\n\n")]))