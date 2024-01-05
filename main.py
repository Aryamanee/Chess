import board
import pygame
import datetime
import evaluation

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

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

def promote(side, time_control, time_w, time_b):
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          return None, time_w, time_b
      elif event.type == 0 and time_control != (-1, -1):
            if side:
              time_b -= 1
            else:
              time_w -= 1
      elif event.type == pygame.MOUSEBUTTONDOWN:
        mousepos = pygame.mouse.get_pos()
        if mousepos[0]>300 and mousepos[0]<375 and mousepos[1]>262.5 and mousepos[1]<337.5:
          return "Q", time_w, time_b
        elif mousepos[0]>375 and mousepos[0]<450 and mousepos[1]>262.5 and mousepos[1]<337.5:
          return "R", time_w, time_b
        elif mousepos[0]>450 and mousepos[0]<525 and mousepos[1]>262.5 and mousepos[1]<337.5:
          return "B", time_w, time_b
        elif mousepos[0]>525 and mousepos[0]<600 and mousepos[1]>262.5 and mousepos[1]<337.5:
          return "N", time_w, time_b

    screen.fill((112, 102, 119))
    if side:
      screen.blit(piece_q, (300, 262.5))
      screen.blit(piece_r, (375, 262.5))
      screen.blit(piece_b, (450, 262.5))
      screen.blit(piece_n, (525, 262.5))
    else:
      screen.blit(piece_Q, (300, 262.5))
      screen.blit(piece_R, (375, 262.5))
      screen.blit(piece_B, (450, 262.5))
      screen.blit(piece_N, (525, 262.5))

    pygame.display.flip()
    clock.tick(60)
def game(turn = False, time_control = (-1, -1)):
  gameboard = board.Board(turn = turn)
  #eval = evaluation.eval(gameboard)
  font = pygame.font.Font('freesansbold.ttf', 32)
  running = True
  selected = None
  squares = []
  time_w = time_b = time_control[0]
  pygame.time.set_timer(0, 1000)
  while running:
    screen.fill((250, 247, 246))
    """if gameboard.all_valid_moves(False) == []:
      if gameboard.king_safe(gameboard.find_king(False), False):
        print("Stalemate")
      else:
        print("Black Wins!")
    elif gameboard.all_valid_moves(True) == []:
      if gameboard.king_safe(gameboard.find_king(True), True):
        print("Stalemate")
      else:
        print("White Wins!")"""
    for event in pygame.event.get():
          if event.type == pygame.QUIT:
              running = False
          elif event.type == 0 and time_control != (-1, -1):
            if gameboard.turn:
              time_b -= 1
              print(datetime.timedelta(seconds = time_b))
            else:
              time_w -= 1
              print(datetime.timedelta(seconds = time_w))
          elif event.type == pygame.MOUSEBUTTONDOWN:
            mousepos = pygame.mouse.get_pos()
            mousesquare = (mousepos[1]//75, mousepos[0]//75)
            if mousesquare[0] >= 0 and mousesquare[0] <=7 and mousesquare[1] >= 0 and mousesquare[1] <=7:
              if gameboard.board[mousesquare[0]][mousesquare[1]] == None:
                if selected != None:
                  if squares.count(mousesquare)==1:
                    if gameboard.board[selected[0]][selected[1]].type == "P" and (mousesquare[0] == 0 or mousesquare[0] == 7):
                      promo, time_w, time_b = promote(gameboard.turn, time_control, time_w, time_b)
                      if promo == None:
                        running = False
                      if time_control!=(-1, -1):
                        if gameboard.turn:
                          time_b += time_control[1]
                        else:
                          time_w += time_control[1]
                      gameboard.move(selected, mousesquare, promo=promo)
                    else:
                      if time_control!=(-1, -1):
                        if gameboard.turn:
                          time_b += time_control[1]
                        else:
                          time_w += time_control[1]
                      gameboard.move(selected, mousesquare)
                    selected = None
              else:
                if gameboard.board[mousesquare[0]][mousesquare[1]].color == gameboard.turn:
                  if mousesquare == selected:
                    selected = None
                  else:
                    selected = mousesquare
                else:
                  if selected!=None:
                    if squares.count(mousesquare) == 1:
                      if gameboard.board[selected[0]][selected[1]].type == "P" and (
                              mousesquare[0] == 0 or mousesquare[0] == 7):
                        promo, time_w, time_b = promote(gameboard.turn, time_control, time_w, time_b)
                        if promo == None:
                          running = False
                        if time_control!=(-1, -1):
                          if gameboard.turn:
                            time_b += time_control[1]
                          else:
                            time_w += time_control[1]
                        gameboard.move(selected, mousesquare, promo=promo)
                      else:
                        if time_control!=(-1, -1):
                          if gameboard.turn:
                            time_b += time_control[1]
                          else:
                            time_w += time_control[1]
                        gameboard.move(selected, mousesquare)
                      selected = None
            else:
              gameboard.unmove()

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
              #check = not gameboard.king_safe(gameboard.find_king(True), True)
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
              #check = not gameboard.king_safe(gameboard.find_king(False), False)
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

    #draw sidebar
    if not time_control == (-1, -1):
      white_clock = font.render(str(datetime.timedelta(seconds=time_w)), False, (0, 0, 0), (200, 200, 200))
      black_clock = font.render(str(datetime.timedelta(seconds=time_b)), False, (0, 0, 0), (200, 200, 200))
      white_clock_rect = white_clock.get_rect()
      black_clock_rect = black_clock.get_rect()
      white_clock_rect.center = (700, 500)
      black_clock_rect.center = (700, 100)
      screen.blit(white_clock, white_clock_rect)
      screen.blit(black_clock, black_clock_rect)
    else:
      white_clock = font.render("NO CLOCK", True, (0, 0, 0), (200, 200, 200))
      black_clock = font.render("NO CLOCK", True, (0, 0, 0), (200, 200, 200))
      white_clock_rect = white_clock.get_rect()
      black_clock_rect = black_clock.get_rect()
      white_clock_rect.center = (700, 500)
      black_clock_rect.center = (700, 100)
      screen.blit(white_clock, white_clock_rect)
      screen.blit(black_clock, black_clock_rect)
    #analysis = font.render(str(round(eval.check_position(), 3)), True, (0,0,0), (200, 200, 200))
    #analysis_rect = analysis.get_rect()
    #analysis_rect.center = (700, 300)
    #screen.blit(analysis, analysis_rect)

    pygame.display.flip()
    clock.tick(60)

if __name__ == "__main__":
  game()