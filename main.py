import board
gameboard = board.Board(position="rb2k1br/ppqp1ppp/2npbn2/2b1p3/2B1P3/2NPBN2/PPPQ1PPP/R3K2R")

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
print(gameboard.is_valid_move(board.E8, board.C8))