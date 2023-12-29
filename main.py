import board
import pygame

piece_B = pygame.image.load("assets/pieces/white-bishop.png")
piece_K = pygame.image.load("assets/pieces/white-king.png")
piece_N = pygame.image.load("assets/pieces/white-knight.png")
piece_P = pygame.image.load("assets/pieces/white-pawn.png")
piece_Q = pygame.image.load("assets/pieces/white-queen.png")
piece_R = pygame.image.load("assets/pieces/white-rook.png")
piece_b = pygame.image.load("assets/pieces/black-bishop.png")
piece_k = pygame.image.load("assets/pieces/black-king.png")
piece_n = pygame.image.load("assets/pieces/black-knight.png")
piece_p = pygame.image.load("assets/pieces/black-pawn.png")
piece_q = pygame.image.load("assets/pieces/black-queen.png")
piece_r = pygame.image.load("assets/pieces/black-rook.png")

gameboard = board.Board("k6K/1Q7/8/8/8/8/8/8")
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
running = True
while running:
  for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
  for i in range(8):
    for j in range(8):
      if i%2==0 and j%2 == 0:
         color = (204, 183, 174)
      elif i%2 == 0 and j%2 != 0:
         color = (112, 102, 119)
      elif i%2 != 0 and j%2 == 0:
         color = (112, 102, 119)
      else:
         color = (204, 183, 174)
      pygame.draw.rect(screen, color, (75*i, 75*j, 75, 75))
  for rank in range(8):
    for file in range(8):
      if gameboard.board[rank][file] != None:
        if gameboard.board[rank][file].color:
          if gameboard.board[rank][file].type == "B":
            piece = piece_b
          elif gameboard.board[rank][file].type == "K":
            piece = piece_k
          elif gameboard.board[rank][file].type == "N":
            piece = piece_n
          elif gameboard.board[rank][file].type == "P":
            piece = piece_p
          elif gameboard.board[rank][file].type == "Q":
            piece = piece_q
          elif gameboard.board[rank][file].type == "R":
            piece = piece_r
        else:
          if gameboard.board[rank][file].type == "B":
            piece = piece_B
          elif gameboard.board[rank][file].type == "K":
            piece = piece_K
          elif gameboard.board[rank][file].type == "N":
            piece = piece_N
          elif gameboard.board[rank][file].type == "P":
            piece = piece_P
          elif gameboard.board[rank][file].type == "Q":
            piece = piece_Q
          elif gameboard.board[rank][file].type == "R":
            piece = piece_R
        screen.blit(piece, (75*file, 75*rank))

  pygame.display.flip()
  clock.tick(60)









"""line = len(gameboard.board)
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
print(gameboard.is_valid_move(board.B7, board.B5))"""