from piece import Piece
from copy import deepcopy

# Set Square Tuples
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


# BOARD CLASS
class Board:
    # INITIALIZE BOARD, args of time control and position
    def __init__(
        self, position="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", turn=False
    ):
        # set board
        self.board = []
        # set if the board should be rendered
        self.render = True
        # find square function
        self.find_square = lambda pos: self.board[pos[0]][pos[1]]
        # set the turn
        self.turn = turn
        # set the lines of fen string
        lines = position.split("/")
        # parse fen string and put it into board form
        line_n = 0
        for line in lines:
            self.board.append([])
            col = 0
            while col <= len(line) - 1:
                if line[col].isalpha():
                    self.board[line_n].append(
                        Piece(line[col].upper(), line[col].islower())
                    )
                    col += 1
                else:
                    for i in range(int(line[col])):
                        self.board[line_n].append(None)
                    col += 1
                    if col > len(line) - 1:
                        break
            line_n += 1
        # moves list
        self.history = []
        # set the board history for threefold repetiton
        self.board_history = [deepcopy(self.board)]

    # king_safe(sqare) function
    def king_safe(self, square, color):
        safe = True
        # takes square of king and checks if the king would be in check on that square
        # check for knights of opposite color
        knight_offsets = [
            (1, 2),
            (2, 1),
            (1, -2),
            (2, -1),
            (-1, 2),
            (-2, 1),
            (-1, -2),
            (-2, -1),
        ]
        for offset in knight_offsets:
            if (
                square[0] + offset[0] <= 7
                and square[0] + offset[0] >= 0
                and square[1] + offset[1] <= 7
                and square[1] + offset[1] >= 0
            ):
                if self.board[square[0] + offset[0]][square[1] + offset[1]] != None:
                    if (
                        self.board[square[0] + offset[0]][square[1] + offset[1]].color
                        != color
                        and self.board[square[0] + offset[0]][
                            square[1] + offset[1]
                        ].type
                        == "N"
                    ):
                        return False

        # check horizontal and vertical lines for opposite color rooks or queens
        for rank in range(0, 8):
            if self.board[rank][square[1]] != None:
                if self.board[rank][square[1]].color != color and (
                    self.board[rank][square[1]].type == "R"
                    or self.board[rank][square[1]].type == "Q"
                ):
                    none, ran = True, False
                    for rankgap in range(
                        min(square[0], rank) + 1, max(square[0], rank)
                    ):
                        ran = True
                        if self.board[rankgap][square[1]] != None:
                            none = False
                    if none and ran:
                        return False
                    elif abs(square[0] - rank) == 1:
                        return False

        for file in range(0, 8):
            if self.board[square[0]][file] != None:
                if self.board[square[0]][file].color != color and (
                    self.board[square[0]][file].type == "R"
                    or self.board[square[0]][file].type == "Q"
                ):
                    none, ran = True, False
                    for filegap in range(
                        min(square[1], file) + 1, max(square[1], file)
                    ):
                        ran = True
                        if self.board[square[0]][filegap] != None:
                            none = False
                    if none and ran:
                        return False
                    elif abs(square[1] - file) == 1:
                        return False

        # check diagonal lines for opposite color bishops or queens
        diagonal1offsets = [
            (7, -7),
            (6, -6),
            (5, -5),
            (4, -4),
            (3, -3),
            (2, -2),
            (1, -1),
            (0, 0),
            (-1, 1),
            (-2, 2),
            (-3, 3),
            (-4, 4),
            (-5, 5),
            (-6, 6),
            (-7, 7),
        ]
        diagonal1 = []
        diagonal2offsets = [
            (7, 7),
            (6, 6),
            (5, 5),
            (4, 4),
            (3, 3),
            (2, 2),
            (1, 1),
            (0, 0),
            (-1, -1),
            (-2, -2),
            (-3, -3),
            (-4, -4),
            (-5, -5),
            (-6, -6),
            (-7, -7),
        ]
        diagonal2 = []

        for offset in diagonal1offsets:
            if (
                square[0] + offset[0] <= 7
                and square[0] + offset[0] >= 0
                and square[1] + offset[1] <= 7
                and square[1] + offset[1] >= 0
            ):
                diagonal1.append(
                    self.board[square[0] + offset[0]][square[1] + offset[1]]
                )
                if offset == (0, 0):
                    kingpos1 = len(diagonal1) - 1
        for piece in range(len(diagonal1)):
            if diagonal1[piece] != None:
                if diagonal1[piece].color != color and (
                    diagonal1[piece].type == "B" or diagonal1[piece].type == "Q"
                ):
                    none, ran = True, False
                    for piecegap in range(
                        min(kingpos1, piece) + 1, max(kingpos1, piece)
                    ):
                        ran = True
                        if diagonal1[piecegap] != None:
                            none = False
                    if none and ran:
                        return False
                    elif abs(kingpos1 - piece) == 1:
                        return False

        for offset in diagonal2offsets:
            if (
                square[0] + offset[0] <= 7
                and square[0] + offset[0] >= 0
                and square[1] + offset[1] <= 7
                and square[1] + offset[1] >= 0
            ):
                diagonal2.append(
                    self.board[square[0] + offset[0]][square[1] + offset[1]]
                )
                if offset == (0, 0):
                    kingpos2 = len(diagonal2) - 1
        for piece in range(len(diagonal2)):
            if diagonal2[piece] != None:
                if diagonal2[piece].color != color and (
                    diagonal2[piece].type == "B" or diagonal2[piece].type == "Q"
                ):
                    none, ran = True, False
                    for piecegap in range(
                        min(kingpos2, piece) + 1, max(kingpos2, piece)
                    ):
                        ran = True
                        if diagonal2[piecegap] != None:
                            none = False
                    if none and ran:
                        return False
                    elif abs(kingpos2 - piece) == 1:
                        return False

        # check around the king for other kings
        kingoffsets = [
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1),
            (1, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
        ]

        for offset in kingoffsets:
            if (
                square[0] + offset[0] <= 7
                and square[0] + offset[0] >= 0
                and square[1] + offset[1] <= 7
                and square[1] + offset[1] >= 0
            ):
                if self.board[square[0] + offset[0]][square[1] + offset[1]] != None:
                    if (
                        self.board[square[0] + offset[0]][square[1] + offset[1]].color
                        != color
                        and self.board[square[0] + offset[0]][
                            square[1] + offset[1]
                        ].type
                        == "K"
                    ):
                        return False

        # check for pawns
        if color:
            pawnoffsets = [(1, 1), (1, -1)]
        else:
            pawnoffsets = [(-1, -1), (-1, 1)]

        for offset in pawnoffsets:
            if (
                square[0] + offset[0] <= 7
                and square[0] + offset[0] >= 0
                and square[1] + offset[1] <= 7
                and square[1] + offset[1] >= 0
            ):
                if self.board[square[0] + offset[0]][square[1] + offset[1]] != None:
                    if (
                        self.board[square[0] + offset[0]][square[1] + offset[1]].color
                        != color
                        and self.board[square[0] + offset[0]][
                            square[1] + offset[1]
                        ].type
                        == "P"
                    ):
                        return False
        return safe

    # is_valid_move function
    def is_valid_move(self, currsquare, endsquare):
        # is endsquare same as current square? or is currentsquare empty or is endsquare same color as current square? and is the currsquare and endsquare on board
        if currsquare == endsquare:
            return False
        elif self.board[currsquare[0]][currsquare[1]] == None:
            return False
        elif (
            currsquare[0] < 0
            or currsquare[0] > 7
            or currsquare[1] < 0
            or currsquare[1] > 7
        ) or (
            endsquare[0] < 0 or endsquare[0] > 7 or endsquare[1] < 0 or endsquare[1] > 7
        ):
            return False
        color = self.board[currsquare[0]][currsquare[1]].color
        if self.board[endsquare[0]][endsquare[1]] != None:
            if self.board[endsquare[0]][endsquare[1]].color == color:
                return False
            elif self.find_square(endsquare).type == "K":
                return False
        # runs for different types of pieces
        # this one for rooks
        if self.board[currsquare[0]][currsquare[1]].type == "R":
            rook_offsets = [
                (1, 0),
                (2, 0),
                (3, 0),
                (4, 0),
                (5, 0),
                (6, 0),
                (7, 0),
                (-1, 0),
                (-2, 0),
                (-3, 0),
                (-4, 0),
                (-5, 0),
                (-6, 0),
                (-7, 0),
                (0, 1),
                (0, 2),
                (0, 3),
                (0, 4),
                (0, 5),
                (0, 6),
                (0, 7),
                (0, -1),
                (0, -2),
                (0, -3),
                (0, -4),
                (0, -5),
                (0, -6),
                (0, -7),
            ]
            # runs if the end square for the rook is somewhere a rook would go, doesn't matter if it's off the board as that has been dealt with above
            if (
                rook_offsets.count(
                    (endsquare[0] - currsquare[0], endsquare[1] - currsquare[1])
                )
                == 1
            ):
                line = []
                if endsquare[0] - currsquare[0] == 0:
                    if currsquare[1] < endsquare[1]:
                        for i in range(currsquare[1] + 1, endsquare[1]):
                            line.append(self.board[currsquare[0]][i])
                    else:
                        for i in range(currsquare[1] - 1, endsquare[1], -1):
                            line.append(self.board[currsquare[0]][i])
                elif currsquare[1] - currsquare[1] == 0:
                    if currsquare[0] < endsquare[0]:
                        for i in range(currsquare[0] + 1, endsquare[0]):
                            line.append(self.board[i][currsquare[1]])
                    else:
                        for i in range(currsquare[0] - 1, endsquare[0], -1):
                            line.append(self.board[i][currsquare[1]])
                if line.count(None) < len(line):
                    return False
                # checks if the king would be safe after move
                self.move(currsquare, endsquare, realmove=False)
                safe = self.king_safe(self.find_king(color), color)
                self.unmove()
                return safe
            else:
                return False
        # runs for Knights
        elif self.board[currsquare[0]][currsquare[1]].type == "N":
            knight_offsets = [
                (1, 2),
                (2, 1),
                (1, -2),
                (2, -1),
                (-1, 2),
                (-2, 1),
                (-1, -2),
                (-2, -1),
            ]
            # runs if the end square for the knight is somewhere a knight would go
            if (
                knight_offsets.count(
                    (endsquare[0] - currsquare[0], endsquare[1] - currsquare[1])
                )
                == 1
            ):
                # checks if the king would be safe after move
                self.move(currsquare, endsquare, realmove=False)
                safe = self.king_safe(self.find_king(color), color)
                self.unmove()
                return safe
            else:
                return False
        # runs for bishops
        elif self.board[currsquare[0]][currsquare[1]].type == "B":
            bishop_offsets = [
                (7, -7),
                (6, -6),
                (5, -5),
                (4, -4),
                (3, -3),
                (2, -2),
                (1, -1),
                (0, 0),
                (-1, 1),
                (-2, 2),
                (-3, 3),
                (-4, 4),
                (-5, 5),
                (-6, 6),
                (-7, 7),
                (7, 7),
                (6, 6),
                (5, 5),
                (4, 4),
                (3, 3),
                (2, 2),
                (1, 1),
                (0, 0),
                (-1, -1),
                (-2, -2),
                (-3, -3),
                (-4, -4),
                (-5, -5),
                (-6, -6),
                (-7, -7),
            ]
            # runs if the end square for the bishop is somewhere a bishop would go, doesn't matter if it's off the board as that has been dealt with above
            if (
                bishop_offsets.count(
                    (endsquare[0] - currsquare[0], endsquare[1] - currsquare[1])
                )
                == 1
            ):
                line = []
                if (
                    endsquare[0] - currsquare[0] > 0
                    and endsquare[1] - currsquare[1] > 0
                ):
                    for i in range(1, abs(endsquare[0] - currsquare[0])):
                        line.append(self.board[currsquare[0] + i][currsquare[1] + i])
                elif (
                    endsquare[0] - currsquare[0] < 0
                    and endsquare[1] - currsquare[1] < 0
                ):
                    for i in range(1, abs(endsquare[0] - currsquare[0])):
                        line.append(self.board[currsquare[0] - i][currsquare[1] - i])
                elif (
                    endsquare[0] - currsquare[0] < 0
                    and endsquare[1] - currsquare[1] > 0
                ):
                    for i in range(1, abs(endsquare[0] - currsquare[0])):
                        line.append(self.board[currsquare[0] - i][currsquare[1] + i])
                elif (
                    endsquare[0] - currsquare[0] > 0
                    and endsquare[1] - currsquare[1] < 0
                ):
                    for i in range(1, abs(endsquare[0] - currsquare[0])):
                        line.append(self.board[currsquare[0] + i][currsquare[1] - i])
                if line.count(None) < len(line):
                    return False

                # checks if the king would be safe after move
                self.move(currsquare, endsquare, realmove=False)
                safe = self.king_safe(self.find_king(color), color)
                self.unmove()
                return safe
            else:
                return False
        elif self.board[currsquare[0]][currsquare[1]].type == "Q":
            queen_offsets = [
                (1, 0),
                (2, 0),
                (3, 0),
                (4, 0),
                (5, 0),
                (6, 0),
                (7, 0),
                (-1, 0),
                (-2, 0),
                (-3, 0),
                (-4, 0),
                (-5, 0),
                (-6, 0),
                (-7, 0),
                (0, 1),
                (0, 2),
                (0, 3),
                (0, 4),
                (0, 5),
                (0, 6),
                (0, 7),
                (0, -1),
                (0, -2),
                (0, -3),
                (0, -4),
                (0, -5),
                (0, -6),
                (0, -7),
                (7, -7),
                (6, -6),
                (5, -5),
                (4, -4),
                (3, -3),
                (2, -2),
                (1, -1),
                (0, 0),
                (-1, 1),
                (-2, 2),
                (-3, 3),
                (-4, 4),
                (-5, 5),
                (-6, 6),
                (-7, 7),
                (7, 7),
                (6, 6),
                (5, 5),
                (4, 4),
                (3, 3),
                (2, 2),
                (1, 1),
                (0, 0),
                (-1, -1),
                (-2, -2),
                (-3, -3),
                (-4, -4),
                (-5, -5),
                (-6, -6),
                (-7, -7),
            ]
            line = []
            # runs if the end square for the queen is somewhere a queen would go, doesn't matter if it's off the board as that has been dealt with above
            if (
                queen_offsets.count(
                    (endsquare[0] - currsquare[0], endsquare[1] - currsquare[1])
                )
                == 1
            ):
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
                elif (
                    endsquare[0] - currsquare[0] > 0
                    and endsquare[1] - currsquare[1] > 0
                ):
                    for i in range(1, abs(endsquare[0] - currsquare[0])):
                        line.append(self.board[currsquare[0] + i][currsquare[1] + i])
                elif (
                    endsquare[0] - currsquare[0] < 0
                    and endsquare[1] - currsquare[1] < 0
                ):
                    for i in range(1, abs(endsquare[0] - currsquare[0])):
                        line.append(self.board[currsquare[0] - i][currsquare[1] - i])
                elif (
                    endsquare[0] - currsquare[0] < 0
                    and endsquare[1] - currsquare[1] > 0
                ):
                    for i in range(1, abs(endsquare[0] - currsquare[0])):
                        line.append(self.board[currsquare[0] - i][currsquare[1] + i])
                elif (
                    endsquare[0] - currsquare[0] > 0
                    and endsquare[1] - currsquare[1] < 0
                ):
                    for i in range(1, abs(endsquare[0] - currsquare[0])):
                        line.append(self.board[currsquare[0] + i][currsquare[1] - i])
                if line.count(None) < len(line):
                    return False

                # checks if the king would be safe after move
                self.move(currsquare, endsquare, realmove=False)
                safe = self.king_safe(self.find_king(color), color)
                self.unmove()
                return safe
            else:
                return False
        elif self.board[currsquare[0]][currsquare[1]].type == "K":
            king_offsets = [
                (0, 1),
                (0, -1),
                (1, 0),
                (-1, 0),
                (1, 1),
                (1, -1),
                (-1, 1),
                (-1, -1),
            ]
            # runs for a black king
            if color:
                # runs if the end square for the king is somewhere a king would go, doesn't matter if it's off the board as that has been dealt with above
                if (
                    king_offsets.count(
                        (endsquare[0] - currsquare[0], endsquare[1] - currsquare[1])
                    )
                    == 1
                ):
                    # checks if the king would be safe after move
                    self.move(currsquare, endsquare, realmove=False)
                    safe = self.king_safe(self.find_king(color), color)
                    self.unmove()
                    return safe
                # castling on black side
                elif (
                    endsquare == G8
                    and currsquare == E8
                    and self.board[0][6] == None
                    and self.board[0][5] == None
                ):
                    if self.board[0][7] != None:
                        return (
                            # checks all castle rules
                            self.king_safe(E8, color)
                            and self.king_safe(F8, color)
                            and self.king_safe(G8, color)
                            and (not self.king_moved(color))
                            and (not self.rook_moved(color, H8))
                            and self.board[0][7].type == "R"
                            and self.board[0][7].color == color
                        )
                # black king long castle
                elif (
                    endsquare == C8
                    and currsquare == E8
                    and self.board[0][3] == None
                    and self.board[0][2] == None
                    and self.board[0][1] == None
                ):
                    if self.board[0][0] != None:
                        return (
                            # checks castling rules
                            self.king_safe(E8, color)
                            and self.king_safe(D8, color)
                            and self.king_safe(C8, color)
                            and (not self.king_moved(color))
                            and (not self.rook_moved(color, A8))
                            and self.board[0][0].type == "R"
                            and self.board[0][0].color == color
                        )
                else:
                    return False
            # white king
            else:
                # runs if the end square for the king is somewhere a king would go, doesn't matter if it's off the board as that has been dealt with above
                if (
                    king_offsets.count(
                        (endsquare[0] - currsquare[0], endsquare[1] - currsquare[1])
                    )
                    == 1
                ):
                    # checks if the king would be safe after move
                    self.move(currsquare, endsquare, realmove=False)
                    safe = self.king_safe(self.find_king(color), color)
                    self.unmove()
                    return safe
                # white king short castle
                elif (
                    endsquare == G1
                    and currsquare == E1
                    and self.board[7][6] == None
                    and self.board[7][5] == None
                ):
                    # checks all conditions for castling
                    if self.board[7][7] != None:
                        return (
                            self.king_safe(E1, color)
                            and self.king_safe(F1, color)
                            and self.king_safe(G1, color)
                            and (not self.king_moved(color))
                            and (not self.rook_moved(color, H1))
                            and self.board[7][7].type == "R"
                            and self.board[7][7].color == color
                        )
                # white king long castle
                elif (
                    endsquare == C1
                    and currsquare == E1
                    and self.board[7][3] == None
                    and self.board[7][2] == None
                    and self.board[7][1] == None
                ):
                    # checks all conditions for castling
                    if self.board[7][0] != None:
                        return (
                            self.king_safe(E1, color)
                            and self.king_safe(D1, color)
                            and self.king_safe(C1, color)
                            and (not self.king_moved(color))
                            and (not self.rook_moved(color, A1))
                            and self.board[7][0].type == "R"
                            and self.board[7][0].color == color
                        )
                else:
                    return False
        elif self.board[currsquare[0]][currsquare[1]].type == "P":
            if self.board[endsquare[0]][endsquare[1]] != None:
                if self.board[endsquare[0]][endsquare[1]].color == color:
                    return False
            if color:
                if (
                    endsquare[0] == currsquare[0] + 1
                    and endsquare[1] == currsquare[1]
                    and self.board[endsquare[0]][endsquare[1]] == None
                ):
                    # checks if the king would be safe after move
                    self.move(currsquare, endsquare, realmove=False)
                    safe = self.king_safe(self.find_king(color), color)
                    self.unmove()
                    return safe
                elif (
                    endsquare[0] == currsquare[0] + 2
                    and endsquare[1] == currsquare[1]
                    and currsquare[0] == 1
                    and self.board[currsquare[0] + 1][currsquare[1]] == None
                    and self.board[endsquare[0]][endsquare[1]] == None
                ):
                    # checks if the king would be safe after move
                    self.move(currsquare, endsquare, realmove=False)
                    safe = self.king_safe(self.find_king(color), color)
                    self.unmove()
                    return safe
                elif endsquare[0] == currsquare[0] + 1 and (
                    endsquare[1] == currsquare[1] + 1
                    or endsquare[1] == currsquare[1] - 1
                ):
                    if self.board[endsquare[0]][endsquare[1]] != None:
                        if self.board[endsquare[0]][endsquare[1]].color != color:
                            # checks if the king would be safe after move
                            self.move(currsquare, endsquare, realmove=False)
                            safe = self.king_safe(self.find_king(color), color)
                            self.unmove()
                            return safe
                    elif len(self.history) > 0:
                        if (
                            self.history[len(self.history) - 1][2].type == "P"
                            and self.history[len(self.history) - 1][0][0] == 6
                            and self.history[len(self.history) - 1][1][0] == 4
                            and self.history[len(self.history) - 1][2].color != color
                            and currsquare[0] == 4
                            and self.history[len(self.history) - 1][0][1]
                            == endsquare[1]
                        ):
                            # checks if the king would be safe after move
                            self.move(currsquare, endsquare, realmove=False)
                            safe = self.king_safe(self.find_king(color), color)
                            self.unmove()
                            return safe
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                if (
                    endsquare[0] == currsquare[0] - 1
                    and endsquare[1] == currsquare[1]
                    and self.board[endsquare[0]][endsquare[1]] == None
                ):
                    # checks if the king would be safe after move
                    self.move(currsquare, endsquare, realmove=False)
                    safe = self.king_safe(self.find_king(color), color)
                    self.unmove()
                    return safe
                elif (
                    endsquare[0] == currsquare[0] - 2
                    and endsquare[1] == currsquare[1]
                    and currsquare[0] == 6
                    and self.board[currsquare[0] - 1][currsquare[1]] == None
                    and self.board[endsquare[0]][endsquare[1]] == None
                ):
                    # checks if the king would be safe after move
                    self.move(currsquare, endsquare, realmove=False)
                    safe = self.king_safe(self.find_king(color), color)
                    self.unmove()
                    return safe
                elif endsquare[0] == currsquare[0] - 1 and (
                    endsquare[1] == currsquare[1] + 1
                    or endsquare[1] == currsquare[1] - 1
                ):
                    if self.board[endsquare[0]][endsquare[1]] != None:
                        if self.board[endsquare[0]][endsquare[1]].color != color:
                            # checks if the king would be safe after move
                            self.move(currsquare, endsquare, realmove=False)
                            safe = self.king_safe(self.find_king(color), color)
                            self.unmove()
                            return safe
                    elif len(self.history) > 0:
                        if (
                            self.history[len(self.history) - 1][2].type == "P"
                            and self.history[len(self.history) - 1][0][0] == 1
                            and self.history[len(self.history) - 1][1][0] == 3
                            and self.history[len(self.history) - 1][2].color != color
                            and currsquare[0] == 3
                            and self.history[len(self.history) - 1][0][1]
                            == endsquare[1]
                        ):
                            # checks if the king would be safe after move
                            self.move(currsquare, endsquare, realmove=False)
                            safe = self.king_safe(self.find_king(color), color)
                            self.unmove()
                            return safe
                        else:
                            return False
                    else:
                        return False
                else:
                    return False

    # move function
    def move(self, currsquare, endsquare, promo="P", realmove=True):
        # movetype 0-normal 1-capture 2-en passant 3-promotion 4-castle
        movetype = 0
        # set captured piece
        captured_piece = captured_piece = self.find_square(endsquare)
        # set to capture if endsquare is not empty
        if self.board[endsquare[0]][endsquare[1]] != None:
            movetype = 1
        color = self.find_square(currsquare).color
        piece = Piece(
            self.board[currsquare[0]][currsquare[1]].type,
            self.board[currsquare[0]][currsquare[1]].color,
        )
        # castling
        if piece.type == "K":
            if abs(currsquare[1] - endsquare[1]) == 2:
                movetype = 4
                if color:
                    if endsquare == G8:
                        self.board[F8[0]][F8[1]] = self.find_square(H8)
                        self.board[H8[0]][H8[1]] = None
                    elif endsquare == C8:
                        self.board[D8[0]][D8[1]] = self.find_square(A8)
                        self.board[A8[0]][A8[1]] = None
                else:
                    if endsquare == G1:
                        self.board[F1[0]][F1[1]] = self.find_square(H1)
                        self.board[H1[0]][H1[1]] = None
                    elif endsquare == C1:
                        self.board[D1[0]][D1[1]] = self.find_square(A1)
                        self.board[A1[0]][A1[1]] = None
        # en passant
        if (
            abs(endsquare[1] - currsquare[1]) == 1
            and self.board[endsquare[0]][endsquare[1]] == None
            and piece.type == "P"
        ):
            movetype = 2
            if color:
                captured_piece = self.board[endsquare[0] - 1][endsquare[1]]
                self.board[endsquare[0] - 1][endsquare[1]] = None
            else:
                captured_piece = self.board[endsquare[0] + 1][endsquare[1]]
                self.board[endsquare[0] + 1][endsquare[1]] = None

        self.board[endsquare[0]][endsquare[1]] = self.board[currsquare[0]][
            currsquare[1]
        ]
        # promotion
        self.board[currsquare[0]][currsquare[1]] = None
        if piece.type == "P":
            if color:
                if endsquare[0] == 7:
                    movetype = 3
                    self.board[endsquare[0]][endsquare[1]].type = promo
            else:
                if endsquare[0] == 0:
                    movetype = 3
                    self.board[endsquare[0]][endsquare[1]].type = promo

        # switch turn
        self.turn = not self.turn
        # add to history
        self.history.append(
            [currsquare, endsquare, piece, captured_piece, movetype, realmove]
        )
        # append deepcopy of board for threefold check if this move hasnt come from ai
        if realmove:
            self.board_history.append(deepcopy(self.board))

    # unmove function - undoes previous move
    def unmove(self):
        if len(self.history) > 0 and len(self.board_history) > 0:
            # get the move and remove from history
            move = self.history.pop()
            # remove the move from board history if it was recorded
            if move[5]:
                self.board_history.pop()
            # undo turn
            self.turn = not self.turn
            # normal or promotion
            if move[4] == 0 or move[4] == 3:
                self.board[move[0][0]][move[0][1]] = move[2]
                self.board[move[1][0]][move[1][1]] = move[3]
            # capture
            elif move[4] == 1:
                self.board[move[0][0]][move[0][1]] = move[2]
                self.board[move[1][0]][move[1][1]] = move[3]
            # en passant
            elif move[4] == 2:
                self.board[move[0][0]][move[0][1]] = move[2]
                self.board[move[1][0]][move[1][1]] = None
                if move[2].color:
                    self.board[move[1][0] - 1][move[1][1]] = move[3]
                else:
                    self.board[move[1][0] + 1][move[1][1]] = move[3]
            # castle
            elif move[4] == 4:
                self.board[move[0][0]][move[0][1]] = move[2]
                self.board[move[1][0]][move[1][1]] = None
                if move[1] == G1:
                    self.board[H1[0]][H1[1]] = self.board[F1[0]][F1[1]]
                    self.board[F1[0]][F1[1]] = None
                elif move[1] == G8:
                    self.board[H8[0]][H8[1]] = self.board[F8[0]][F8[1]]
                    self.board[F8[0]][F8[1]] = None
                elif move[1] == C1:
                    self.board[A1[0]][A1[1]] = self.board[D1[0]][D1[1]]
                    self.board[D1[0]][D1[1]] = None
                elif move[1] == C8:
                    self.board[A8[0]][A8[1]] = self.board[D8[0]][D8[1]]
                    self.board[D8[0]][D8[1]] = None

    # find_king function
    def find_king(self, color):
        #search for king
        for rank in range(len(self.board)):
            for square in range(len(self.board[rank])):
                if self.board[rank][square] != None:
                    if (
                        self.board[rank][square].color == color
                        and self.board[rank][square].type == "K"
                    ):
                        return (rank, square)
    #check if the king of specified side has moved in the history
    def king_moved(self, color):
        for move in self.history:
            if move[2].type == "K" and move[2].color == color:
                return True
        return False
    
    #check if the rook of specified side has moved in the history of its starting square
    def rook_moved(self, color, square):
        for move in self.history:
            if (
                move[2].type == "R"
                and move[2].color == color
                and (move[0] == square or move[1] == square)
            ):
                return True
        return False

    # valid_moves(square)
    # returns all valid moves for piece on that square
    def valid_moves(self, square):
        #set moves list to empty
        moves = []
        #runs if there is something on the square to move from, otherwise no moves will be added to the list and an empty list will be returned
        if self.board[square[0]][square[1]] != None:
            #kings
            if self.board[square[0]][square[1]].type == "K":
                #checks all of the possible moves for a king and returns each one that is true
                king_offsets = [
                    (0, 1),
                    (0, -1),
                    (1, 0),
                    (-1, 0),
                    (1, 1),
                    (1, -1),
                    (-1, 1),
                    (-1, -1),
                    (0, 2),
                    (0, -2),
                ]
                for offset in king_offsets:
                    newsquare = (square[0] + offset[0], square[1] + offset[1])
                    if self.is_valid_move(square, newsquare):
                        moves.append(newsquare)
            elif self.board[square[0]][square[1]].type == "Q":
                #checks all of the possible moves for a queen and returns each one that is true
                queen_offsets = [
                    (1, 0),
                    (2, 0),
                    (3, 0),
                    (4, 0),
                    (5, 0),
                    (6, 0),
                    (7, 0),
                    (-1, 0),
                    (-2, 0),
                    (-3, 0),
                    (-4, 0),
                    (-5, 0),
                    (-6, 0),
                    (-7, 0),
                    (0, 1),
                    (0, 2),
                    (0, 3),
                    (0, 4),
                    (0, 5),
                    (0, 6),
                    (0, 7),
                    (0, -1),
                    (0, -2),
                    (0, -3),
                    (0, -4),
                    (0, -5),
                    (0, -6),
                    (0, -7),
                    (7, -7),
                    (6, -6),
                    (5, -5),
                    (4, -4),
                    (3, -3),
                    (2, -2),
                    (1, -1),
                    (0, 0),
                    (-1, 1),
                    (-2, 2),
                    (-3, 3),
                    (-4, 4),
                    (-5, 5),
                    (-6, 6),
                    (-7, 7),
                    (7, 7),
                    (6, 6),
                    (5, 5),
                    (4, 4),
                    (3, 3),
                    (2, 2),
                    (1, 1),
                    (0, 0),
                    (-1, -1),
                    (-2, -2),
                    (-3, -3),
                    (-4, -4),
                    (-5, -5),
                    (-6, -6),
                    (-7, -7),
                ]
                for offset in queen_offsets:
                    newsquare = (square[0] + offset[0], square[1] + offset[1])
                    if self.is_valid_move(square, newsquare):
                        moves.append(newsquare)
            elif self.board[square[0]][square[1]].type == "R":
                #checks all of the possible moves for a rook and returns each one that is true
                rook_offsets = [
                    (1, 0),
                    (2, 0),
                    (3, 0),
                    (4, 0),
                    (5, 0),
                    (6, 0),
                    (7, 0),
                    (-1, 0),
                    (-2, 0),
                    (-3, 0),
                    (-4, 0),
                    (-5, 0),
                    (-6, 0),
                    (-7, 0),
                    (0, 1),
                    (0, 2),
                    (0, 3),
                    (0, 4),
                    (0, 5),
                    (0, 6),
                    (0, 7),
                    (0, -1),
                    (0, -2),
                    (0, -3),
                    (0, -4),
                    (0, -5),
                    (0, -6),
                    (0, -7),
                ]
                for offset in rook_offsets:
                    newsquare = (square[0] + offset[0], square[1] + offset[1])
                    if self.is_valid_move(square, newsquare):
                        moves.append(newsquare)
            elif self.board[square[0]][square[1]].type == "B":
                #checks all of the possible moves for a bishop and returns each one that is true
                bishop_offsets = [
                    (7, -7),
                    (6, -6),
                    (5, -5),
                    (4, -4),
                    (3, -3),
                    (2, -2),
                    (1, -1),
                    (0, 0),
                    (-1, 1),
                    (-2, 2),
                    (-3, 3),
                    (-4, 4),
                    (-5, 5),
                    (-6, 6),
                    (-7, 7),
                    (7, 7),
                    (6, 6),
                    (5, 5),
                    (4, 4),
                    (3, 3),
                    (2, 2),
                    (1, 1),
                    (0, 0),
                    (-1, -1),
                    (-2, -2),
                    (-3, -3),
                    (-4, -4),
                    (-5, -5),
                    (-6, -6),
                    (-7, -7),
                ]
                for offset in bishop_offsets:
                    newsquare = (square[0] + offset[0], square[1] + offset[1])
                    if self.is_valid_move(square, newsquare):
                        moves.append(newsquare)
            elif self.board[square[0]][square[1]].type == "N":
                #checks all of the possible moves for a knight and returns each one that is true
                knight_offsets = [
                    (1, 2),
                    (2, 1),
                    (1, -2),
                    (2, -1),
                    (-1, 2),
                    (-2, 1),
                    (-1, -2),
                    (-2, -1),
                ]
                for offset in knight_offsets:
                    newsquare = (square[0] + offset[0], square[1] + offset[1])
                    if self.is_valid_move(square, newsquare):
                        moves.append(newsquare)
            elif self.board[square[0]][square[1]].type == "P":
                #checks all of the possible moves for a pawn and returns each one that is true
                if self.board[square[0]][square[1]].color:
                    pawn_offsets = [(1, 0), (2, 0), (1, 1), (1, -1)]
                else:
                    pawn_offsets = [(-1, 0), [-2, 0], (-1, 1), (-1, -1)]
                for offset in pawn_offsets:
                    newsquare = (square[0] + offset[0], square[1] + offset[1])
                    if self.is_valid_move(square, newsquare):
                        moves.append(newsquare)
        return moves

    # all_valid_moves(side)
    # returns all valid moves for all pieces for the side provided
    def all_valid_moves(self, side):
        #squares are all the squares that the specified side has a piece
        squares = []
        #moves are all the squares that the piece can end up along with the square it started at
        moves = []
        #look for pieces of specified side
        for rank in range(8):
            for file in range(8):
                if self.board[rank][file] != None:
                    if self.board[rank][file].color == side:
                        squares.append((rank, file))
        #check the valid moves for each square
        for square in squares:
            move_piece = self.valid_moves(square)
            for move in move_piece:
                #movetypes for move ordering to make a better chance of effective ab pruning
                movetype = 0
                #check if its a capture
                if self.find_square(move) != None:
                    movetype = 1
                #check if its a check
                self.move(square, move, realmove=False)
                if not self.king_safe(self.find_king(not side), not side):
                    movetype = 2
                self.unmove()
                #if its promotion add the possible pieces to promote to
                if (
                    self.board[square[0]][square[1]].type == "P"
                    and square[0] == 6
                    and side
                ):
                    promos = ["Q", "R", "N", "B"]
                    for promo in promos:
                        moves.append((square, move, movetype, promo))
                elif (
                    self.board[square[0]][square[1]].type == "P"
                    and square[0] == 1
                    and not side
                ):
                    promos = ["Q", "R", "N", "B"]
                    for promo in promos:
                        moves.append((square, move, movetype, promo))
                else:
                    moves.append((square, move, movetype))
        #return the moves
        return moves

    #return a tuple consiting of the total material points of white and then the total for black.
    def material(self):
        mw = mb = 0
        for rank in range(8):
            for file in range(8):
                if self.find_square((rank, file)) != None:
                    if self.find_square((rank, file)).color:
                        type = self.find_square((rank, file)).type
                        if type == "Q":
                            mb += 9
                        elif type == "R":
                            mb += 5
                        elif type == "B" or type == "N":
                            mb += 3
                        elif type == "P":
                            mb += 1
                    else:
                        type = self.find_square((rank, file)).type
                        if type == "Q":
                            mw += 9
                        elif type == "R":
                            mw += 5
                        elif type == "B" or type == "N":
                            mw += 3
                        elif type == "P":
                            mw += 1
        return (mw, mb)
    #return the material difference between white and black - 0 for equal, >0 for white has more and <0 for white has less
    def material_diff(self):
        material = self.material()
        return material[0] - material[1]

    #count the ammount of pieces on the board
    def num_pieces(self):
        count = 0
        for rank in range(8):
            for file in range(8):
                if self.find_square((rank, file)) != None:
                    count += 1
        return count

    #return if its a fifty move draw - 100 total moves have been played with no pawns or captures
    def fifty_move(self):
        if len(self.history) >= 100:
            history = self.history[len(self.history) - 100 : len(self.history) - 1]
            for move in history:
                if move[2].type == "P" or move[3] != None:
                    return False
            return True
        else:
            return False

    #find if its an insufficient material draw - not enough material on the board to end in checkmate no matter what
    def insufficient_material(self):
        pawns = False
        rooks = False
        queens = False
        for rank in range(8):
            for file in range(8):
                if self.find_square((rank, file)) != None:
                    if self.find_square((rank, file)).type == "P":
                        pawns = True
                    elif self.find_square((rank, file)).type == "R":
                        rooks = True
                    elif self.find_square((rank, file)).type == "Q":
                        queens = True
        if pawns or rooks or queens:
            return False
        else:
            bn_white = 0
            bn_black = 0
            for rank in range(8):
                for file in range(8):
                    piece = self.find_square((rank, file))
                    if piece != None:
                        if piece.type == "N" or piece.type == "B":
                            if piece.color:
                                bn_black += 1
                            else:
                                bn_white += 1
            return not bn_white > 1 or bn_black > 1
