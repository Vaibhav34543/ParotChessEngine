from ursina import *
import datetime ## DEBUG

turn = 0        # 0 - White, 1 - Black
PossibleCheckers = ["queen", "rook", "bishop", "knight", "pawn"]

def GetCheckerName(pos):
    Log("[GetCheckerName] CALLED: TRUE")
    for i in scene.entities:
        if pos == [int(i.x), int(i.y)]:
            return i.name

def GetKing(classpiece):
    Log("[GetKing] CALLED: TRUE")
    for i in scene.entities:
        if i.name == "king":
            if returnClass(i) == classpiece:
                Log("\tFOUND KING: TRUE")
                return i


def GetKingPos(classPiece):
    for i in scene.entities:
        print(i)
        Log(f"CHECK: {i.x}")
        Log(f"Checking Entity Name: {i.name}")
        if str(i.name) == "king":
            if returnClass(i) == classPiece:
                Log(f"FOUND KING: {i.parent}")
                Pos = [int(i.x), int(i.y)]
                return Pos


# Checks all possible ways and returns True if the king has got check
def CheckForCheck(king, pieceClass):
    Log("[CheckForCheck] CALLED: TRUE")
    kingPos = [int(king.x), int(king.y)]
    Log(f"\tCHECKING FOR CHECK ON KING POS {kingPos}")
    kingClass = returnClass(king)
    Log(f"\tCHECKING FOR CHECK ON KING CLASS {kingClass}")
    right = int(8 - kingPos[0])
    top = int(8 - kingPos[1])
    left = int(kingPos[0] + 1)
    bottom = int(kingPos[1] + 1)
    c = 0
    for i in range(1, top):
        if CheckPosCollide([kingPos[0], kingPos[1] + i], kingClass):
            break
        elif checkOppCollisions([kingPos[0], kingPos[1] + i], kingClass):
            if GetCheckerName([kingPos[0], kingPos[1] + i]) in ["queen", "rook"]:
                Log(f"\tCHECK FOUND: TRUE BY {[kingPos[0], kingPos[1] + i]}")
                king.color = color.red
                c = 1
    for i in range(1, bottom):
        if CheckPosCollide([kingPos[0], kingPos[1] - i], kingClass):
            break
        elif checkOppCollisions([kingPos[0], kingPos[1] - i], kingClass):
            if GetCheckerName([kingPos[0], kingPos[1] - i]) in ["queen", "rook"]:
                Log(f"\tCHECK FOUND: TRUE BY {[kingPos[0], kingPos[1] - i]}")
                king.color = color.red
                c = 1
    for i in range(1, right):
        if CheckPosCollide([kingPos[0] + i, kingPos[1]], kingClass):
            break
        elif checkOppCollisions([kingPos[0] + i, kingPos[1]], kingClass):
            if GetCheckerName([kingPos[0] + i, kingPos[1]]) in ["queen", "rook"]:
                Log(f"CHECK FOUND: TRUE by position {[kingPos[0]+i, kingPos[1]]}")
                king.color = color.red
                c = 1
    for i in range(1, left):
        if CheckPosCollide([kingPos[0] - i, kingPos[1]], kingClass):
            break
        elif checkOppCollisions([kingPos[0] - i, kingPos[1]], kingClass):
            if GetCheckerName([kingPos[0] - i, kingPos[1]]) in ["queen", "rook"]:
                Log(f"CHECK FOUND: TRUE by position {[kingPos[0]-i, kingPos[1]]}")
                king.color = color.red
                c = 1
            
    # Diagnol Checks
    for i in range(1, min(top, right)):
        if CheckPosCollide([kingPos[0] + i, kingPos[1] + i], kingClass):
            break
        if checkOppCollisions([kingPos[0] + i, kingPos[1] + i], kingClass):
            if GetCheckerName([kingPos[0] + i, kingPos[1] + i]) in ["queen", "bishop"]:
                Log(f"CHECK FOUND: TRUE by position {[kingPos[0]+i, kingPos[1]+i]}")
                king.color = color.red
                c = 1
    for i in range(1, min(top, left)):
        if CheckPosCollide([kingPos[0] - i, kingPos[1] + i], kingClass):
            break
        if checkOppCollisions([kingPos[0] - i, kingPos[1] + i], kingClass):
            if GetCheckerName([kingPos[0] - i, kingPos[1] + i]) in ["queen", "bishop"]:
                Log(f"CHECK FOUND: TRUE by position {[kingPos[0]+i, kingPos[1]+i]}")
                king.color = color.red
                c = 1
    for i in range(1, min(bottom, left)):
        if CheckPosCollide([kingPos[0] - i, kingPos[1] - i], kingClass):
            break
        if checkOppCollisions([kingPos[0] - i, kingPos[1] - i], kingClass):
            if GetCheckerName([kingPos[0] - i, kingPos[1] - i]) in ["queen", "bishop"]:
                Log(f"CHECK FOUND: TRUE by position {[kingPos[0]+i, kingPos[1]+i]}")
                king.color = color.red
                c = 1
    for i in range(1, min(bottom, right)):
        if CheckPosCollide([kingPos[0] + i, kingPos[1] - i], kingClass):
            break
        if checkOppCollisions([kingPos[0] + i, kingPos[1] - i], kingClass):
            if GetCheckerName([kingPos[0] + i, kingPos[1] - i]) in ["queen", "bishop"]:
                Log(f"CHECK FOUND: TRUE by position {[kingPos[0]+i, kingPos[1]+i]}")
                king.color = color.red
                c = 1
    
    AllNearMovement = [[-1, 1],[0, 1],[1, 1],[-1, 0],[1, 0],[-1, -1],[0, -1],[1, -1],[-1, 2],[1, 2],[2, 1],[2, -1],[1, -2],[-1, -2],[-2, -1],[-2, 1]]
    for i in AllNearMovement:
        if CheckPosCollide([int(kingPos[0] + i[0]), int(kingPos[1] + i[1])], kingClass):
            continue
        if checkOppCollisions([int(kingPos[0] + i[0]), int(kingPos[1] + i[1])], kingClass):
            if GetCheckerName([int(kingPos[0] + i[0]), int(kingPos[1] + i[1])]) in ["pawn", "knight"]:
                Log(f"CHECK FOUND: TRUE by position {[int(kingPos[0] + i[0]), int(kingPos[1] + i[1])]}")
                king.color = color.red
                c = 1
    


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
        Log("---------------------------TURN-CHANGE----------------------------")
        turn = 1
        CheckForCheck(GetKing("b"), "b")
    else: 
        Log("---------------------------TURN-CHANGE----------------------------")
        turn = 0
        CheckForCheck(GetKing("w"), "w")

# Debug
def Log(data):
    with open('ChessLog.txt', 'a') as file:
        file.write(data+"\n")

Log("==================================================================")
Log("==================================================================")
Log(f"\t\tNEW SESSION: START {datetime.datetime.now()}")
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
        Log("[deleteCollidedOpp] CALLED: TRUE")
        for i in scene.entities:
            if type(i) == "<class '__main__.Board'>":
                continue
            if [int(i.x), int(i.y)] == pos:
                Log("[deleteCollidedOpp] POSITIONS MATCHED: TRUE")
                if returnClass(i) != returnClass(pieceClass):
                    Log(f"\tREMOVING POSITION FROM {Positions[1]}")
                    Log(f'\tDELETING POSITION = [{int(i.x)},{int(i.y)}]')
                    Log(f"\tDESTROYED [{i.name}]")
                    Positions[1].remove([int(i.x), int(i.y)])
                    Log(f"\t\tUPDATED POSITIONS: {Positions}")
                    destroy(i)
                    break
    else:
        Log("[deleteCollidedOpp] CALLED: TRUE")
        for i in scene.entities:
            if type(i) == "<class '__main__.Board'>":
                continue
            if [int(i.x), int(i.y)] == pos:
                Log("[deleteCollidedOpp] POSITIONS MATCHED: TRUE")
                if returnClass(i) != returnClass(pieceClass):
                    Log(f"\tREMOVING POSITION FROM {Positions[1]}")
                    Log(f'\tDELETING POSITION = [{int(i.x)},{int(i.y)}]')
                    Log(f"\tDESTROYED [{i.name}]")
                    Positions[0].remove([int(i.x), int(i.y)])
                    Log(f"\t\tUPDATED POSITIONS: {Positions}")
                    destroy(i)
                    break

# Checks if the opponent positions collide
# Takes in a move and checks if that moves x,y match with both
# the white and black class positions
def checkOppCollisions(move, pieceClass):
    Log(f"[checkOppCollisions] CALLED: TRUE [{pieceClass}]")
    if pieceClass == "w":
        if move in Positions[1]:
            Log(f"\t{move} FOUND IN {Positions[1]}")
            return True
        else: return False
    else:
        if move in Positions[0]:
            Log(f"\t{move} FOUND IN {Positions[0]}")
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
    Log("[CheckPosCollide] CALLED: TRUE")
    pos = [int(pos[0]), int(pos[1])]
    if pieceClass == "w":
        if pos in Positions[0]:
            Log(f"\tCHECKING {pos} IN {Positions[0]}")
            return True
        else: return False
    else:
        if pos in Positions[1]:
            Log(f"\tCHECKING {pos} IN {Positions[1]}")
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
                Log(f"CURRENT POSITIONS: {Positions}")
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
                Log(f"\tCURRENT TURN STATE [{turn}]")


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

# Stops the hovers when an enemy pawn has been targeted and can't go further
def captureBug(pos, pieceClass):
    if pieceClass == "w":
        if [int(pos[0]), int(pos[1])] in Positions[1]:
            return True
    else:
        if [int(pos[0]), int(pos[1])] in Positions[0]:
            return True

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
            if captureBug([bishop.x + i, bishop.y + i], returnClass(h_parent.parent)):
                break
        # if checkOppCollisions([bishop.x + i, bishop.y + i], returnClass(h_parent)):
        #     Hover(i, i, h_parent)
        #     break
        else:
            break
    for i in range(1, min(top, left)):
        if CheckPosCollide([bishop.x - i, bishop.y + i], returnClass(h_parent.parent))!=True:
            Hover(-i, i, h_parent)
            if captureBug([bishop.x - i, bishop.y + i], returnClass(h_parent.parent)):
                break
        else:
            break
    for i in range(1, min(left, bottom)):
        if CheckPosCollide([bishop.x - i, bishop.y - i], returnClass(h_parent.parent))!=True:
            Hover(-i, -i, h_parent)
            if captureBug([bishop.x - i, bishop.y - i], returnClass(h_parent.parent)):
                break
        else:
            break
    for i in range(1, min(bottom, right)):
        if CheckPosCollide([bishop.x + i, bishop.y - i], returnClass(h_parent.parent))!=True:
            Hover(i, -i, h_parent)
            if captureBug([bishop.x + i, bishop.y - i], returnClass(h_parent.parent)):
                break
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
            if captureBug([rook.x + i, rook.y], returnClass(h_parent.parent)):
                break
        else:
            break
    for i in range(1, left):
        if CheckPosCollide([rook.x - i, rook.y], returnClass(h_parent.parent))!=True:
            Hover(-i, 0, h_parent)
            if captureBug([rook.x - i, rook.y], returnClass(h_parent.parent)):
                break
        else:
            break
    for i in range(1, top):
        if CheckPosCollide([rook.x, rook.y + i], returnClass(h_parent.parent))!=True:
            Hover(0, i, h_parent)
            if captureBug([rook.x, rook.y + i], returnClass(h_parent.parent)):
                break
        else:
            break
    for i in range(1, bottom):
        if CheckPosCollide([rook.x, rook.y - i], returnClass(h_parent.parent))!=True:
            Hover(0, -i, h_parent)
            if captureBug([rook.x, rook.y - i], returnClass(h_parent.parent)):
                break
        else:
            break

# Check for knight hovers
def KnightManager(knight, h_parent):
    # Kind of complicated but all it does is 
    # Checks for the L shaped positions if they are in board 
    # and then adds them to hovers
    if int(knight.y + 2) <= 7 and int(knight.x + 1) <= 7:
        if CheckPosCollide([knight.x+1, knight.y+2], returnClass(h_parent.parent)) != True:
            Hover(1, 2, h_parent) 
    if int(knight.y + 2) <= 7 and int(knight.x - 1) >= 0:
        if CheckPosCollide([knight.x -1, knight.y +2], returnClass(h_parent.parent)) != True:
            Hover(-1, 2, h_parent) 
    if int(knight.y + 1) <= 7 and int(knight.x + 2) <= 7:
        if CheckPosCollide([knight.x +2, knight.y+1], returnClass(h_parent.parent)) != True:
            Hover(2, 1, h_parent) 
    if int(knight.y - 1) >= 0 and int(knight.x + 2) <= 7:
        if CheckPosCollide([knight.x+2, knight.y-1], returnClass(h_parent.parent)) != True:
            Hover(2, -1, h_parent) 
    if int(knight.y + 1) <= 7 and int(knight.x - 2) >= 0:
        if CheckPosCollide([knight.x-2, knight.y+1], returnClass(h_parent.parent)) != True:
            Hover(-2, 1, h_parent) 
    if int(knight.y - 1) >= 0 and int(knight.x - 2) >= 0:
        if CheckPosCollide([knight.x-2, knight.y-1], returnClass(h_parent.parent)) != True:
            Hover(-2, -1, h_parent) 
    if int(knight.y - 2) >= 0 and int(knight.x + 1) <= 7:
        if CheckPosCollide([knight.x+1, knight.y-2], returnClass(h_parent.parent)) != True:
            Hover(1, -2, h_parent) 
    if int(knight.y - 2) >= 0 and int(knight.x - 1) >= 0:
        if CheckPosCollide([knight.x-1, knight.y-2], returnClass(h_parent.parent)) != True:
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
        if CheckTurn(self):
            if self.hovered:
                if keys == "left mouse down":
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
        if CheckTurn(self):
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
        if CheckTurn(self):
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
                if CheckTurn(self):
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
                if CheckTurn(self):
                    x = Entity(parent = self, origin = (0, 0, 0))
                    KnightManager(self, x)

# Checks for diagnol collisions 
def PawnCollisions(current_pos, pieceClass, h_parent):
    Log("[PawnCollisions] CALLED: TRUE")
    p = current_pos
    if pieceClass == "w":
        Log(f"\t CHECKING DIAGNOL COLLISIONS FOR {p} IN {Positions[1]}")
        if [p[0] + 1, p[1] + 1] in Positions[1]:
            Log("\t\tFOUND DIAGNOL COLLISION: TRUE")
            Hover(1, 1, h_parent)
        if [p[0] - 1, p[1] + 1] in Positions[1]:
            Log("\t\tFOUND DIAGNOL COLLISION: TRUE")
            Hover(-1, 1, h_parent)
    else:
        Log(f"\t CHECKING DIAGNOL COLLISIONS FOR {p} IN {Positions[0]}")
        if [p[0] + 1, p[1] - 1] in Positions[0]:
            Log("\t\tFOUND DIAGNOL COLLISION: TRUE")
            Hover(1, -1, h_parent)
        if [p[0] - 1, p[1] - 1] in Positions[0]:
            Log("\t\tFOUND DIAGNOL COLLISION: TRUE")
            Hover(-1, -1, h_parent)

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
                if CheckTurn(self):
                    x = Entity(parent = self, origin = (0, 0, 0))
                    if str(self.texture) == "pawnB.png":
                        if self.y == 6:
                            if CheckPosCollide([self.x, self.y - 1], returnClass(self)) != True:
                                if captureBug([self.x, self.y - 1], returnClass(self)) != True:
                                    Hover(0, -1, x)
                                if CheckPosCollide([self.x, self.y - 2], returnClass(self)) != True:
                                    if captureBug([self.x, self.y - 2], returnClass(self)) != True:
                                        Hover(0, -2, x)
                        
                        else:
                            if CheckPosCollide([self.x, self.y - 1], returnClass(self)) != True:
                                if captureBug([self.x, self.y - 1], returnClass(self)) != True:
                                    Hover(0, -1, x)
                    elif str(self.texture) == "pawnW.png":
                        if self.y == 1:
                            if CheckPosCollide([self.x, self.y + 1], returnClass(self)) != True:
                                if captureBug([self.x, self.y + 1], returnClass(self)) != True:
                                    Hover(0, 1, x)
                                if CheckPosCollide([self.x, self.y + 2], returnClass(self)) != True:
                                    if captureBug([self.x, self.y + 2], returnClass(self)) != True:
                                        Hover(0, 2, x)
                        
                        elif CheckPosCollide([self.x, self.y + 1], returnClass(self)) != True:
                            if captureBug([self.x, self.y + 1], returnClass(self)) != True:
                                Hover(0, 1, x)
                    PawnCollisions([int(self.x), int(self.y)], returnClass(self), x)


board = Board()

for i in range(0, 8):
    Pawn(i, 1, 'pawnW')
for i in range(0, 8):
    Pawn(i, 6, 'pawnB')
Pawn(3, 6, 'pawnB')
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

# aligning camera with board
cam = EditorCamera()
cam.position = (3.5, 3.5, -1)
app.run()