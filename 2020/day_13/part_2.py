import sys
import math

def parse():
    infile = sys.argv[1] if len(sys.argv) > 1 else "input.in"
    return [line.strip().split(',') for i, line in enumerate(open(infile).readlines()) if i > 0][0]

def multiply_parameters(b, N, x_i):
    return b*N*x_i

# Euclidean Algorithm https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/the-euclidean-algorithm
# (A * A^-1) ≡ 1 (mod C)
# Only the numbers coprime to C (numbers that share no prime factors with C) have a modular inverse (mod C)
# If A = B⋅Q + R and B≠0 then GCD(A,B) = GCD(B,R)
# Calculate the gcd of the two input values in a efficient manner by splitting up the numbers into two smaller numbers.
def fast_inverse_calculation(x, n):
    a = 1
    b = 0

    while x != n:

        if x < n:
            temp = n // x
            if n - x * temp == 0:
                temp = 1
            n -= x * temp
            b -= a * temp
        else:
            temp = x // n
            if x - n * temp == 0:
                temp = 1
            x -= n * temp
            a -= b * temp
    if x > 1 or n > 1:
        # They are not coprime(No inverse)
        print("The gcd of x and n is not 1")
    return a

# Chinese remainder theorem
# https://en.wikipedia.org/wiki/Chinese_remainder_theorem
def find_earliest_waiting_time(data_):
    # b_i: remainders of the modulo operations
    b_i = list()
    # Mod values
    data = list()
    for i, c in enumerate(data_):
        if c != 'x':
            number = int(c)
            b_i.append((number-i) % number)
            data.append(number)
    N = 1
    for number in data:
        N *= number
    # x_i: i*N/N_i*x_i <=> 1*i mod(mod_i)
    # i multiplied on both sides to get 1*x_i on the left side.
    # Thus x_i <=> i*x_i mod(mod_i)
    x_i = [fast_inverse_calculation(i, b) for i, b in zip([N//n for n in data], data)]

    # Slow method of calculating the inverse
    #for number in data:
    #    rem = math.inf
    #    i = 1
    #    while rem != 1:
    #        rem = (i*N/number) % number
    #        i += 1
    #    x_i.append((i-1))
    # Had to floor the N/N_i to convert it to long int

    return list(map(multiply_parameters, b_i, [math.floor(N/number) for number in data], x_i)), N

data = parse()
ans = find_earliest_waiting_time(data)
# Reduce the answer to the smallest possible value
print(sum(ans[0]) % (ans[1]))