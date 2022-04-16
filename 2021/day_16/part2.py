# VVVTTTAAAAABBBBBCCCCC
# 1 - not last group
# 0 - last group
# Packet type ID 4: packet is a literal value, otherwise the packet is an operator(worry later) or  more subpackets.
# Literal value is AAAABBBBCCCC (remove prefix 1).

# If the length type ID is 0, then the next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet.
# If the length type ID is 1, then the next 11 bits are a number that represents the number of sub-packets immediately contained by this packet.

import numpy as np

with open("./raw.txt") as fin:
    raw_data = fin.read().strip()

data = "".join(bin(int(c, base=16))[2:].zfill(4) for c in raw_data)

def parse(bitstring, i):
    # Result is where literal values are stored.
    result = list()

    # Return empty list if the end of the bitstring is reached or only zeros left.
    if i >= len(bitstring) or int(bitstring[i:], 2) == 0:
        return -1
    
    # Packet version
    v = int(bitstring[i:i+3], 2)
    # Packet type ID
    tId = int(bitstring[i+3:i+6], 2)

    if tId == 4: # Literal value
        # temp values
        number = ""
        count = 0
        # Extracting literal value.
        while bitstring[i+6+count*5] != "0":
            number += bitstring[i+7+count*5:11+i+count*5]
            count += 1
        number += bitstring[i+7+count*5:i+11+count*5]
        
        return int(number, 2), i+11+5*count
    else:
        # Length type ID
        lenTypId = bitstring[i+6]
        
        if lenTypId == '0':
            current_index = i+22
            bitSize = int(bitstring[i+7:i+22], 2)
            # Extracting subpackets based on bit size of packets.
            while (current_index - (i+22)) != bitSize:
                literal_value, next_index = parse(bitstring, current_index)
                if literal_value == -1:
                    continue
                current_index = next_index
                result.append(literal_value)
        else:
            current_index = i+18
            subPacketCount = int(bitstring[i+7:i+18], 2)
            # Extracting subpackets based on subpacket count.
            for i in range(subPacketCount):
                literal_value, next_index = parse(bitstring, current_index)
                if literal_value == -1:
                    continue
                current_index = next_index
                result.append(literal_value)
        # Sum packets
        if tId == 0:
            return sum(result), current_index
        # multilying together literal values.
        elif tId == 1:
            ans = 1
            for item in result:
                ans *= item
            return ans, current_index
        # Minimum of literal values.
        elif tId == 2:
            return min(result), current_index
        # Maximum of literal values.
        elif tId == 3:
            return max(result), current_index 
        # First literal value grater than second literal value.
        elif tId == 5:
            return (1 if result[0] > result[1] else 0), current_index
        # First literal value less than second literal value.
        elif tId == 6:
            return (1 if result[0] < result[1] else 0), current_index
        # First literal value equal to second literal value.
        elif tId == 7:
            return (1 if result[0] == result[1] else 0), current_index 
        

print(parse(data, 0)[0])


