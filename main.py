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

gameboard = board.Board()
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
running = True

turn = False
selected = None
squares = []
while running:
  for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
          mousepos = pygame.mouse.get_pos()
          mousesquare = (mousepos[1]//75, mousepos[0]//75)
          if gameboard.board[mousesquare[0]][mousesquare[1]] == None:
            if selected != None:
              if squares.count(mousesquare)==1:
                gameboard.move(selected, mousesquare)
                selected = None
                turn = not turn
          else:
            if gameboard.board[mousesquare[0]][mousesquare[1]].color == turn:
              if mousesquare == selected:
                selected = None
              else:
                selected = mousesquare
            else:
              if selected!=None:
                if squares.count(mousesquare) == 1:
                  gameboard.move(selected, mousesquare)
                  selected = None
                  turn = not turn

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
  if selected != None:
    squares = gameboard.valid_moves(selected)
  else:
    squares = []
  for square in squares:
    if gameboard.board[square[0]][square[1]] == None:
      pygame.draw.rect(screen, (0, 255, 0), (square[1]*75+25, square[0]*75+25, 25, 25))
    else:
      pygame.draw.rect(screen, (0, 255, 0), (square[1]*75, square[0]*75, 75, 75), width = 5)
  for rank in range(8):
    for file in range(8):
      check = False
      if gameboard.board[rank][file] != None:
        if gameboard.board[rank][file].color:
          if gameboard.board[rank][file].type == "B":
            piece = piece_b
          elif gameboard.board[rank][file].type == "K":
            piece = piece_k
            check = not gameboard.king_safe(gameboard.find_king(True), True)
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
            check = not gameboard.king_safe(gameboard.find_king(False), False)
          elif gameboard.board[rank][file].type == "N":
            piece = piece_N
          elif gameboard.board[rank][file].type == "P":
            piece = piece_P
          elif gameboard.board[rank][file].type == "Q":
            piece = piece_Q
          elif gameboard.board[rank][file].type == "R":
            piece = piece_R
        if check:
          pygame.draw.rect(screen, (255, 0, 0), (75*file, 75*rank, 75, 75))
        screen.blit(piece, (75*file, 75*rank))

  pygame.display.flip()
  clock.tick(60)