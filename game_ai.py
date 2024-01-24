# import the libraries
import board
import pygame
import evaluation
import threading

# load all of the piece images
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


# main function, initiates the pygame window and starts the game
def main(turn=False):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    game(screen, clock, turn)


# promotion screen, ran by game function, takes the side of the player promoting(False: white True: black), takes the screen to draw on and clock
def promote(side, screen, clock):
    # promotion loop, ends on return value
    while True:
        # cycle through events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # returns none when the window close button is pressed, this is interpreted by the game function which then halts the program
                return None
            # runs on mouse press
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # gets where the mouse clicked
                mousepos = pygame.mouse.get_pos()
                # returns Q if the mouse is over the queen button
                if (
                    mousepos[0] > 300
                    and mousepos[0] < 375
                    and mousepos[1] > 262.5
                    and mousepos[1] < 337.5
                ):
                    return "Q"
                # return R if the mouse is over the rook button
                elif (
                    mousepos[0] > 375
                    and mousepos[0] < 450
                    and mousepos[1] > 262.5
                    and mousepos[1] < 337.5
                ):
                    return "R"
                # returns B if the mouse is over the bishop button
                elif (
                    mousepos[0] > 450
                    and mousepos[0] < 525
                    and mousepos[1] > 262.5
                    and mousepos[1] < 337.5
                ):
                    return "B"
                # return N if the mouse is over the knight button
                elif (
                    mousepos[0] > 525
                    and mousepos[0] < 600
                    and mousepos[1] > 262.5
                    and mousepos[1] < 337.5
                ):
                    return "N"

        # fill background
        screen.fill((112, 102, 119))
        # places black pieces if it is the correct side
        if side:
            screen.blit(piece_q, (300, 262.5))
            screen.blit(piece_r, (375, 262.5))
            screen.blit(piece_b, (450, 262.5))
            screen.blit(piece_n, (525, 262.5))
        # places white pieces if it is the correct side
        else:
            screen.blit(piece_Q, (300, 262.5))
            screen.blit(piece_R, (375, 262.5))
            screen.blit(piece_B, (450, 262.5))
            screen.blit(piece_N, (525, 262.5))

        # display the frame
        pygame.display.flip()
        # set fps cap to 60
        clock.tick(60)


# game function, takes screen, clock, turn and position as arguments. ran by the main function
def game(
    screen,
    clock,
    turn=False,
    position="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",
):
    # make a board object
    gameboard = board.Board(turn=turn, position=position)
    # make evaluation object
    eval = evaluation.eval(gameboard)
    # set running to true
    running = True
    # set the selected square to None and set the valid squares to empty
    selected = None
    squares = []
    # set game_over to False and status to white to play
    game_over = False
    status = "White To Play!"
    # runs while the program is running
    while running:
        # fills the background
        screen.fill((250, 247, 246))
        # unsets valid squares when the game ends
        if game_over and selected != None:
            squares = []

        # checking for wins or draws
        if gameboard.render and not game_over:
            # runs if white has no valid moves to make
            if gameboard.all_valid_moves(False) == []:
                # runs if white king is safe - stalemate
                if gameboard.king_safe(gameboard.find_king(False), False):
                    game_over = True
                    status = "Stalemate!"
                # runs if white king is not safe - blacks win
                else:
                    game_over = True
                    status = "AI Wins!"
            # runs if black has no more moves
            elif gameboard.all_valid_moves(True) == []:
                # runs if black king is not in check - stalemate
                if gameboard.king_safe(gameboard.find_king(True), True):
                    game_over = True
                    status = "Stalemate!"
                # runs if black king is in check - white wins
                else:
                    game_over = True
                    status = "Human Wins!"
            # runs on threefold
            elif gameboard.board_history.count(gameboard.board) == 3:
                game_over = True
                status = "Threefold!"
            # runs if the board is a 50 move draw
            elif gameboard.fifty_move():
                game_over = True
                status = "Fifty Move!"
            elif gameboard.insufficient_material():
                game_over = True
                status = "Insufficient\nMaterial!"
            # runs if its whites turn
            elif not gameboard.turn:
                status = "White To Play!"
            # runs if something is selected - gets all the valid moves
            if selected != None:
                squares = gameboard.valid_moves(selected)
            # if nothing is selected, remove all valid move squares
            else:
                squares = []
            # runs if its the ai has to move and has not moved yet
            if gameboard.turn and not game_over:
                status = "AI Is Thinking..."
                # renders the frame as nothing will render while the ai is thinking as the ai is trying many positions and we dont want to render them
                draw_everything(
                    screen,
                    gameboard,
                    squares,
                    status,
                )
                pygame.display.flip()
                # play the ove
                play_ai_move(gameboard, eval)
        # event loop
        for event in pygame.event.get():
            # runs if quit button is pressed
            if event.type == pygame.QUIT:
                running = False
            # runs on mouse press
            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                and gameboard.render
                and not game_over
            ):
                # get mouse position
                mousepos = pygame.mouse.get_pos()
                # get the square the mouse is on
                mousesquare = (mousepos[1] // 75, mousepos[0] // 75)
                # runs if its the mouse is on the board
                if (
                    mousesquare[0] >= 0
                    and mousesquare[0] <= 7
                    and mousesquare[1] >= 0
                    and mousesquare[1] <= 7
                ):
                    # runs if the clicked square has no pieces on it
                    if gameboard.board[mousesquare[0]][mousesquare[1]] == None:
                        # runs if piece is selected already
                        if selected != None:
                            # runs if the square clicked is a legal move square
                            if squares.count(mousesquare) == 1:
                                # runs for promotion
                                if gameboard.board[selected[0]][
                                    selected[1]
                                ].type == "P" and (
                                    mousesquare[0] == 0 or mousesquare[0] == 7
                                ):
                                    promo = promote(
                                        gameboard.turn,
                                        screen,
                                        clock,
                                    )
                                    # runs if the promo returns None which means the program needs to exit
                                    if promo == None:
                                        running = False
                                    # play the move and unselect the squares and select
                                    gameboard.move(selected, mousesquare, promo=promo)
                                    selected, squares = None, []
                                else:
                                    # play the move and unselect the squares and select
                                    gameboard.move(selected, mousesquare)
                                    selected, squares = None, []
                    # runs if the mouse is pressed on a square that has a piece
                    else:
                        # runs if the piece that is clicked is white and its whites turn
                        if (
                            gameboard.board[mousesquare[0]][mousesquare[1]].color
                            == False
                            and gameboard.turn == False
                        ):
                            # unselects piece if its the same one thats already selected
                            if mousesquare == selected:
                                selected = None
                            # selects the pressed piece otherwise
                            else:
                                selected = mousesquare
                        # runs if a black piece is pressed
                        else:
                            # runs if a piece is already selected for moving - captures
                            if selected != None:
                                # capture with promotion
                                if squares.count(mousesquare) == 1:
                                    if gameboard.board[selected[0]][
                                        selected[1]
                                    ].type == "P" and (
                                        mousesquare[0] == 0 or mousesquare[0] == 7
                                    ):
                                        promo = promote(
                                            gameboard.turn,
                                            screen,
                                            clock,
                                        )
                                        # exits if promo returns None
                                        if promo == None:
                                            running = False
                                        # plays move
                                        gameboard.move(
                                            selected, mousesquare, promo=promo
                                        )
                                        selected, squares = None, []
                                    else:
                                        # non-promo capture
                                        gameboard.move(selected, mousesquare)
                                        selected, squares = None, []
                # runs if board is not pressed
                else:
                    # takeback button
                    if (
                        mousepos[0] >= 620
                        and mousepos[1] >= 350
                        and mousepos[0] <= 780
                        and mousepos[1] <= 380
                        and not game_over
                    ):
                        gameboard.unmove()
                        gameboard.unmove()
                        selected = None
                    # resign button
                    elif (
                        mousepos[0] >= 620
                        and mousepos[1] >= 400
                        and mousepos[0] <= 780
                        and mousepos[1] <= 430
                        and not game_over
                    ):
                        if not gameboard.turn:
                            game_over = True
                            status = "AI Wins!"
        # draw screen
        if gameboard.render:
            draw_everything(screen, gameboard, squares, status)
            pygame.display.update()
        # restrict fps to 60
        clock.tick(60)


# playy ai move
def play_ai_move(gameboard, eval):
    # if its black - ai turn, run
    if gameboard.turn:
        # runs at depth of 2 if lot of pieces left
        if gameboard.num_pieces() > 12:
            threading.Thread(target=eval.play_best_move, args=[2]).start()
        # runs at depth of 3 if some pieces left
        elif gameboard.num_pieces() > 8:
            threading.Thread(target=eval.play_best_move, args=[3]).start()
        # runs at depth of 4 if few pieces left
        elif gameboard.num_pieces() > 4:
            threading.Thread(target=eval.play_best_move, args=[4]).start()
        # runs at depth of 5 if if barely any pieces left
        else:
            threading.Thread(target=eval.play_best_move, args=[5]).start()


# draw pieces function
def draw_pieces(gameboard, screen):
    # runs for each square
    for rank in range(8):
        for file in range(8):
            # set check highlighter to false
            check = False
            # runs if a piece is on the square - sets the piece texture
            if gameboard.board[rank][file] != None:
                if gameboard.board[rank][file].color:
                    if gameboard.board[rank][file].type == "B":
                        piece = piece_b
                    elif gameboard.board[rank][file].type == "K":
                        piece = piece_k
                        # sets check highlighter
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
                        # sets check highlighter
                        check = not gameboard.king_safe(
                            gameboard.find_king(False), False
                        )
                    elif gameboard.board[rank][file].type == "N":
                        piece = piece_N
                    elif gameboard.board[rank][file].type == "P":
                        piece = piece_P
                    elif gameboard.board[rank][file].type == "Q":
                        piece = piece_Q
                    elif gameboard.board[rank][file].type == "R":
                        piece = piece_R
                if check:
                    # draw check highlighter on square
                    pygame.draw.rect(
                        screen, (255, 0, 0), (75 * file, 75 * rank, 75, 75)
                    )
                # place piece
                screen.blit(piece, (75 * file, 75 * rank))


# draw the board
def draw_board(screen):
    # runs for each square
    for i in range(8):
        for j in range(8):
            # white squares
            if i % 2 == 0 and j % 2 == 0:
                color = (204, 183, 174)
            # black squares
            elif i % 2 == 0 and j % 2 != 0:
                color = (112, 102, 119)
            # black squares
            elif i % 2 != 0 and j % 2 == 0:
                color = (112, 102, 119)
            # white squares
            else:
                color = (204, 183, 174)
            # draws the square on screen
            pygame.draw.rect(screen, color, (75 * i, 75 * j, 75, 75))


# draws each valid move highlighter
def draw_valid_moves(gameboard, screen, squares):
    # runs for each valid move swuare
    for square in squares:
        # runs if the square is empty - small square in center
        if gameboard.board[square[0]][square[1]] == None:
            pygame.draw.rect(
                screen,
                (0, 255, 0),
                (square[1] * 75 + 25, square[0] * 75 + 25, 25, 25),
            )
        # runs if square is a capture square - highlight around box
        else:
            pygame.draw.rect(
                screen,
                (0, 255, 0),
                (square[1] * 75, square[0] * 75, 75, 75),
                width=5,
            )


# draw the previous move highlighter
def draw_previous_move(gameboard, screen):
    # runs if a previous move exists
    if len(gameboard.history) > 0:
        # draw a purple rectangle at the square of the starting positon of the previous move
        pygame.draw.rect(
            screen,
            (255, 0, 255),
            (
                gameboard.history[len(gameboard.history) - 1][0][1] * 75,
                gameboard.history[len(gameboard.history) - 1][0][0] * 75,
                75,
                75,
            ),
        )
        # draw a purple rectangle at the ending square of the previous move
        pygame.draw.rect(
            screen,
            (255, 0, 255),
            (
                gameboard.history[len(gameboard.history) - 1][1][1] * 75,
                gameboard.history[len(gameboard.history) - 1][1][0] * 75,
                75,
                75,
            ),
        )


# draw the game status
def draw_status(screen, status):
    # define font
    font = pygame.font.Font("freesansbold.ttf", 25)
    # render, center and place message
    message_box = font.render(status, True, (0, 0, 0))
    message_rect = message_box.get_rect()
    message_rect.center = (700, 250)
    screen.blit(message_box, message_rect)


# draw the buttons
def draw_buttons(screen):
    # set the font
    font = pygame.font.Font("freesansbold.ttf", 22)
    # draw the buttons
    pygame.draw.rect(screen, (0, 0, 0), (620, 350, 160, 30), width=3)
    pygame.draw.rect(screen, (0, 0, 0), (620, 400, 160, 30), width=3)
    # place the text inside the buttons
    takeback = font.render("Takeback", True, (0, 0, 0))
    resign = font.render("Resign", True, (0, 0, 0))
    takeback_rect = takeback.get_rect()
    resign_rect = resign.get_rect()
    takeback_rect.center = (700, 365)
    resign_rect.center = (700, 415)
    screen.blit(takeback, takeback_rect)
    screen.blit(resign, resign_rect)


# run all of the draw functions
def draw_everything(screen, gameboard, squares, status):
    draw_board(screen)
    draw_previous_move(gameboard, screen)
    draw_valid_moves(gameboard, screen, squares)
    draw_pieces(gameboard, screen)
    draw_status(screen, status)
    draw_buttons(screen)
