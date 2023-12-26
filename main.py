import board
gameboard = board.Board(position="1q4k1/8/8/6n1/1R6/8/6Q1/1K6")

line = len(gameboard.board)
for i in gameboard.board:
  print(str(line) + " ", end="")
  for k in i:
    if k != None:
      if not k.color:
        print("[" + k.type +"]", end = "")
      else:
        print("[" + k.type.lower() + "]", end = "")
    else:
      print("[ ]", end = "")
  print("\n")
  line-=1
print("   A  B  C  D  E  F  G  H")
print(gameboard.king_safe(gameboard.find_king(True), True))
print(gameboard.is_valid_move(board.B4, board.B6))