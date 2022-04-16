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

velocity_vectors = set()

# Check if probe has reached the trajectory.
def xy_in_target(x, y, dx, dy):
    if (y < y_min or x > x_max):
        return False
    elif (y<=y_max and x >= x_min):
        velocity_vectors.add((dx, dy))
        return False
    else:
        return True

for dx in range(1, 1000):
    # All values above or equal y_min will miss.
    for dy in range(y_min, abs(y_min)):
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
            running = xy_in_target(pos[0], pos[1], dx, dy)
           
print(len(velocity_vectors))
