# Aryaman Sawhney
# evaluation.py
# a function that evaluates statically and minimax to sort through options  - this is the base of the ai

# import the board
import board


# Move Analyzer
# takes current board situation
class eval:
    def __init__(self, gameboard: board.Board):
        self.board = gameboard

    # check_position function
    def check_position(self):
        # the thresholds that define game development
        midgamethreshold = 15
        endgamethreshold = 60
        # get all the pieces
        pieces = self.board.material()
        # get the ammount of material white has and black has
        pieces_white = pieces[0]
        pieces_black = pieces[1]
        # gets the king safety values
        king_safety_white = self.king_safety(False)
        king_safety_black = self.king_safety(True)
        # sets a number which shows how many white minor pieces and pawns are off their original squares
        development_white = [
            self.board.find_square(board.B1) == None,
            self.board.find_square(board.C1) == None,
            self.board.find_square(board.F1) == None,
            self.board.find_square(board.G1) == None,
            self.board.find_square(board.A1) == None,
            self.board.find_square(board.H1) == None,
            self.board.find_square(board.A2) == None,
            self.board.find_square(board.B2) == None,
            self.board.find_square(board.C2) == None,
            self.board.find_square(board.D2) == None,
            self.board.find_square(board.E2) == None,
            self.board.find_square(board.F2) == None,
            self.board.find_square(board.G2) == None,
            self.board.find_square(board.H2) == None,
        ].count(True)
        # sets a number which shows how many black minor pieces and pawns are off their original squares
        development_black = [
            self.board.find_square(board.B8) == None,
            self.board.find_square(board.C8) == None,
            self.board.find_square(board.F8) == None,
            self.board.find_square(board.G8) == None,
            self.board.find_square(board.A8) == None,
            self.board.find_square(board.H8) == None,
            self.board.find_square(board.A7) == None,
            self.board.find_square(board.B7) == None,
            self.board.find_square(board.C7) == None,
            self.board.find_square(board.D7) == None,
            self.board.find_square(board.E7) == None,
            self.board.find_square(board.F7) == None,
            self.board.find_square(board.G7) == None,
            self.board.find_square(board.H7) == None,
        ].count(True)
        # sets the ammount of white and black control on the board judged by the ammount of valid squares they have to land on
        control_white = len(self.board.all_valid_moves(False))
        control_black = len(self.board.all_valid_moves(True))
        # the number thats used to judge game development
        phase = (
            (development_white + development_black) + 78 - pieces_white - pieces_black
        )
        # list of black and white pawns, gets populated in the loop
        pawns_white = []
        pawns_black = []
        for rank in range(8):
            for file in range(8):
                if self.board.find_square((rank, file)) != None:
                    if self.board.find_square((rank, file)).type == "P":
                        if self.board.find_square((rank, file)).color:
                            pawns_black.append((rank, file))
                        else:
                            pawns_white.append((rank, file))
        # sets how far the pawns are to the end for each side
        pawn_to_end_white = 0
        pawn_to_end_black = 0
        for pawn in pawns_white:
            pawn_to_end_white += pawn[0]
        for pawn in pawns_black:
            pawn_to_end_black += 7 - pawn[0]
        # runs for opening
        if phase < midgamethreshold:
            # king safety is important, so is square control and so is material advantage, pawns to the other side not so much
            king_saftey_weight = 0.1
            square_control_weight = 0.05
            material_advantage_weight = 1
            pawn_to_end_weight = 0.05
        elif phase < endgamethreshold:
            # midgame, king safety is important, so is square control, material advantage is quite important but getting the pawns to the end not so much
            king_saftey_weight = 0.1
            square_control_weight = 0.075
            material_advantage_weight = 1.5
            pawn_to_end_weight = 0.05
        # endgame
        else:
            # king needs to come out more, square control is still important, material advantage is important but getting the pawns to the end is quite important
            king_saftey_weight = 0.075
            square_control_weight = 0.05
            material_advantage_weight = 1
            pawn_to_end_weight = 0.2
        # return the weighted score of the positon(positive good for white, negative good for black)
        return (
            (king_safety_white - king_safety_black) * king_saftey_weight
            + (control_white - control_black) * square_control_weight
            + (pieces_white - pieces_black) * material_advantage_weight
            + (pawn_to_end_white - pawn_to_end_black) * pawn_to_end_weight
        )

    # function that determines the safety of the king
    def king_safety(self, side):
        # get the square the king is on for the side provided
        king_square = self.board.find_king(side)
        # penalty for the king being away from the right side of the board.
        if side:
            king_distance_penalty = -king_square[0]
        else:
            king_distance_penalty = king_square[0] - 7
        # offsets that are around the king
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
        # calculate squares around king
        squares_around_king = []
        for offset in king_offsets:
            if (
                king_square[0] + offset[0] >= 0
                and king_square[0] + offset[0] <= 7
                and king_square[1] + offset[1] >= 0
                and king_square[1] + offset[1] <= 7
            ):
                squares_around_king.append(
                    (king_square[0] + offset[0], king_square[1] + offset[1])
                )
        opponent_moves = self.board.all_valid_moves(not side)
        king_safety = 0
        # check how many opponent pieces control squares around the king
        for move in range(len(opponent_moves)):
            opponent_moves[move] = opponent_moves[move][1]
        for move in opponent_moves:
            king_safety -= squares_around_king.count(move) == 1
        for square in squares_around_king:
            if self.board.find_square(square) != None:
                if self.board.find_square(square).color == side:
                    king_safety += 1
        king_safety += king_distance_penalty
        # return the safety of the king
        return king_safety

    # play best move function
    def play_best_move(self, depth):
        # stop the board from rendering as rendering would show all the moves that are being calculated
        self.board.render = False
        # find best move
        best_move = self.find_best_move(depth)
        # runs if its a non promoting move
        if len(best_move) == 3:
            self.board.move(best_move[0], best_move[1], realmove=False)
        # runs if its a promoting move
        else:
            self.board.move(best_move[0], best_move[1], best_move[3], realmove=False)
        # start rendering on the board again
        self.board.render = True

    # find best move function
    def find_best_move(self, depth):
        # sets alpha beta move values
        alpha = -float("inf")
        beta = float("inf")
        # no best move so far
        best_move = None
        # sets the side to the current turn on the board
        side = self.board.turn
        # sets all of the moves to look at
        valid_moves_side = self.board.all_valid_moves(side)
        # returns None if depth is 0
        if depth == 0:
            return best_move
        # starts minimax for the black side
        if side:
            # sets the worst position to best for white
            minimum_evaluation = float("inf")
            # order the moves - checks, captures, normal moves for a higher chance of effective ab pruning
            valid_moves_side.sort(key=lambda x: x[2], reverse=True)
            for move in valid_moves_side:
                # try the move, without recording the move for threefold as that is very slow
                if len(move) == 3:
                    self.board.move(move[0], move[1], realmove=False)
                else:
                    self.board.move(move[0], move[1], promo=move[3], realmove=False)
                # get the evaluation by calling minimax
                evaluation = self.minimax(depth - 1, not side, alpha, beta)
                # updates best move if the move is better
                if evaluation <= minimum_evaluation:
                    minimum_evaluation = evaluation
                    best_move = move
                # undo move
                self.board.unmove()
                if evaluation == -float("inf"):
                    # return move if it results in checkmate
                    return best_move
                # sets beta, break out if beta goes under or is equal to alpha
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            # returns move
            return best_move
        # starts minimax for the white side
        else:
            maximum_evaluation = -float("inf")
            # order the moves - checks, captures, normal moves for a higher chance of effective ab pruning
            valid_moves_side.sort(key=lambda x: x[2], reverse=True)
            for move in valid_moves_side:
                # try the move, without recording the move for threefold as that is very slow realmove = False indicates that
                if len(move) == 3:
                    self.board.move(move[0], move[1], realmove=False)
                else:
                    self.board.move(move[0], move[1], promo=move[3], realmove=False)
                # get the evaluation by calling minimax
                evaluation = self.minimax(depth - 1, not side, alpha, beta)
                # updates best move if the move is better
                if evaluation >= maximum_evaluation:
                    maximum_evaluation = evaluation
                    best_move = move
                # undo move
                self.board.unmove()
                # return move if it results in checkmate
                if evaluation == float("inf"):
                    return best_move
                # set alpha
                alpha = max(alpha, evaluation)
                # break out if beta is less than or equal to alpha
                if beta <= alpha:
                    break
                # returns move
            return best_move

    # https://www.youtube.com/watch?v=l-hh51ncgDI&ab_channel=SebastianLague - minimax psuedocode
    # minimax function
    def minimax(self, depth, side, alpha=-float("inf"), beta=float("inf")):
        # sets all valid moves for side
        valid_moves_side = self.board.all_valid_moves(side)
        # returns 0, otherwise returns checkmate if no moves are available
        if valid_moves_side == []:
            if self.board.king_safe(self.board.find_king(side), side):
                return 0
            else:
                if side:
                    return float("inf")
                else:
                    return -float("inf")
        elif self.board.fifty_move():
            return 0
        elif self.board.insufficient_material():
            return 0
        # returns static evaluation on 0 depth reached
        elif depth == 0:
            return self.check_position()

        # runs for black to play
        if side:
            # sets worst positon to white win
            minimum_evaluation = float("inf")
            # order moves
            valid_moves_side.sort(key=lambda x: x[2], reverse=True)
            # try the move, get an evaluation and unmove, return the evaluation
            for move in valid_moves_side:
                if len(move) == 3:
                    self.board.move(move[0], move[1], realmove=False)
                else:
                    self.board.move(move[0], move[1], promo=move[3], realmove=False)
                evaluation = self.minimax(depth - 1, not side, alpha, beta)
                minimum_evaluation = min(evaluation, minimum_evaluation)
                beta = min(beta, evaluation)
                self.board.unmove()
                if beta <= alpha:
                    break
            return minimum_evaluation

        # white to play
        else:
            # try the move, get an evaluation and unmove, return the evaluation
            maximum_evaluation = -float("inf")
            valid_moves_side.sort(key=lambda x: x[2], reverse=True)
            for move in valid_moves_side:
                if len(move) == 3:
                    self.board.move(move[0], move[1], realmove=False)
                else:
                    self.board.move(move[0], move[1], promo=move[3], realmove=False)
                evaluation = self.minimax(depth - 1, not side, alpha, beta)
                maximum_evaluation = max(evaluation, maximum_evaluation)
                alpha = max(alpha, evaluation)
                self.board.unmove()
                if beta <= alpha:
                    break
            return maximum_evaluation
