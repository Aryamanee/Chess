import board

# Move Analyzer
# takes current board situation and color of analyzing
class eval():
    def __init__(self, gameboard: board.Board):
        self.board = gameboard
    #def
    # check_position function
    # checks material advantage of side
    # checks if king is exposed
    # checks if pieces have much play or they are in a closed position
    # checks for forced check sequences in the next 4 moves that may end in a checkmate
    # uses these factors to determine a number that represents if the game is in blacks favor or whites favor
    # find best_move function
    # uses all_valid_move function of board and runs on a temporary board
    # evaluates each new temporary board and ranks it using check_position function
    # returns move with highest rating