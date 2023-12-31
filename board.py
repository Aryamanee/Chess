from piece import Piece
import copy

#Squares
A1 = (7, 0)
A2 = (6, 0)
A3 = (5, 0)
A4 = (4, 0)
A5 = (3, 0)
A6 = (2, 0)
A7 = (1, 0)
A8 = (0, 0)
B1 = (7, 1)
B2 = (6, 1)
B3 = (5, 1)
B4 = (4, 1)
B5 = (3, 1)
B6 = (2, 1)
B7 = (1, 1)
B8 = (0, 1)
C1 = (7, 2)
C2 = (6, 2)
C3 = (5, 2)
C4 = (4, 2)
C5 = (3, 2)
C6 = (2, 2)
C7 = (1, 2)
C8 = (0, 2)
D1 = (7, 3)
D2 = (6, 3)
D3 = (5, 3)
D4 = (4, 3)
D5 = (3, 3)
D6 = (2, 3)
D7 = (1, 3)
D8 = (0, 3)
E1 = (7, 4)
E2 = (6, 4)
E3 = (5, 4)
E4 = (4, 4)
E5 = (3, 4)
E6 = (2, 4)
E7 = (1, 4)
E8 = (0, 4)
F1 = (7, 5)
F2 = (6, 5)
F3 = (5, 5)
F4 = (4, 5)
F5 = (3, 5)
F6 = (2, 5)
F7 = (1, 5)
F8 = (0, 5)
G1 = (7, 6)
G2 = (6, 6)
G3 = (5, 6)
G4 = (4, 6)
G5 = (3, 6)
G6 = (2, 6)
G7 = (1, 6)
G8 = (0, 6)
H1 = (7, 7)
H2 = (6, 7)
H3 = (5, 7)
H4 = (4, 7)
H5 = (3, 7)
H6 = (2, 7)
H7 = (1, 7)
H8 = (0, 7)

#BOARD CLASS
class Board:
  #INITIALIZE BOARD, args of time control and position
  def __init__(self, position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", time_control = (-1, -1)):
    #set time control
    self.time_control = time_control
    #set board
    self.board = []
    lines = position.split("/")
    line_n = 0
    for line in lines:
      self.board.append([])
      col = 0
      while col <= len(line)-1:
        if line[col].isalpha():
          self.board[line_n].append(Piece(line[col].upper(), line[col].islower()))
          col+=1
        else:
          for i in range(int(line[col])):
            self.board[line_n].append(None)
          col+=1
          if col > len(line)-1:
            break
      line_n+=1

    #moves list
    self.history = []

  #king_safe(sqare) function
  def king_safe(self, square, color, board = []):
    if board == []:
      board  = self.board
    safe = True
  #takes square of king and checks if the king would be in check on that square
    #check for knights of opposite color
    knight_offsets = [(1,2),(2,1),(1,-2),(2,-1),(-1,2),(-2,1),(-1,-2),(-2,-1)]
    for offset in knight_offsets:
      if square[0] + offset[0] <=7 and square[0] + offset[0] >=0 and square[1] + offset[1] <=7 and square[1] + offset[1] >=0:
        if board[square[0] + offset[0]][square[1] + offset[1]] != None:
          if board[square[0] + offset[0]][square[1] + offset[1]].color != color and board[square[0] + offset[0]][square[1] + offset[1]].type == "N":
            return False

    #check horizontal and vertical lines for opposite color rooks or queens
    for rank in range(0,8):
      if board[rank][square[1]] != None:
        if board[rank][square[1]].color != color and (board[rank][square[1]].type == "R" or board[rank][square[1]].type == "Q"):
          none, ran = True, False
          for rankgap in range(min(square[0],rank)+1,max(square[0],rank)):
            ran = True
            if board[rankgap][square[1]] != None:
             none = False
          if none and ran:
            return False
          elif abs(square[0] - rank) == 1:
            return False

    for file in range(0,8):
      if board[square[0]][file] != None:
        if board[square[0]][file].color != color and (board[square[0]][file].type == "R" or board[square[0]][file].type == "Q"):
          none, ran = True, False
          for filegap in range(min(square[1],file)+1,max(square[1],file)):
            ran = True
            if board[square[0]][filegap] != None:
             none = False
          if none and ran:
            return False
          elif abs(square[1] - file) == 1:
            return False

    #check diagonal lines for opposite color bishops or queens
    diagonal1offsets = [(7, -7), (6, -6), (5, -5), (4, -4), (3, -3), (2, -2), (1, -1), (0, 0), (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)]
    diagonal1 = []
    diagonal2offsets = [(7, 7), (6, 6), (5, 5), (4, 4), (3, 3), (2, 2), (1, 1), (0, 0), (-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)]
    diagonal2 = []

    for offset in diagonal1offsets:
      if square[0] + offset[0] <=7 and square[0] + offset[0] >=0 and square[1] + offset[1] <=7 and square[1] + offset[1] >=0:
        diagonal1.append(board[square[0] + offset[0]][square[1] + offset[1]])
        if offset == (0,0):
          kingpos1 = len(diagonal1)-1
    for piece in range(len(diagonal1)):
      if diagonal1[piece] != None:
        if diagonal1[piece].color != color and (diagonal1[piece].type == "B" or diagonal1[piece].type == "Q"):
          none, ran = True, False
          for piecegap in range(min(kingpos1,piece)+1,max(kingpos1,piece)):
            ran = True
            if diagonal1[piecegap] != None:
             none = False
          if none and ran:
            return False
          elif abs(kingpos1 - piece) == 1:
            return False

    for offset in diagonal2offsets:
      if square[0] + offset[0] <=7 and square[0] + offset[0] >=0 and square[1] + offset[1] <=7 and square[1] + offset[1] >=0:
        diagonal2.append(board[square[0] + offset[0]][square[1] + offset[1]])
        if offset == (0,0):
          kingpos2 = len(diagonal2)-1
    for piece in range(len(diagonal2)):
      if diagonal2[piece] != None:
        if diagonal2[piece].color != color and (diagonal2[piece].type == "B" or diagonal2[piece].type == "Q"):
          none, ran = True, False
          for piecegap in range(min(kingpos2,piece)+1,max(kingpos2,piece)):
            ran = True
            if diagonal2[piecegap] != None:
             none = False
          if none and ran:
            return False
          elif abs(kingpos2 - piece) == 1:
            return False

    #check around the king for other kings
    kingoffsets = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]

    for offset in kingoffsets:
      if square[0] + offset[0] <=7 and square[0] + offset[0] >=0 and square[1] + offset[1] <=7 and square[1] + offset[1] >= 0:
        if board[square[0] + offset[0]][square[1] + offset[1]] != None:
          if board[square[0] + offset[0]][square[1] + offset[1]].color != color and board[square[0] + offset[0]][square[1] + offset[1]].type == "K":
            return False

    #check for pawns 
    if color:
      pawnoffsets = [(1, 1), (1, -1)]
    else:
      pawnoffsets = [(-1, -1), (-1, 1)]

    for offset in pawnoffsets:
      if square[0] + offset[0] <=7 and square[0] + offset[0] >=0 and square[1] + offset[1] <=7:
        if board[square[0] + offset[0]][square[1] + offset[1]] != None:
          if board[square[0] + offset[0]][square[1] + offset[1]].color != color and board[square[0] + offset[0]][square[1] + offset[1]].type == "P":
            return False

    return safe

  #is_valid_move function
  def is_valid_move(self, currsquare, endsquare):
    #is endsquare same as current square? or is currentsquare empty or is endsquare same color as current square? and is the currsquare and endsquare on board
    if currsquare == endsquare:
      return False
    elif self.board[currsquare[0]][currsquare[1]] == None:
      return False
    elif (currsquare[0]<0 or currsquare[0]>7 or currsquare[1]<0 or currsquare[1]>7) or (endsquare[0]<0 or endsquare[0]>7 or endsquare[1]<0 or endsquare[1]>7):
      return False
    color = self.board[currsquare[0]][currsquare[1]].color
    if self.board[endsquare[0]][endsquare[1]] != None:
      if self.board[endsquare[0]][endsquare[1]].color == color:
        return False
    #runs for different types of pieces
    #this one for rooks
    if self.board[currsquare[0]][currsquare[1]].type == "R":
      rook_offsets = [(1,0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (-1,0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)]
      # runs if the end square for the rook is somewhere a rook would go, doesn't matter if it's off the board as that has been dealt with above
      if rook_offsets.count((endsquare[0] - currsquare[0], endsquare[1] - currsquare[1])) == 1:
        line = []
        if endsquare[0] - currsquare[0] == 0:
          if currsquare[1] < endsquare[1]:
            for i in range(currsquare[1]+1, endsquare[1]):
              line.append(self.board[currsquare[0]][i])
          else:
            for i in range(currsquare[1]-1, endsquare[1], -1):
              line.append(self.board[currsquare[0]][i])
        elif currsquare[1] - currsquare[1] == 0:
          if currsquare[0] < endsquare[0]:
            for i in range(currsquare[0]+1, endsquare[0]):
              line.append(self.board[i][currsquare[1]])
          else:
            for i in range(currsquare[0]-1, endsquare[0], -1):
              line.append(self.board[i][currsquare[1]])
        if line.count(None)<len(line):
          return False
        # creates a copy of the board and plays the move to check if the the king of the player would be safe after the move
        board_copy = copy.deepcopy(self.board)
        self.move(currsquare, endsquare, board_copy)
        return self.king_safe(self.find_king(color, board_copy), color, board_copy)
      else:
        return False
    #runs for Knights
    elif self.board[currsquare[0]][currsquare[1]].type == "N":
      knight_offsets = [(1,2),(2,1),(1,-2),(2,-1),(-1,2),(-2,1),(-1,-2),(-2,-1)]
      #runs if the end square for the knight is somewhere a knight would go
      if knight_offsets.count((endsquare[0]-currsquare[0],endsquare[1]-currsquare[1])) == 1:
        #creates a copy of the board and plays the move to check if the the king of the player would be safe after the move
        board_copy = copy.deepcopy(self.board)
        self.move(currsquare, endsquare, board_copy)
        return self.king_safe(self.find_king(color, board_copy) ,color, board_copy)
      else:
        return False
    #runs for bishops
    elif self.board[currsquare[0]][currsquare[1]].type == "B":
      bishop_offsets = [(7, -7), (6, -6), (5, -5), (4, -4), (3, -3), (2, -2), (1, -1), (0, 0), (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7), (7, 7), (6, 6), (5, 5), (4, 4), (3, 3), (2, 2), (1, 1), (0, 0), (-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)]
      # runs if the end square for the bishop is somewhere a bishop would go, doesn't matter if it's off the board as that has been dealt with above
      if bishop_offsets.count((endsquare[0] - currsquare[0], endsquare[1] - currsquare[1])) == 1:
        line = []
        if endsquare[0] - currsquare[0] > 0 and endsquare[1] - currsquare[1] > 0:
          for i in range(1, abs(endsquare[0] - currsquare[0])):
            line.append(self.board[currsquare[0] + i][currsquare[1] + i])
        elif endsquare[0] - currsquare[0] < 0 and endsquare[1] - currsquare[1] < 0:
          for i in range(1, abs(endsquare[0] - currsquare[0])):
            line.append(self.board[currsquare[0] - i][currsquare[1] - i])
        elif endsquare[0] - currsquare[0] < 0 and endsquare[1] - currsquare[1] > 0:
          for i in range(1, abs(endsquare[0] - currsquare[0])):
            line.append(self.board[currsquare[0] - i][currsquare[1] + i])
        elif endsquare[0] - currsquare[0] > 0 and endsquare[1] - currsquare[1] < 0:
          for i in range(1, abs(endsquare[0] - currsquare[0])):
            line.append(self.board[currsquare[0] + i][currsquare[1] - i])
        if line.count(None) < len(line):
          return False

        # creates a copy of the board and plays the move to check if the the king of the player would be safe after the move
        board_copy = copy.deepcopy(self.board)
        self.move(currsquare, endsquare, board_copy)
        return self.king_safe(self.find_king(color, board_copy), color, board_copy)
      else:
        return False
    elif self.board[currsquare[0]][currsquare[1]].type == "Q":
      queen_offsets = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7), (7, -7), (6, -6), (5, -5), (4, -4), (3, -3), (2, -2), (1, -1), (0, 0), (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7), (7, 7), (6, 6), (5, 5), (4, 4), (3, 3), (2, 2), (1, 1), (0, 0), (-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)]
      line = []
      # runs if the end square for the queen is somewhere a queen would go, doesn't matter if it's off the board as that has been dealt with above
      if queen_offsets.count((endsquare[0] - currsquare[0], endsquare[1] - currsquare[1])) == 1:
        line = []
        if endsquare[0] - currsquare[0] == 0:
          if currsquare[1] < endsquare[1]:
            for i in range(currsquare[1] + 1, endsquare[1]):
              line.append(self.board[currsquare[0]][i])
          else:
            for i in range(currsquare[1] - 1, endsquare[1], -1):
              line.append(self.board[currsquare[0]][i])
        elif endsquare[1] - currsquare[1] == 0:
          if currsquare[0] < endsquare[0]:
            for i in range(currsquare[0] + 1, endsquare[0]):
              line.append(self.board[i][currsquare[1]])
          else:
            for i in range(currsquare[0] - 1, endsquare[0], -1):
              line.append(self.board[i][currsquare[1]])
        elif endsquare[0] - currsquare[0] > 0 and endsquare[1] - currsquare[1] > 0:
          for i in range(1, abs(endsquare[0] - currsquare[0])):
            line.append(self.board[currsquare[0] + i][currsquare[1] + i])
        elif endsquare[0] - currsquare[0] < 0 and endsquare[1] - currsquare[1] < 0:
          for i in range(1, abs(endsquare[0] - currsquare[0])):
            line.append(self.board[currsquare[0] - i][currsquare[1] - i])
        elif endsquare[0] - currsquare[0] < 0 and endsquare[1] - currsquare[1] > 0:
          for i in range(1, abs(endsquare[0] - currsquare[0])):
            line.append(self.board[currsquare[0] - i][currsquare[1] + i])
        elif endsquare[0] - currsquare[0] > 0 and endsquare[1] - currsquare[1] < 0:
          for i in range(1, abs(endsquare[0] - currsquare[0])):
            line.append(self.board[currsquare[0] + i][currsquare[1] - i])
        if line.count(None) < len(line):
          return False

        # creates a copy of the board and plays the move to check if the the king of the player would be safe after the move
        board_copy = copy.deepcopy(self.board)
        self.move(currsquare, endsquare, board_copy)
        return self.king_safe(self.find_king(color, board_copy), color, board_copy)
      else:
        return False
    elif self.board[currsquare[0]][currsquare[1]].type == "K":
      king_offsets = [(0,1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
      #runs for a black king
      if color:
        # runs if the end square for the king is somewhere a king would go, doesn't matter if it's off the board as that has been dealt with above
        if king_offsets.count((endsquare[0] - currsquare[0], endsquare[1] - currsquare[1])) == 1:
          # creates a copy of the board and plays the move to check if the the king of the player would be safe after the move
          board_copy = copy.deepcopy(self.board)
          self.move(currsquare, endsquare, board_copy)
          return self.king_safe(self.find_king(color, board_copy), color, board_copy)
        elif endsquare == G8 and currsquare == E8 and self.board[0][6] == None and self.board[0][5] == None:
          return self.king_safe(E8, color) and self.king_safe(F8, color) and self.king_safe(G8, color) and (not self.king_moved(color)) and (not self.rook_moved(color, H8))
        elif endsquare == C8 and currsquare == E8 and self.board[0][3] == None and self.board[0][2] == None and self.board[0][1] == None:
          return self.king_safe(E8, color) and self.king_safe(D8, color) and self.king_safe(C8, color) and (not self.king_moved(color)) and (not self.rook_moved(color, A8))
        else:
          return False
      #white king
      else:

        # runs if the end square for the king is somewhere a king would go, doesn't matter if it's off the board as that has been dealt with above
        if king_offsets.count((endsquare[0] - currsquare[0], endsquare[1] - currsquare[1])) == 1:
          # creates a copy of the board and plays the move to check if the the king of the player would be safe after the move
          board_copy = copy.deepcopy(self.board)
          self.move(currsquare, endsquare, board_copy)
          return self.king_safe(self.find_king(color, board_copy), color, board_copy)
        elif endsquare == G1 and currsquare == E1 and self.board[7][6] == None and self.board[7][5] == None:
          return self.king_safe(E1, color) and self.king_safe(F1, color) and self.king_safe(G1, color) and (
            not self.king_moved(color)) and (not self.rook_moved(color, H1))
        elif endsquare == C1 and currsquare == E1 and self.board[7][3] == None and self.board[7][2] == None and self.board[7][1] == None:
          return self.king_safe(E1, color) and self.king_safe(D1, color) and self.king_safe(C1, color) and (
            not self.king_moved(color)) and (not self.rook_moved(color, A1))
        else:
          return False
    elif self.board[currsquare[0]][currsquare[1]].type == "P":
      if self.board[endsquare[0]][endsquare[1]] != None:
        if self.board[endsquare[0]][endsquare[1]].color == color:
          return False
      if color:
        if endsquare[0] == currsquare[0]+1 and endsquare[1] == currsquare[1] and self.board[endsquare[0]][endsquare[1]] == None:
          board_copy = copy.deepcopy(self.board)
          self.move(currsquare, endsquare, board_copy)
          return self.king_safe(self.find_king(color, board_copy), color, board_copy)
        elif endsquare[0] == currsquare[0]+2 and endsquare[1] == currsquare[1] and currsquare[0] == 1 and self.board[currsquare[0]+1][currsquare[1]] == None and self.board[endsquare[0]][endsquare[1]] == None:
          board_copy = copy.deepcopy(self.board)
          self.move(currsquare, endsquare, board_copy)
          return self.king_safe(self.find_king(color, board_copy), color, board_copy)
        elif endsquare[0] == currsquare[0]+1 and (endsquare[1] == currsquare[1]+1 or endsquare[1] == currsquare[1]-1):
          if self.board[endsquare[0]][endsquare[1]] != None:
            if self.board[endsquare[0]][endsquare[1]].color != color:
              board_copy = copy.deepcopy(self.board)
              self.move(currsquare, endsquare, board_copy)
              return self.king_safe(self.find_king(color, board_copy), color, board_copy)
          elif len(self.history) > 0:
            if self.history[len(self.history)-1][2].type == "P" and self.history[len(self.history)-1][0][0] == 6 and self.history[len(self.history)-1][1][0] == 4 and self.history[len(self.history)-1][2].color != color and currsquare[0] == 4 and self.history[len(self.history)-1][0][1] == endsquare[1]:
              board_copy = copy.deepcopy(self.board)
              self.move(currsquare, endsquare, board_copy)
              return self.king_safe(self.find_king(color, board_copy), color, board_copy)
            else:
              return False
          else:
            return False
        else:
          return False
      else:
        if endsquare[0] == currsquare[0]-1 and endsquare[1] == currsquare[1] and self.board[endsquare[0]][endsquare[1]] == None:
          board_copy = copy.deepcopy(self.board)
          self.move(currsquare, endsquare, board_copy)
          return self.king_safe(self.find_king(color, board_copy), color, board_copy)
        elif endsquare[0] == currsquare[0]-2 and endsquare[1] == currsquare[1] and currsquare[0] == 6 and self.board[currsquare[0]-1][currsquare[1]] == None and self.board[endsquare[0]][endsquare[1]] == None:
          board_copy = copy.deepcopy(self.board)
          self.move(currsquare, endsquare, board_copy)
          return self.king_safe(self.find_king(color, board_copy), color, board_copy)
        elif endsquare[0] == currsquare[0]-1 and (endsquare[1] == currsquare[1]+1 or endsquare[1] == currsquare[1]-1):
          if self.board[endsquare[0]][endsquare[1]] != None:
            if self.board[endsquare[0]][endsquare[1]].color != color:
              board_copy = copy.deepcopy(self.board)
              self.move(currsquare, endsquare, board_copy)
              return self.king_safe(self.find_king(color, board_copy), color, board_copy)
          elif len(self.history) > 0:
            if self.history[len(self.history)-1][2].type == "P" and self.history[len(self.history)-1][0][0] == 1 and self.history[len(self.history)-1][1][0] == 3 and self.history[len(self.history)-1][2].color != color and currsquare[0] == 3 and self.history[len(self.history)-1][0][1] == endsquare[1]:
              board_copy = copy.deepcopy(self.board)
              self.move(currsquare, endsquare, board_copy)
              return self.king_safe(self.find_king(color, board_copy), color, board_copy)
            else:
              return False
          else:
            return False
        else:
          return False
    
    #else is king in check after move(king_safe(square) function)
    #is a same color col in the way?
    #for castles - has the king or the rook in question moved and is there anything blocking the path(king_safe(square) function)
  #move function
  def move(self, currsquare, endsquare, board = [], promo = "P"):
    log_move = board == []
    if board == []:
      board = self.board
    color = board[currsquare[0]][currsquare[1]].color
    piece  = self.board[currsquare[0]][currsquare[1]]
    if piece.type == "K":
      if abs(currsquare[1] - endsquare[1]) == 2:
        if color:
          if endsquare == G8:
            self.move(H8, F8)
          elif endsquare == C8:
            self.move(A8, D8)
        else:
          if endsquare == G1:
            self.move(H1, F1)
          elif endsquare == C1:
            self.move(A1, D1)

    board[endsquare[0]][endsquare[1]] = board[currsquare[0]][currsquare[1]]
    board[currsquare[0]][currsquare[1]] = None
    if piece.type == "P":
      if color:
        if endsquare[0] == 7:
          board[endsquare[0]][endsquare[1]].type = promo
      else:
        if endsquare[0] == 0:
          board[endsquare[0]][endsquare[1]].type = promo
    if log_move:
      if self.king_safe(self.find_king(not color), not color):
        self.history.append([currsquare, endsquare, piece, 0])
      else:
        self.history.append([currsquare, endsquare, piece, 1])

  #find_king function
  def find_king(self, color, board = []):
    if board == []:
      board = self.board
    for rank in range(len(board)):
      for square in range(len(board[rank])):
        if board[rank][square]!=None:
          if board[rank][square].color == color and board[rank][square].type == "K":
            return (rank, square)
            
  def king_moved(self, color):
    for move in self.history:
      if move[2].type == "K" and move[2].color == color:
        return True
    return False

  def rook_moved(self, color, square):
    for move in self.history:
      if move[2].type == "R" and move[2].color == color and move[0] == square:
        return True
    return False
  #valid_moves(square)
  #returns all valid moves for piece on that square
  def valid_moves(self, square):
    moves = []
    if self.board[square[0]][square[1]] != None:
      if self.board[square[0]][square[1]].type == "K":
        king_offsets = [(0,1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1), (0, 2), (0, -2)]
        for offset in king_offsets:
          newsquare = (square[0] + offset[0], square[1] + offset[1])
          if self.is_valid_move(square, newsquare):
            moves.append(newsquare)
      elif self.board[square[0]][square[1]].type == "Q":
        queen_offsets = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7), (7, -7), (6, -6), (5, -5), (4, -4), (3, -3), (2, -2), (1, -1), (0, 0), (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7), (7, 7), (6, 6), (5, 5), (4, 4), (3, 3), (2, 2), (1, 1), (0, 0), (-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)]
        for offset in queen_offsets:
          newsquare = (square[0] + offset[0], square[1] + offset[1])
          if self.is_valid_move(square, newsquare):
            moves.append(newsquare)
      elif self.board[square[0]][square[1]].type == "R":
        rook_offsets = [(1,0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (-1,0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)]
        for offset in rook_offsets:
          newsquare = (square[0] + offset[0], square[1] + offset[1])
          if self.is_valid_move(square, newsquare):
            moves.append(newsquare)
      elif self.board[square[0]][square[1]].type == "B":
        bishop_offsets = [(7, -7), (6, -6), (5, -5), (4, -4), (3, -3), (2, -2), (1, -1), (0, 0), (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7), (7, 7), (6, 6), (5, 5), (4, 4), (3, 3), (2, 2), (1, 1), (0, 0), (-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)]
        for offset in bishop_offsets:
          newsquare = (square[0] + offset[0], square[1] + offset[1])
          if self.is_valid_move(square, newsquare):
            moves.append(newsquare)
      elif self.board[square[0]][square[1]].type == "N":
        knight_offsets = [(1,2),(2,1),(1,-2),(2,-1),(-1,2),(-2,1),(-1,-2),(-2,-1)]
        for offset in knight_offsets:
          newsquare = (square[0] + offset[0], square[1] + offset[1])
          if self.is_valid_move(square, newsquare):
            moves.append(newsquare)
      elif self.board[square[0]][square[1]].type == "P":
        if self.board[square[0]][square[1]].color:
          pawn_offsets = [(1, 0), (2, 0), (1, 1), (1, -1)]
        else:
          pawn_offsets = [(-1, 0), [-2, 0], (-1, 1), (-1, -1)]
        for offset in pawn_offsets:
          newsquare = (square[0] + offset[0], square[1] + offset[1])
          if self.is_valid_move(square, newsquare):
            moves.append(newsquare)
      return moves
#all_valid_moves(side)
  #returns all valid moves for all pieces for the side provided