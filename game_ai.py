import board
import pygame
import evaluation
import threading

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


def main(turn=False):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    game(screen, clock, turn)


def promote(side, screen, clock):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                if (
                    mousepos[0] > 300
                    and mousepos[0] < 375
                    and mousepos[1] > 262.5
                    and mousepos[1] < 337.5
                ):
                    return "Q"
                elif (
                    mousepos[0] > 375
                    and mousepos[0] < 450
                    and mousepos[1] > 262.5
                    and mousepos[1] < 337.5
                ):
                    return "R"
                elif (
                    mousepos[0] > 450
                    and mousepos[0] < 525
                    and mousepos[1] > 262.5
                    and mousepos[1] < 337.5
                ):
                    return "B"
                elif (
                    mousepos[0] > 525
                    and mousepos[0] < 600
                    and mousepos[1] > 262.5
                    and mousepos[1] < 337.5
                ):
                    return "N"

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


def game(
    screen,
    clock,
    turn=False,
    position="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",
):
    gameboard = board.Board(turn=turn, position=position)
    eval = evaluation.eval(gameboard)
    running = True
    font = pygame.font.Font("freesansbold.ttf", 32)
    selected = None
    squares = []
    game_over = False
    status = "White To Play!"
    pygame.time.set_timer(0, 1000)
    while running:
        screen.fill((250, 247, 246))
        if game_over and selected != None:
            squares = []
        if gameboard.render and not game_over:
            if gameboard.all_valid_moves(False) == []:
                if gameboard.king_safe(gameboard.find_king(False), False):
                    game_over = True
                    status = "Stalemate!"
                else:
                    game_over = True
                    status = "AI Wins!"
            elif gameboard.all_valid_moves(True) == []:
                if gameboard.king_safe(gameboard.find_king(True), True):
                    game_over = True
                    status = "Stalemate!"
                else:
                    game_over = True
                    status = "Human Wins!"
            elif gameboard.board_history.count(gameboard.board) == 3:
                game_over = True
                status = "Threefold!"
            elif gameboard.fifty_move():
                game_over = True
                status = "Fifty Move!"
            elif not gameboard.turn:
                status = "White To Play!"
            if selected != None:
                squares = gameboard.valid_moves(selected)
            else:
                squares = []
            if gameboard.turn and not game_over:
                status = "AI Is Thinking..."
                draw_everything(
                    screen,
                    gameboard,
                    font,
                    squares,
                    status,
                )
                pygame.display.flip()
                play_ai_move(gameboard, eval)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                and gameboard.render
                and not game_over
            ):
                mousepos = pygame.mouse.get_pos()
                mousesquare = (mousepos[1] // 75, mousepos[0] // 75)
                if (
                    mousesquare[0] >= 0
                    and mousesquare[0] <= 7
                    and mousesquare[1] >= 0
                    and mousesquare[1] <= 7
                ):
                    if gameboard.board[mousesquare[0]][mousesquare[1]] == None:
                        if selected != None:
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
                                    if promo == None:
                                        running = False
                                    gameboard.move(selected, mousesquare, promo=promo)
                                    selected, squares = None, []
                                else:
                                    gameboard.move(selected, mousesquare)
                                    selected, squares = None, []
                    else:
                        if (
                            gameboard.board[mousesquare[0]][mousesquare[1]].color
                            == False
                            and gameboard.turn == False
                        ):
                            if mousesquare == selected:
                                selected = None
                            else:
                                selected = mousesquare
                        else:
                            if selected != None:
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
                                        if promo == None:
                                            running = False
                                        gameboard.move(
                                            selected, mousesquare, promo=promo
                                        )
                                        selected, squares = None, []
                                    else:
                                        gameboard.move(selected, mousesquare)
                                        selected, squares = None, []

                else:
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

        if gameboard.render:
            draw_everything(screen, gameboard, font, squares, status)
            pygame.display.update()
        clock.tick(60)


def play_ai_move(gameboard, eval):
    if gameboard.turn:
        if gameboard.num_pieces() > 12:
            threading.Thread(target=eval.play_best_move, args=[2]).start()
        elif gameboard.num_pieces() > 8:
            threading.Thread(target=eval.play_best_move, args=[3]).start()
        elif gameboard.num_pieces() > 4:
            threading.Thread(target=eval.play_best_move, args=[4]).start()
        else:
            threading.Thread(target=eval.play_best_move, args=[5]).start()


def draw_pieces(gameboard, screen):
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
                    pygame.draw.rect(
                        screen, (255, 0, 0), (75 * file, 75 * rank, 75, 75)
                    )
                screen.blit(piece, (75 * file, 75 * rank))


def draw_board(screen):
    for i in range(8):
        for j in range(8):
            if i % 2 == 0 and j % 2 == 0:
                color = (204, 183, 174)
            elif i % 2 == 0 and j % 2 != 0:
                color = (112, 102, 119)
            elif i % 2 != 0 and j % 2 == 0:
                color = (112, 102, 119)
            else:
                color = (204, 183, 174)
            pygame.draw.rect(screen, color, (75 * i, 75 * j, 75, 75))


def draw_valid_moves(gameboard, screen, squares):
    for square in squares:
        if gameboard.board[square[0]][square[1]] == None:
            pygame.draw.rect(
                screen,
                (0, 255, 0),
                (square[1] * 75 + 25, square[0] * 75 + 25, 25, 25),
            )
        else:
            pygame.draw.rect(
                screen,
                (0, 255, 0),
                (square[1] * 75, square[0] * 75, 75, 75),
                width=5,
            )


def draw_previous_move(gameboard, screen):
    if len(gameboard.history) > 0:
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


def draw_status(screen, status):
    font = pygame.font.Font("freesansbold.ttf", 25)
    message_box = font.render(status, True, (0, 0, 0))
    message_rect = message_box.get_rect()
    message_rect.center = (700, 250)
    screen.blit(message_box, message_rect)


def draw_buttons(screen):
    font = pygame.font.Font("freesansbold.ttf", 22)
    pygame.draw.rect(screen, (0, 0, 0), (620, 350, 160, 30), width=3)
    pygame.draw.rect(screen, (0, 0, 0), (620, 400, 160, 30), width=3)
    takeback = font.render("Takeback", True, (0, 0, 0))
    resign = font.render("Resign", True, (0, 0, 0))
    takeback_rect = takeback.get_rect()
    resign_rect = resign.get_rect()
    takeback_rect.center = (700, 365)
    resign_rect.center = (700, 415)
    screen.blit(takeback, takeback_rect)
    screen.blit(resign, resign_rect)


def draw_everything(screen, gameboard, font, squares, status):
    draw_board(screen)
    draw_previous_move(gameboard, screen)
    draw_valid_moves(gameboard, screen, squares)
    draw_pieces(gameboard, screen)
    draw_status(screen, status)
    draw_buttons(screen)


main()
