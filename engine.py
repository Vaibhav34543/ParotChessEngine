from ursina import *

# Boredered Square Window
app = Ursina(borderless=False)
window.size = (800, 800)

# Positions stored [white, black]
Positions = [[], []]

# Updates the positions
def ManagePositions(prev_pos, new_pos):
    for i in Positions:
        print(i)
        if prev_pos == i:
            Positions.remove(prev_pos)
            Positions.append(new_pos)
            print(prev_pos)

# Destroys the hovers
def destroyHovers():
    for i in scene.entities:
        if i.name == "hover":
            destroy(i)
            destroyHovers()

# Checks if a piece collides with its own class
def CheckPosCollide(pos, player = "white"):
    if player == "black":
        for i in Positions[1]:
            if i == pos:
                return True
    else:
        for i in Positions[0]:
            if i == pos:
                return True

# Creates hovers for movements on clicking
# any of the hovers the piece is moved to that hovers location
class Hover(Button):
    def __init__(self, x, y, prnt):
        super().__init__(
            model='plane',
            parent=prnt,
            texture = 'hover',
            position = (x, 0.02, y),
            color = color.white
        )

    def input(self, key):
        if self.hovered:
            if key == "left mouse down":
                # Updates the position in the Positions[]
                ManagePositions([int(self.parent.parent.x), int(self.parent.parent.y)], [int(self.parent.parent.x + self.x), int(self.parent.parent.y + self.z)])
                self.parent.parent.position = (self.parent.parent.x + self.x, self.parent.parent.y + self.z, self.parent.parent.z)
                
                # Destroys all hovers at the end after clicking
                destroy(self.parent)

# Creates the board
class Board(Button):
    def __init__(self):
        super().__init__(
            model='plane',
            parent=scene,
            scale = 8,
            rotation_x = -90,
            texture = 'boardN',
            position=(3.5, 3.5, 0),
            origin = (0, 0, 0),
            color=color.white
        )

    # on click on board delete hovers
    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                destroyHovers()

# Handling Bishop Hovers
def BishopManager(bishop, h_parent):
    # Checks how many pieces can diagonally be moved
    right = int(8 - bishop.x)
    top = int(8 - bishop.y)
    left = int(bishop.x + 1)
    bottom = int(bishop.y + 1)
    for i in range(1, min(top, right)):
        if CheckPosCollide([bishop.x + i, bishop.y + i])!=True:
            Hover(i, i, h_parent)
        else:
            break
    for i in range(1, min(top, left)):
        if CheckPosCollide([bishop.x - i, bishop.y + i])!=True:
            Hover(-i, i, h_parent)
        else:
            break
    for i in range(1, min(left, bottom)):
        if CheckPosCollide([bishop.x - i, bishop.y - i])!=True:
            Hover(-i, -i, h_parent)
        else:
            break
    for i in range(1, min(bottom, right)):
        if CheckPosCollide([bishop.x + i, bishop.y - i])!=True:
            Hover(i, -i, h_parent)
        else:
            break

# Handling Rook Hovers
def RookManager(rook, h_parent):
    # Checking for clamp values
    right = int(8 - rook.x)
    top = int(8 - rook.y)
    left = int(rook.x + 1)
    bottom = int(rook.y + 1)
    for i in range(1, right):
        if CheckPosCollide([rook.x + i, rook.y])!=True:
            Hover(i, 0, h_parent)
        else:
            break
    for i in range(1, left):
        if CheckPosCollide([rook.x - i, rook.y])!=True:
            Hover(-i, 0, h_parent)
        else:
            break
    for i in range(1, top):
        if CheckPosCollide([rook.x, rook.y + i])!=True:
            Hover(0, i, h_parent)
        else:
            break
    for i in range(1, bottom):
        if CheckPosCollide([rook.x, rook.y - i])!=True:
            Hover(0, -i, h_parent)
        else:
            break

# Check for knight hovers
def KnightManager(knight, h_parent):
    # Kind of complicated but all it does is 
    # Checks for the L shaped positions if they are in board 
    # and then adds them to hovers
    if int(knight.y + 2) <= 7 and int(knight.x + 1) <= 7:
        if CheckPosCollide([knight.x+1, knight.y+2]) != True:
            Hover(1, 2, h_parent) 
    if int(knight.y + 2) <= 7 and int(knight.x - 1) >= 0:
        if CheckPosCollide([knight.x -1, knight.y +2]) != True:
            Hover(-1, 2, h_parent) 
    if int(knight.y + 1) <= 7 and int(knight.x + 2) <= 7:
        if CheckPosCollide([knight.x +2, knight.y+1]) != True:
            Hover(2, 1, h_parent) 
    if int(knight.y - 1) >= 0 and int(knight.x + 2) <= 7:
        if CheckPosCollide([knight.x+2, knight.y-1]) != True:
            Hover(2, -1, h_parent) 
    if int(knight.y + 1) <= 7 and int(knight.x - 2) >= 0:
        if CheckPosCollide([knight.x-2, knight.y+1]) != True:
            Hover(-2, 1, h_parent) 
    if int(knight.y - 1) >= 0 and int(knight.x - 2) >= 0:
        if CheckPosCollide([knight.x-2, knight.y-1]) != True:
            Hover(-2, -1, h_parent) 
    if int(knight.y - 2) >= 0 and int(knight.x + 1) <= 7:
        if CheckPosCollide([knight.x+1, knight.y-2]) != True:
            Hover(1, -2, h_parent) 
    if int(knight.y - 2) >= 0 and int(knight.x - 1) >= 0:
        if CheckPosCollide([knight.x-1, knight.y-2]) != True:
            Hover(-1, -2, h_parent)

# Handling King's hovers
class King(Button):
    def __init__(self, x, y, txtr):
        super().__init__(
            model='plane',
            parent=scene,
            texture = txtr,
            rotation_x = -90,
            position = (x, y, -0.01),
            color = color.white
        )
        if str(self.texture) == "kingW.png":
            Positions[0].append([x, y])
        else:
            Positions[1].append([x, y])

    def input(self, keys):
        if self.hovered:
            if keys == "left mouse down":
                # c[] simply consists all values 
                # that when passed in hover function
                # checks all 8 squares around the king
                x = Entity(parent = self, origin = (0, 0, 0))
                c = [[0, 1], [1, 1], [-1, 1], [1, 0], [-1, 0], [-1, -1], [0, -1], [1, -1]]
                for i in c:
                    if CheckPosCollide([self.x + i[0], self.y + i[1]]) != True:
                        if self.y + i[1] < 0:
                            continue
                        if self.x + i[0] < 0:
                            continue
                        if self.y + i[1] > 7:
                            continue
                        if self.x + i[0] > 7:
                            continue
                        else:
                            Hover(i[0], i[1], x)
                if x.hovered:
                    if keys == "left mouse down":
                       destroy(x)

# Handling Pawn Hovers
class Pawn(Button):
    def __init__(self, x, y, textr):
        super().__init__(
            model='plane',
            parent=scene,
            texture = textr,
            rotation_x = -90,
            position = (x, y, -0.01),
            color = color.white
        )
        if str(self.texture) == "pawnW.png":
            Positions[0].append([x, y])
        else:
            Positions[1].append([x, y])

    def input(self, keys):
        if self.hovered:
            if keys == 'left mouse down':
                x = Entity(parent = self, origin = (0, 0, 0))
                print(self.texture)
                
                # if the pawn is a black pawn
                if str(self.texture) == "pawnB.png":
                    # performing downward direction hovers
                    if self.y == 6:
                        if CheckPosCollide([self.x, self.y - 1]) != True:
                            Hover(0, -1, x)
                            if CheckPosCollide([self.x, self.y - 2]) != True:
                                Hover(0, -2, x)
                    
                    elif CheckPosCollide([self.x, self.y - 1]) != True:
                        Hover(0, -1, x)

                # if the pawn is a white pawn
                elif str(self.texture) == "pawnW.png":
                    # performing upward direction hovers
                    if self.y == 1:
                        if CheckPosCollide([self.x, self.y + 1]) != True:
                            Hover(0, 1, x)
                            if CheckPosCollide([self.x, self.y + 2]) != True:
                                Hover(0, 2, x)
                    
                    elif CheckPosCollide([self.x, self.y + 1]) != True:
                        Hover(0, 1, x)

# Bishop Hovers
class Bishop(Button):
    def __init__(self, x, y, textr):
        super().__init__(
            model='plane',
            parent=scene,
            texture = textr,
            rotation_x = -90,
            position = (x, y, -0.01),
            color = color.white
        )
        if str(self.texture) == "bishopW.png":
            Positions[0].append([x, y])
        else:
            Positions[1].append([x, y])

    def input(self, keys):
        if self.hovered:
            if keys == 'left mouse down':
                x = Entity(parent = self, origin = (0, 0, 0))
                BishopManager(self, x)

# Rook hovers
class Rook(Button):
    def __init__(self, x, y, textr):
        super().__init__(
            model='plane',
            parent=scene,
            texture = textr,
            rotation_x = -90,
            position = (x, y, -0.01),
            color = color.white
        )
        if str(self.texture) == "rookW.png":
            Positions[0].append([x, y])
        else:
            Positions[1].append([x, y])

    def input(self, keys):
        if self.hovered:
            if keys == 'left mouse down':
                x = Entity(parent = self, origin = (0, 0, 0))
                RookManager(self, x)

# queen hovers
class Queen(Button):
    def __init__(self, x, y, textr):
        super().__init__(
            model='plane',
            parent=scene,
            texture = textr,
            rotation_x = -90,
            position = (x, y, -0.01),
            color = color.white
        )
        if str(self.texture) == "queenW.png":
            Positions[0].append([x, y])
        else:
            Positions[1].append([x, y])

    def input(self, keys):
        if self.hovered:
            if keys == 'left mouse down':
                x = Entity(parent = self, origin = (0, 0, 0))
                RookManager(self, x)
                BishopManager(self, x)

# Knight hovers
class Knight(Button):
    def __init__(self, x, y, textr):
        super().__init__(
            model='plane',
            parent=scene,
            texture = textr,
            rotation_x = -90,
            position = (x, y, -0.01),
            color = color.white
        )
        if str(self.texture) == "knightW.png":
            Positions[0].append([x, y])
        else:
            Positions[1].append([x, y])


    def input(self, keys):
        if self.hovered:
            if keys == 'left mouse down':
                x = Entity(parent = self, origin = (0, 0, 0))
                KnightManager(self, x)

# Pawn Hovers
class Pawn(Button):
    def __init__(self, x, y, textr):
        super().__init__(
            model='plane',
            parent=scene,
            texture = textr,
            rotation_x = -90,
            position = (x, y, -0.01),
            color = color.white
        )
        if str(self.texture) == "pawnW.png":
            Positions[0].append([x, y])
        else:
            Positions[1].append([x, y])

    def input(self, keys):
        if self.hovered:
            if keys == 'left mouse down':
                x = Entity(parent = self, origin = (0, 0, 0))
                print(self.texture)
                if str(self.texture) == "pawnB.png":
                    print("check") 
                    if self.y == 6:
                        if CheckPosCollide([self.x, self.y - 1]) != True:
                            Hover(0, -1, x)
                            if CheckPosCollide([self.x, self.y - 2]) != True:
                                Hover(0, -2, x)
                    
                    elif CheckPosCollide([self.x, self.y - 1]) != True:
                        Hover(0, -1, x)
                elif str(self.texture) == "pawnW.png":
                    if self.y == 1:
                        if CheckPosCollide([self.x, self.y + 1]) != True:
                            Hover(0, 1, x)
                            if CheckPosCollide([self.x, self.y + 2]) != True:
                                Hover(0, 2, x)
                    
                    elif CheckPosCollide([self.x, self.y + 1]) != True:
                        Hover(0, 1, x)

# Creating the board
class Board(Button):
    def __init__(self):
        super().__init__(
            model='plane',
            parent=scene,
            scale = 8,
            rotation_x = -90,
            texture = 'boardN',
            position=(3.5, 3.5, 0),
            origin = (0, 0, 0),
            color=color.white
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                destroyHovers()


board = Board()

for i in range(0, 8):
    Pawn(i, 1, 'pawnW')
for i in range(0, 8):
    Pawn(i, 6, 'pawnB')
k = King(4, 0, 'kingW')
kb = King(4, 7, 'kingB')
q = Queen(3, 0, 'queenW')
qb = Queen(3, 7, 'queenB')
b = Bishop(2, 0, 'bishopW')
bb = Bishop(2, 7, 'bishopB')
b2 = Bishop(5, 0, 'bishopW')
b2b = Bishop(5, 7, 'bishopB')
Kn = Knight(1, 0, 'knightW')
Knb = Knight(1, 7, 'knightB')
Kn2 = Knight(6, 0, 'knightW')
Kn2b = Knight(6, 7, 'knightB')
r = Rook(0, 0, 'rookW')
rb = Rook(0, 7, 'rookB')
r2 = Rook(7, 0, 'rookW')
r2b = Rook(7, 7, 'rookB')

cam = EditorCamera(orthographic_lens_mode = False)
cam.position = (3.5, 3.5, -1)
app.run()