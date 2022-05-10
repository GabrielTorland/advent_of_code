with open("./input.in") as f:
    f.readline()
    buses = [(i, int(bus)) for i, bus in enumerate(f.readline().split(",")) if bus != "x"]

timestamp = 0
step = buses[0][1]
for i, bus_id in buses[1:]:
    while True:
        if (timestamp + i) % bus_id == 0:
            step *= bus_id
            break
        timestamp += step
print(timestamp)