import board
import evaluation

Board = board.Board("1r3b1k/5Qp1/p6B/q1Pp4/2p5/5P1P/P1K2P2/3R2R1")
eval = evaluation.eval(Board)

print(eval.minimax(3, True))