import sys, math, re, random
from collections import defaultdict, Counter

from numpy import imag

class Tile:
    def __init__(self, id):
        self.id = id

        # Possible neighboors, later set to the actual neighboors
        self.tile_up = set()
        self.tile_down = set()
        self.tile_left = set()
        self.tile_right = set()

        # Tile states
        self.validated = False
        self.corner_tile = False
        self.rotations = 0
        self.flipped = False

        # Match equal sides
        self.horizontl_1 = set()
        self.horizontl_2 = set()
        self.vertical_1 = set()
        self.vertical_2 = set()

        # Tile
        self.tile = []

    def associated_sides(self, sides_map):
        """Stores each tile side as a tuple in a dictionary.

        Args:
            sides_map (_dict_): _key: tuple(sides of the tile), value: tile ids._
        """        
        key = tuple(row[0] for row in self.tile)
        self.vertical_1.add(key)
        sides_map[key].add(self.id)
        key = tuple(row[0] for row in self.tile[::-1])
        self.vertical_1.add(key)
        sides_map[key].add(self.id)

        key = tuple(row[len(row)-1] for row in self.tile[::-1])
        self.vertical_2.add(key)
        sides_map[key].add(self.id)
        key = tuple(row[len(row)-1] for row in self.tile)
        self.vertical_2.add(key)
        sides_map[key].add(self.id)

        key = tuple(entry for entry in self.tile[0][::-1])
        self.horizontl_1.add(key)
        sides_map[key].add(self.id)
        key = tuple(entry for entry in self.tile[0])
        self.horizontl_1.add(key) 
        sides_map[key].add(self.id)

        key = tuple(entry for entry in self.tile[len(self.tile)-1])
        self.horizontl_2.add(key)
        sides_map[key].add(self.id)
        key = tuple(entry for entry in self.tile[len(self.tile)-1][::-1])
        self.horizontl_2.add(key) 
        sides_map[key].add(self.id)


    def find_distinct_neighbors(self, sides_map, tiles_map):
        """Removes tiles id from associated sides, and store it as the tile neighboor.
           Mark that their are only one possible neighboor on each side(Except coner tiles and edges).

        Args:
            sides_map (_dict_): _key: sides of tile, value: tile ids_
            tiles_map (_dict_): _key: tile id, value: tile object_ 

        Returns:
            _int_: _if it's 2, the tile is a corner, otherwise it's not._
        """        
        count = 0
        for key in self.vertical_1:
            neighboor = sides_map[key]
            if len(neighboor) >= 2:
                self.tile_left = self.tile_left.union(neighboor.difference({self.id}))
        if len(self.tile_left) == 0:
            self.tile_left = None
            count += 1
        else:
            self.tile_left = tiles_map[self.tile_left.pop()]
        for key in self.vertical_2:
            neighboor = sides_map[key]
            if len(neighboor) >= 2:
                self.tile_right = self.tile_right.union(neighboor.difference({self.id}))
        if len(self.tile_right) == 0:
            self.tile_right = None
            count += 1
        else:
            self.tile_right = tiles_map[self.tile_right.pop()]
        for key in self.horizontl_1:
            neighboor = sides_map[key]
            if len(neighboor) >= 2:
                self.tile_up = self.tile_up.union(neighboor.difference({self.id}))
        if len(self.tile_up) == 0:
            self.tile_up = None
            count += 1
        else:
            self.tile_up = tiles_map[self.tile_up.pop()]
        for key in self.horizontl_2:
            neighboor = sides_map[key]
            if len(neighboor) >= 2:
                self.tile_down = self.tile_down.union(neighboor.difference({self.id}))
        if len(self.tile_down) == 0:
            self.tile_down = None
            count += 1
        else:
            self.tile_down = tiles_map[self.tile_down.pop()]
        return count

    def rotate(self):
        """Rotating tile counterclockwise 90 degrees.
        """        
        left = self.tile_left
        right = self.tile_right
        up = self.tile_up 
        down = self.tile_down

        self.tile_left = up
        self.tile_down = left
        self.tile_right = down
        self.tile_up = right

        self.rotations = (self.rotations + 1)

    def flip(self):
        """Flipping tile.
        """        
        up = self.tile_up 
        down = self.tile_down

        self.tile_down = up
        self.tile_up = down
        self.flipped = True

    def orientate_corner_tile(self, depth):
        """Rotating and flipping tile untill a possible orientation is found.

        Args:
            depth (_int_): _There are only 8 possible orientations_

        Returns:
            _bool_: _True if an orientation was found_
        """        
        if depth == 4:
            self.flip()
        elif depth == 8:
            return False
        if self.tile_left == None:
            if self.tile_up != None:
                if self.tile_up.validated and self.tile_up.tile_down != None:
                    if self.tile_up.tile_down.id == self.id:
                        return True
            else:
                if not self.tile_right.validated and not self.tile_down.validated:
                    return True
        self.rotate()
        self.orientate_corner_tile(depth+1)

    def orientate_right(self, depth):
        """Rotating and flipping tile untill a possible orientation is found.

        Args:
            depth (_int_): _There are only 8 possible orientations_

        Returns:
            _bool_: _True if an orientation was found_
        """ 
        if depth == 4:
            self.flip()
        elif depth == 8:
            return False
        if self.tile_left != None:
            if self.tile_left.validated and self.tile_left.tile_right != None:
                if self.tile_left.tile_right.id == self.id:
                    if self.tile_up != None:
                        if self.tile_up.validated and self.tile_up.tile_down != None:
                            if self.tile_up.tile_down.id == self.id:
                                return True
                    else:
                        # Right corner
                        if self.tile_right != None and self.tile_down != None:
                            if (not self.tile_right.validated) and (not self.tile_down.validated):
                                return True
                        elif self.tile_down != None and self.tile_right == None:
                            if not self.tile_down.validated:
                                return True
        self.rotate()
        self.orientate_right(depth+1)

    def orientate(self, depth, corner_state=False):
        """Differrent orientations for corner tiles and right tiles.

        Args:
            corner_state (bool, optional): _True if the tile is a corner tile_. Defaults to False.
        """        
        if corner_state:
            return self.orientate_corner_tile(depth)
        else:
            return self.orientate_right(depth)
        
    def update_rotation(self, i):
        """Rotate tile, flip if i equal 3.

        Args:
            i (_int_): _Indicator of how many times rotated_
        """        
        new_tile = []
        for x in range(len(self.tile)):
            for y in range(len(self.tile)):
                for c in self.tile[y][len(self.tile)-1-x]:
                    if y > len(new_tile)-1:
                        new_tile.append([])
                    new_tile[x].append(c)
        if i == 3:
            new_tile = new_tile[::-1]
        self.tile = new_tile
        
        
    


def parse():
    infile = sys.argv[1] if len(sys.argv) > 1 else "input.in"
    tiles = []
    sides_map = defaultdict(lambda: set())
    for line in open(infile).readlines():
        if "Tile" in line:
            id = line.split(" ")[1]
            tile = Tile(int(id[:len(id)-2]))
            continue
        if line.strip() == "":
            tile.associated_sides(sides_map)
            tiles.append(tile)
            continue
        tile.tile.append(list(line.strip()))
    tile.associated_sides(sides_map)
    tiles.append(tile)
    return tiles, sides_map

def find_all_distinct_neighboors(tiles, sides_map, tiles_map):
    corners = list()
    for tile in tiles:
        if tile.find_distinct_neighbors(sides_map, tiles_map) == 2:
            corners.append(tile)
            tile.corner_tile = True
    return corners

def flip_tiles(tile, depth, start_tile, l):
    """_summary_

    Args:
        tile (_Tile object_): _Initially this is the corner tile_
        depth (_int_): _Recursive depth_
        start_tile (_Tile object_): _Needed to validate right untill end, then down, then right untill end..._
        l (_int_): _Length of one of the sides on the image_

    Returns:
        _bool_: _True if all tiles was orientated correctly_
    """    
    state = False
    for w in range(2):
        if depth % (l) == 0:
            if w == 0:
                    tile.orientate(0, True)
            elif depth == 0:
                left = tile.tile_left
                right = tile.tile_right
                up = tile.tile_up
                down = tile.tile_down

                tile.tile_up = left
                tile.tile_left = up
                tile.tile_down = right
                tile.tile_right = down
        else:
            if w == 0:
                tile.orientate(0)
            else:
                break
        tile.validated = True
        for i in range(8):
            if i > 0:
                tile.update_rotation(i-1)
            clear = True
            if depth != 0:
                if tile.tile_up != None:
                    if tuple(tile.tile[0]) != tuple(tile.tile_up.tile[len(tile.tile)-1]):
                        clear = False
                if tile.tile_left != None:
                    if tuple([row[0] for row in tile.tile]) != tuple([row[len(tile.tile)-1] for row in tile.tile_left.tile]):
                        clear = False
            if clear:
                if tile.tile_right != None:
                    if flip_tiles(tile.tile_right, depth+1, start_tile, l):
                        return True
                elif start_tile.tile_down != None:
                    if flip_tiles(start_tile.tile_down, depth+1, start_tile.tile_down, l):
                        return True
                else:
                    return True
         
    
    if not state:
        # Flip horizontally
        new_tile = []
        for y in range(len(tile.tile))[::-1]:
            for x in range(len(tile.tile)):
                if x > len(new_tile)-1:
                    new_tile.append([])
                new_tile[x].append(tile.tile[x][y])
        tile.tile = new_tile
        tile.validated = False
        return False


def create_image_list(corner_tile, l):
    """Convert tree structure to a 2d list.

    Args:
        corner_tile (_Tile object_): _initially corner tile_
        l (_int_): _length of side of the image_

    Returns:
        _list_: _2d list of image_
    """    
    image_list = []
    start_tile = corner_tile
    current_tile = corner_tile
    for i in range(l):
        for t in range(len(corner_tile.tile)):
            image_list.append(list())
        for j in range(l):        
            x = 0
            for row in current_tile.tile:
                image_list[i*len(corner_tile.tile)+x] += row
                x += 1

            current_tile = current_tile.tile_right if current_tile.tile_right != None else start_tile.tile_down
        start_tile = start_tile.tile_down
    return image_list      


def store_image(image_map, infile):
    # Clear file
    file = open(infile,"w")
    file.close()
    # Store image
    with open(infile, 'w') as f:
        for row in image_map:
            temp = "".join([c for c in row]) + '\n'
            f.write(temp)

def remove_boarders(tiles):
    for tile in tiles:
        new_tile = []
        for x in range(len(tile.tile)):
            if x != 0 and x != len(tile.tile)-1:
                new_tile.append([])
            for y in range(len(tile.tile)):
                if x != 0 and x != len(tile.tile)-1 and y != 0 and y != len(tile.tile)-1:
                    new_tile[x-(2 if x == len(tile.tile)-1 else 1)].append(tile.tile[x][y])
        tile.tile = new_tile

def rotate_image(image):
    # Rotate 2d list 90 degrees
    return [list(i) for i in zip(*image[::-1])]

def flip_image(image):
    # Flip 2d list
    return image[::-1]

def mark_seamonster(image, seamonsters, l):
    for seamonster in seamonsters:
        index = seamonster.start(0)
        # start
        image[index//len(image)][index % len(image)] = "O"
        # 5 between
        image[(index+(l-19+1))//len(image)][(index+(l-19+1)) % len(image)] = "O"
        # 4 between
        image[(index+(l-19+1)+5)//len(image)][(index+(l-19+1)+5) % len(image)] = "O"
        image[(index+(l-19+1)+6)//len(image)][(index+(l-19+1)+6) % len(image)] = "O"
        # 4 between
        image[(index+(l-19+1)+11)//len(image)][(index+(l-19+1)+11) % len(image)] = "O"
        image[(index+(l-19+1)+12)//len(image)][(index+(l-19+1)+12) % len(image)] = "O"
        # 4 between
        image[(index+(l-19+1)+17)//len(image)][(index+(l-19+1)+17) % len(image)] = "O"
        image[(index+(l-19+1)+18)//len(image)][(index+(l-19+1)+18) % len(image)] = "O"
        image[(index+(l-19+1)+19)//len(image)][(index+(l-19+1)+19) % len(image)] = "O"
        # 5 between
        image[(index+2*(l-19+1)+19)//len(image)][(index+2*(l-19+1)+19) % len(image)] = "O"
        # 2 between
        image[(index+2*(l-19+1)+22)//len(image)][(index+2*(l-19+1)+22) % len(image)] = "O"
        # 2 between
        image[(index+2*(l-19+1)+25)//len(image)][(index+2*(l-19+1)+25) % len(image)] = "O"
        # 2 between
        image[(index+2*(l-19+1)+28)//len(image)][(index+2*(l-19+1)+28) % len(image)] = "O"
        # 2 between
        image[(index+2*(l-19+1)+31)//len(image)][(index+2*(l-19+1)+31) % len(image)] = "O"
        # 2 between
        image[(index+2*(l-19+1)+34)//len(image)][(index+2*(l-19+1)+34) % len(image)] = "O"

def create_regex(l):
    tmp = "#.{O}#.{O}##.{O}##.{O}###.{O}#.{O}#.{O}#.{O}#.{O}#.{O}#"
    spaces = [l-19, 4, 4, 4, l-19, 2, 2, 2, 2, 2][::-1]
    regex = r""
    for line in tmp.split("O"):
        regex += line
        if line[len(line)-1] == '{':
            regex += f"{spaces.pop()}"

    return re.compile(regex)
     

def count_seamonsters(image):
    l = len(image)
    pattern = create_regex(l)
    fail = True
    for i in range(8):
        line = ""
        for row in image:
            line += "".join([c for c in row])       
        result = pattern.findall(line)
        if len(result) > 0:
            mark_seamonster(image, pattern.finditer(line), l)
            # Have to search twice because of overlapping matches(Not direct overlap but same row)
            line = ""
            for row in image:
                line += "".join([c for c in row])       
            mark_seamonster(image, pattern.finditer(line), l)
            store_image(image, "result.txt")
            fail = False
            break
        image = rotate_image(image)
        if i == 3:
            image = flip_image(image)
    if fail:
        print("Error!")
        store_image(image, "result.txt")
    return image

def multiply_corners(corner_tiles):
    p1 = 1
    for x in corner_tiles:
        p1 *= x.id
    return p1


# Construct image
tiles, sides_map = parse()
tiles_map = {tile.id: tile for tile in tiles}
corner_tiles = find_all_distinct_neighboors(tiles, sides_map, tiles_map)
corner_tile = random.choice(corner_tiles)
flip_tiles(corner_tile, 0, corner_tile, int(math.sqrt(len(tiles))))

# Store image
image_list = create_image_list(corner_tile, int(math.sqrt(len(tiles))))
store_image(image_list, "image.txt")
remove_boarders(tiles)
image_list = create_image_list(corner_tile, int(math.sqrt(len(tiles))))

# Find seamonsters
image_list = count_seamonsters(image_list)
free_water = Counter([c for row in image_list for c in row])['#']

print("part 1:", multiply_corners(corner_tiles))

print("Part 2:", free_water)