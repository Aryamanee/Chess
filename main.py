import board
gameboard = board.Board()

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
print(gameboard.is_valid_move(board.B7, board.B6))