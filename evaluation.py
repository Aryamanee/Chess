import board

# Move Analyzer
# takes current board situation and color of analyzing
class eval():
    def __init__(self, gameboard: board.Board):
        self.board = gameboard

    # check_position function
    # checks material advantage of side
    def check_position(self):
        midgamethreshold = 10
        endgamethreshold = 20
        development_white = [self.board.find_square(board.B1) == None, self.board.find_square(board.C1) == None, self.board.find_square(board.F1) == None, self.board.find_square(board.G1) == None, self.board.find_square(board.A1) == None, self.board.find_square(board.H1) == None, self.board.find_square(board.A2) == None, self.board.find_square(board.B2) == None, self.board.find_square(board.C2) == None, self.board.find_square(board.D2) == None, self.board.find_square(board.E2) == None, self.board.find_square(board.F2) == None, self.board.find_square(board.G2) == None, self.board.find_square(board.H2) == None].count(True)
        development_black = [self.board.find_square(board.B8) == None, self.board.find_square(board.C8) == None, self.board.find_square(board.F8) == None, self.board.find_square(board.G8) == None, self.board.find_square(board.A8) == None, self.board.find_square(board.H8) == None, self.board.find_square(board.A7) == None, self.board.find_square(board.B7) == None, self.board.find_square(board.C7) == None, self.board.find_square(board.D7) == None, self.board.find_square(board.E7) == None, self.board.find_square(board.F7) == None, self.board.find_square(board.G7) == None, self.board.find_square(board.H7) == None].count(True)
        return development_white - development_black + self.board.material_diff()
    # checks if king is exposed
    # checks if pieces have much play or they are in a closed position
    # checks for forced check sequences in the next 4 moves that may end in a checkmate
    # uses these factors to determine a number that represents if the game is in blacks favor or whites favor
    # find best_move function
    # uses all_valid_move function of board and runs on a temporary board
    # evaluates each new temporary board and ranks it using check_position function
    # returns move with highest rating