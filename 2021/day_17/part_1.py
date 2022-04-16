
# Directions x, y
# Vectors for direction as (dx, dy)
# -y is down

# The probe's x position increases by its x velocity.
# The probe's y position increases by its y velocity.
# Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if it is greater than 0, increases by 1 if it is less than 0, or does not change if it is already 0.
# Due to gravity, the probe's y velocity decreases by 1.

# Input data
x_min = 32
x_max = 65
y_min = -225
y_max = -177


y_distance = set()

# Check if probe has reached the trajectory.
def y_in_target(y, dy):
    if (y < y_min):
        return False
    elif (y<=y_max):
        y_distance.add(sum(list(range(1, dy+1, 1))))
        return False
    else:
        return True

# Only need to calculate the dx that stop moving in the trajectory.
for dx in [i for i in range(100) if x_min <= sum(range(1, i+1, 1)) <= x_max]:
    # All values above or equal y_min will miss.
    for dy in range(1, abs(y_min)):
        pos = [0, 0]        
        velocity = [dx, dy]
        running = True
        while running:
            # Update position
            pos[0] += velocity[0]
            pos[1] += velocity[1]
            # x rules
            if velocity[0] > 0:
                velocity[0] -= 1
            elif velocity[0] < 0:
                velocity[0] += 1
            # y rules   
            velocity[1] -= 1 # gravity
            running = y_in_target(pos[1], dy)
           
print(max(y_distance))

# Or we could simply:
print(sum(list(range(1, abs(y_min)))))

