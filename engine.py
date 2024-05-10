from ursina import *

turn = 0        # 0 - White, 1 - Black


# Checks if it is white's turn or black's
def CheckTurn(piece):
    if returnClass(piece) == "w" and turn == 0:
        return True
    elif returnClass(piece) == "w" and turn == 1:
        return False
    elif returnClass(piece) == "b" and turn == 1:
        return True
    elif returnClass(piece) == "b" and turn == 0:
        return False

# Change Turns
def ChangeTurn(piece):
    global turn
    if returnClass(piece) == "w":
        turn = 1
    else: turn = 0

# Debug
def Log(data):
    with open('ChessLog.txt', 'a') as file:
        file.write(data+"\n")

Log("==================================================================")
Log("==================================================================")
Log("==================================================================")

# Boredered Square Window
app = Ursina(borderless=False)
window.size = (800, 800)

# Positions stored [white, black]
Positions = [[], []]

# Returns the piece class
def returnClass(piece):
    if "W" in str(piece.texture):
        return  "w"
    else:
        return "b"

# Deletes the enemy collided sprite
def deleteCollidedOpp(pos, pieceClass):
    if returnClass(pieceClass) == "w":
        Log("deleteCollidedOpp CALLED: TRUE")
        for i in scene.entities:
            if type(i) == "<class '__main__.Board'>":
                continue
            Log(f"Entity TYPE CHECK : {type(i)}")
            Log(f"deleteCollidedOpp search for {pos} in {i.position}")
            if [int(i.x), int(i.y)] == pos:
                Log("deleteCollidedOpp POSITIONS MATCHED: TRUE")
                if returnClass(i) != returnClass(pieceClass):
                    Log(f"Removing item from {Positions[1]}")
                    Log(f'Position to delete: [{int(i.x)},{int(i.y)}]')
                    Log(f"Destroying {i.name}")
                    Positions[1].remove([int(i.x), int(i.y)])
                    Log(f"New Positions Data: {Positions}")
                    destroy(i)
                    break
    else:
        Log("deleteCollidedOpp CALLED: TRUE")
        for i in scene.entities:
            if type(i) == "<class '__main__.Board'>":
                continue
            Log(f"deleteCollidedOpp search for {pos} in {i.position}")
            if [int(i.x), int(i.y)] == pos:
                Log("deleteCollidedOpp POSITIONS MATCHED: TRUE")
                if returnClass(i) != returnClass(pieceClass):
                    Log(f"Removing item from {Positions[0]}")
                    Log(f'Position to delete: [{int(i.x)},{int(i.y)}]')
                    Log("Destroying matched Entity")
                    Positions[0].remove([int(i.x), int(i.y)])
                    Log(f"New Positions Data: {Positions}")
                    destroy(i)
                    break

# Checks if the opponent positions collide
# Takes in a move and checks if that moves x,y match with both
# the white and black class positions
def checkOppCollisions(move, pieceClass):
    if pieceClass == "w":
        if move in Positions[1]:
            Log(f"{move} FOUND IN {Positions[1]}")
            return True
        else: return False
    else:
        if move in Positions[0]:
            Log(f"{move} FOUND IN {Positions[0]}")
            return True
        else: return False



# Updates the positions
def ManagePositions(prev_pos, new_pos, pClass):
    pClassC = returnClass(pClass)
    if pClassC == "w":
        for i in Positions[0]:
            if prev_pos == i:
                Positions[0].remove(prev_pos)
                Positions[0].append(new_pos)
    else:
        for i in Positions[1]:
            if prev_pos == i:
                Positions[1].remove(prev_pos)
                Positions[1].append(new_pos)

# Destroys the hovers
def destroyHovers():
    for i in scene.entities:
        if i.name == "hover":
            destroy(i)
            destroyHovers()

# Checks if a piece collides with its own class
def CheckPosCollide(pos, pieceClass):
    pos = [int(pos[0]), int(pos[1])]
    if pieceClass == "w":
        if pos in Positions[0]:
            Log(f"Checking {pos} in {Positions[0]}")
            return True
        else: return False
    else:
        if pos in Positions[1]:
            Log(f"Checking {pos} in {Positions[1]}")
            return True
        else: return False

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
                Log(f"Positions: {Positions}")
                old_move = [int(self.parent.parent.x), int(self.parent.parent.y)]
                new_move = [int(self.parent.parent.x + self.x), int(self.parent.parent.y + self.z)]
                # Checks if the new move collides with opponents 
                # Positions array
                if checkOppCollisions(new_move, returnClass(self.parent.parent)):
                    deleteCollidedOpp(new_move, self.parent.parent)
                # Updates the position in the Positions[]
                ManagePositions(old_move, new_move, self.parent.parent)
                self.parent.parent.position = (self.parent.parent.x + self.x, self.parent.parent.y + self.z, self.parent.parent.z)

                
                # Destroys all hovers at the end after clicking
                destroy(self.parent)
                ChangeTurn(self.parent.parent)
                Log(f"Current Turn State: {turn}")


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
        if CheckPosCollide([bishop.x + i, bishop.y + i], returnClass(h_parent.parent))!=True:
            Hover(i, i, h_parent)
        else:
            break
    for i in range(1, min(top, left)):
        if CheckPosCollide([bishop.x - i, bishop.y + i], returnClass(h_parent.parent))!=True:
            Hover(-i, i, h_parent)
        else:
            break
    for i in range(1, min(left, bottom)):
        if CheckPosCollide([bishop.x - i, bishop.y - i], returnClass(h_parent.parent))!=True:
            Hover(-i, -i, h_parent)
        else:
            break
    for i in range(1, min(bottom, right)):
        if CheckPosCollide([bishop.x + i, bishop.y - i], returnClass(h_parent.parent))!=True:
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
        if CheckPosCollide([rook.x + i, rook.y], returnClass(h_parent.parent))!=True:
            Hover(i, 0, h_parent)
        else:
            break
    for i in range(1, left):
        if CheckPosCollide([rook.x - i, rook.y], returnClass(h_parent.parent))!=True:
            Hover(-i, 0, h_parent)
        else:
            break
    for i in range(1, top):
        if CheckPosCollide([rook.x, rook.y + i], returnClass(h_parent.parent))!=True:
            Hover(0, i, h_parent)
        else:
            break
    for i in range(1, bottom):
        if CheckPosCollide([rook.x, rook.y - i], returnClass(h_parent.parent))!=True:
            Hover(0, -i, h_parent)
        else:
            break

# # Check for knight hovers
# def KnightManager(knight, h_parent):
#     # Kind of complicated but all it does is 
#     # Checks for the L shaped positions if they are in board 
#     # and then adds them to hovers
#     if int(knight.y + 2) <= 7 and int(knight.x + 1) <= 7:
#         if CheckPosCollide([knight.x+1, knight.y+2]) != True:
#             Hover(1, 2, h_parent) 
#     if int(knight.y + 2) <= 7 and int(knight.x - 1) >= 0:
#         if CheckPosCollide([knight.x -1, knight.y +2]) != True:
#             Hover(-1, 2, h_parent) 
#     if int(knight.y + 1) <= 7 and int(knight.x + 2) <= 7:
#         if CheckPosCollide([knight.x +2, knight.y+1]) != True:
#             Hover(2, 1, h_parent) 
#     if int(knight.y - 1) >= 0 and int(knight.x + 2) <= 7:
#         if CheckPosCollide([knight.x+2, knight.y-1]) != True:
#             Hover(2, -1, h_parent) 
#     if int(knight.y + 1) <= 7 and int(knight.x - 2) >= 0:
#         if CheckPosCollide([knight.x-2, knight.y+1]) != True:
#             Hover(-2, 1, h_parent) 
#     if int(knight.y - 1) >= 0 and int(knight.x - 2) >= 0:
#         if CheckPosCollide([knight.x-2, knight.y-1]) != True:
#             Hover(-2, -1, h_parent) 
#     if int(knight.y - 2) >= 0 and int(knight.x + 1) <= 7:
#         if CheckPosCollide([knight.x+1, knight.y-2]) != True:
#             Hover(1, -2, h_parent) 
#     if int(knight.y - 2) >= 0 and int(knight.x - 1) >= 0:
#         if CheckPosCollide([knight.x-1, knight.y-2]) != True:
#             Hover(-1, -2, h_parent)

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
        if CheckTurn(self):
            if self.hovered:
                if keys == "left mouse down":
                    Log(f"King Clicked: Positions - {Positions}")
                    Log(f"King Position: {self.position}")
                    # c[] simply consists all values 
                    # that when passed in hover function
                    # checks all 8 squares around the king
                    x = Entity(parent = self, origin = (0, 0, 0))
                    c = [[0, 1], [1, 1], [-1, 1], [1, 0], [-1, 0], [-1, -1], [0, -1], [1, -1]]
                    for i in c:
                        if CheckPosCollide([self.x + i[0], self.y + i[1]], returnClass(self)) != True:
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
# class Pawn(Button):
#     def __init__(self, x, y, textr):
#         super().__init__(
#             model='plane',
#             parent=scene,
#             texture = textr,
#             rotation_x = -90,
#             position = (x, y, -0.01),
#             color = color.white
#         )
#         if str(self.texture) == "pawnW.png":
#             Positions[0].append([x, y])
#         else:
#             Positions[1].append([x, y])

#     def input(self, keys):
#         if self.hovered:
#             if keys == 'left mouse down':
#                 x = Entity(parent = self, origin = (0, 0, 0))
#                 print(self.texture)
                
#                 # if the pawn is a black pawn
#                 if str(self.texture) == "pawnB.png":
#                     # performing downward direction hovers
#                     if self.y == 6:
#                         if CheckPosCollide([self.x, self.y - 1]) != True:
#                             Hover(0, -1, x)
#                             if CheckPosCollide([self.x, self.y - 2]) != True:
#                                 Hover(0, -2, x)
                    
#                     elif CheckPosCollide([self.x, self.y - 1]) != True:
#                         Hover(0, -1, x)

#                 # if the pawn is a white pawn
#                 elif str(self.texture) == "pawnW.png":
#                     # performing upward direction hovers
#                     if self.y == 1:
#                         if CheckPosCollide([self.x, self.y + 1]) != True:
#                             Hover(0, 1, x)
#                             if CheckPosCollide([self.x, self.y + 2]) != True:
#                                 Hover(0, 2, x)
                    
#                     elif CheckPosCollide([self.x, self.y + 1]) != True:
#                         Hover(0, 1, x)

# # Bishop Hovers
# class Bishop(Button):
#     def __init__(self, x, y, textr):
#         super().__init__(
#             model='plane',
#             parent=scene,
#             texture = textr,
#             rotation_x = -90,
#             position = (x, y, -0.01),
#             color = color.white
#         )
#         if str(self.texture) == "bishopW.png":
#             Positions[0].append([x, y])
#         else:
#             Positions[1].append([x, y])

#     def input(self, keys):
#         if self.hovered:
#             if keys == 'left mouse down':
#                 x = Entity(parent = self, origin = (0, 0, 0))
#                 BishopManager(self, x)

# # Rook hovers
# class Rook(Button):
#     def __init__(self, x, y, textr):
#         super().__init__(
#             model='plane',
#             parent=scene,
#             texture = textr,
#             rotation_x = -90,
#             position = (x, y, -0.01),
#             color = color.white
#         )
#         if str(self.texture) == "rookW.png":
#             Positions[0].append([x, y])
#         else:
#             Positions[1].append([x, y])

#     def input(self, keys):
#         if self.hovered:
#             if keys == 'left mouse down':
#                 x = Entity(parent = self, origin = (0, 0, 0))
#                 RookManager(self, x)

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
                if CheckTurn(self):
                    Log(f"Queen Cliked: Positions - {Positions}")
                    Log(f"Queen Position: {self.position}")
                    x = Entity(parent = self, origin = (0, 0, 0))
                    RookManager(self, x)
                    BishopManager(self, x)

# # Knight hovers
# class Knight(Button):
#     def __init__(self, x, y, textr):
#         super().__init__(
#             model='plane',
#             parent=scene,
#             texture = textr,
#             rotation_x = -90,
#             position = (x, y, -0.01),
#             color = color.white
#         )
#         if str(self.texture) == "knightW.png":
#             Positions[0].append([x, y])
#         else:
#             Positions[1].append([x, y])


#     def input(self, keys):
#         if self.hovered:
#             if keys == 'left mouse down':
#                 x = Entity(parent = self, origin = (0, 0, 0))
#                 KnightManager(self, x)

# # Pawn Hovers
# class Pawn(Button):
#     def __init__(self, x, y, textr):
#         super().__init__(
#             model='plane',
#             parent=scene,
#             texture = textr,
#             rotation_x = -90,
#             position = (x, y, -0.01),
#             color = color.white
#         )
#         if str(self.texture) == "pawnW.png":
#             Positions[0].append([x, y])
#         else:
#             Positions[1].append([x, y])

#     def input(self, keys):
#         if self.hovered:
#             if keys == 'left mouse down':
#                 x = Entity(parent = self, origin = (0, 0, 0))
#                 print(self.texture)
#                 if str(self.texture) == "pawnB.png":
#                     print("check") 
#                     if self.y == 6:
#                         if CheckPosCollide([self.x, self.y - 1]) != True:
#                             Hover(0, -1, x)
#                             if CheckPosCollide([self.x, self.y - 2]) != True:
#                                 Hover(0, -2, x)
                    
#                     elif CheckPosCollide([self.x, self.y - 1]) != True:
#                         Hover(0, -1, x)
#                 elif str(self.texture) == "pawnW.png":
#                     if self.y == 1:
#                         if CheckPosCollide([self.x, self.y + 1]) != True:
#                             Hover(0, 1, x)
#                             if CheckPosCollide([self.x, self.y + 2]) != True:
#                                 Hover(0, 2, x)
                    
#                     elif CheckPosCollide([self.x, self.y + 1]) != True:
#                         Hover(0, 1, x)


board = Board()

for i in range(0, 8):
    Queen(i, 1, 'queenW')
for i in range(0, 8):
    Queen(i, 6, 'queenB')
# k = King(4, 4, 'kingW')
# k = King(4, 3, 'kingW')
# kb = King(4, 5, 'kingB')
# kb = King(4, 7, 'kingB')
# q = Queen(3, 0, 'queenW')
# qb = Queen(3, 7, 'queenB')
# b = Bishop(2, 0, 'bishopW')
# bb = Bishop(2, 7, 'bishopB')
# b2 = Bishop(5, 0, 'bishopW')
# b2b = Bishop(5, 7, 'bishopB')
# Kn = Knight(1, 0, 'knightW')
# Knb = Knight(1, 7, 'knightB')
# Kn2 = Knight(6, 0, 'knightW')
# Kn2b = Knight(6, 7, 'knightB')
# r = Rook(0, 0, 'rookW')
# rb = Rook(0, 7, 'rookB')
# r2 = Rook(7, 0, 'rookW')
# r2b = Rook(7, 7, 'rookB')

# aligning camera with board
cam = EditorCamera()
cam.position = (3.5, 3.5, -1)
app.run()