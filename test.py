import board

Board = board.Board("r5k1/2p2r2/1p1p2p1/8/p1qPP2p/K5Q1/1P6/8")
print(Board.king_safe(Board.find_king(False), False))