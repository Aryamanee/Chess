import board
import copy

# Move Analyzer
# takes current board situation and color of analyzing
class eval():
    def __init__(self, gameboard: board.Board):
        self.board = gameboard

    # check_position function
    # checks material advantage of side
    def check_position(self, Board = []):
        if Board == []:
             Board = self.board
        midgamethreshold = 15
        endgamethreshold = 60
        pieces = Board.material()
        pieces_white = pieces[0]
        pieces_black = pieces[1]
        king_safety_white = self.king_safety(False, Board)
        king_safety_black = self.king_safety(True, Board)
        development_white = [Board.find_square(board.B1) == None, Board.find_square(board.C1) == None, Board.find_square(board.F1) == None, Board.find_square(board.G1) == None, Board.find_square(board.A1) == None, Board.find_square(board.H1) == None, Board.find_square(board.A2) == None, Board.find_square(board.B2) == None, Board.find_square(board.C2) == None, Board.find_square(board.D2) == None, Board.find_square(board.E2) == None, Board.find_square(board.F2) == None, Board.find_square(board.G2) == None, Board.find_square(board.H2) == None].count(True)
        development_black = [Board.find_square(board.B8) == None, Board.find_square(board.C8) == None, Board.find_square(board.F8) == None, Board.find_square(board.G8) == None, Board.find_square(board.A8) == None, Board.find_square(board.H8) == None, Board.find_square(board.A7) == None, Board.find_square(board.B7) == None, Board.find_square(board.C7) == None, Board.find_square(board.D7) == None, Board.find_square(board.E7) == None, Board.find_square(board.F7) == None, Board.find_square(board.G7) == None, Board.find_square(board.H7) == None].count(True)
        control_white = len(Board.all_valid_moves(False))
        control_black = len(Board.all_valid_moves(True))
        phase =  (development_white + development_black)+78-pieces_white-pieces_black
        if phase < midgamethreshold:
            center_control_weight = 1
            king_saftey_weight = 0.2
            square_control_weight = 0.1
            material_advantage_weight = 1
        elif phase < endgamethreshold:
            center_control_weight = 1
            king_saftey_weight = 0.2
            square_control_weight = 0.1
            material_advantage_weight = 1
        else:
            center_control_weight = 1
            king_saftey_weight = 0.1
            square_control_weight = 1
            material_advantage_weight = 1
        return (king_safety_white - king_safety_black)*king_saftey_weight + (control_white - control_black)*square_control_weight + (pieces_white - pieces_black)*material_advantage_weight
    def king_safety(self, side, Board: board.Board = []):
        if Board == []:
             Board = self.board
        king_square = Board.find_king(side)
        if side:
            king_distance_penalty = -king_square[0]
        else:
            king_distance_penalty = king_square[0]-7
        king_offsets = [(0,1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        squares_around_king = []
        for offset in king_offsets:
            if king_square[0] + offset[0] >=0 and king_square[0] + offset[0] <=7 and king_square[1] + offset[1] >=0 and king_square[1] + offset[1] <=7:
                squares_around_king.append((king_square[0]+offset[0], king_square[1]+offset[1]))
        opponent_moves = Board.all_valid_moves(not side)
        king_safety = 0
        for move in range(len(opponent_moves)):
            opponent_moves[move] = opponent_moves[move][1]
        for move in opponent_moves:
            king_safety -= squares_around_king.count(move) == 1
        for square in squares_around_king:
            if Board.find_square(square) != None:
                if Board.find_square(square).color == side:
                    king_safety+=1
        king_safety += king_distance_penalty
        return king_safety
        
    # checks if king is exposed
    # checks if pieces have much play or they are in a closed position
    # checks for forced check sequences in the next 4 moves that may end in a checkmate
    # uses these factors to determine a number that represents if the game is in blacks favor or whites favor
    # find best_move function
    # uses all_valid_move function of board and runs on a temporary board
    # evaluates each new temporary board and ranks it using check_position function
    # returns move with highest rating

    #https://www.youtube.com/watch?v=l-hh51ncgDI&ab_channel=SebastianLague - base minimax code
    def minimax(self, Board: board.Board, depth, side, alpha = -float("inf"), beta = float("inf")):
        if Board.all_valid_moves(False) == []:
            if Board.king_safe(Board.find_king(False), False):
                return 0
            else:
                return -float("inf")
        elif Board.all_valid_moves(True) == []:
            if Board.king_safe(Board.find_king(True), True):
                return 0
            else:
                return float("inf")
        elif depth == 0:
            return self.check_position(Board)
        if side:
            minimum_evaluation = float("inf")
            for move in Board.all_valid_moves(side):
                simulated_board = copy.deepcopy(Board)
                if len(move) == 2:
                    simulated_board.move(move[0], move[1])
                else:
                    simulated_board.move(move[0], move[1], promo = move[2])
                evaluation = self.minimax(simulated_board, depth-1, not side, alpha, beta)
                minimum_evaluation = min(evaluation, minimum_evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return minimum_evaluation
        else:
            maximum_evaluation = -float("inf")
            for move in Board.all_valid_moves(side):
                simulated_board = copy.deepcopy(Board)
                if len(move) == 2:
                    simulated_board.move(move[0], move[1])
                else:
                    simulated_board.move(move[0], move[1], promo = move[2])
                evaluation = self.minimax(simulated_board, depth-1, not side, alpha, beta)
                maximum_evaluation = max(evaluation, maximum_evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return maximum_evaluation
