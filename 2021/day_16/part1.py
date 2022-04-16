# VVVTTTAAAAABBBBBCCCCC
# 1 - not last group
# 0 - last group
# Packet type ID 4: packet is a literal value, otherwise the packet is an operator(worry later) or  more subpackets.
# Literal value is AAAABBBBCCCC (remove prefix 1).

# If the length type ID is 0, then the next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet.
# If the length type ID is 1, then the next 11 bits are a number that represents the number of sub-packets immediately contained by this packet.

with open("./raw.txt") as fin:
    raw_data = fin.read().strip()


data = "".join(bin(int(c, base=16))[2:].zfill(4) for c in raw_data)

def parse(bitstring, i, count=-1):
    if i >= len(bitstring) or int(bitstring[i:], 2) == 0:
        return 0
    v = int(bitstring[i:i+3], 2)
    tId = int(bitstring[i+3:i+6], 2)
    if tId == 4: # Literal value
        result = ""
        count_ = 0
        while bitstring[i+6+count_*5] != "0":
            result += bitstring[i+7+count_*5:11+i+count_*5]
            count_ += 1
        result += bitstring[i+7+count_*5:i+11+count_*5]
        return v + parse(bitstring, i+11+5*count_, count-1)
    else:
        lenTypId = bitstring[i+6]
        if lenTypId == '0':
            bitSize = int(bitstring[i+7:i+22], 2)
            return v + parse(bitstring, i+22, count-1) 
        else:
            subPacketCount = int(bitstring[i+8:i+18], 2)
            return v + parse(bitstring, i+18, count=subPacketCount)
        

print(parse(data, 0))

