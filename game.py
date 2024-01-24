# import the required libraries
import board
import pygame
import datetime
import threading
from copy import deepcopy

# load the piece textures
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


# main function - ran by the gui
def main(turn=False, time_control=(-1, -1)):
    # initialize pygame, screen and clock. Then start game function
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    game(screen, clock, turn, time_control)


# promote function
def promote(side, time_control, time_w, time_b, screen, clock):
    while True:
        # event loop
        for event in pygame.event.get():
            # quit on exit, None is interpreted by game function to quit
            if event.type == pygame.QUIT:
                return None, time_w, time_b
            # take time away from the side who is playing as deciding promotion counts to the clock
            elif event.type == 0 and time_control != (-1, -1):
                if side:
                    time_b -= 1
                else:
                    time_w -= 1
            # mouse press, detect which button was pressed(queen, rook, knight bishop and return result)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                if (
                    mousepos[0] > 300
                    and mousepos[0] < 375
                    and mousepos[1] > 262.5
                    and mousepos[1] < 337.5
                ):
                    return "Q", time_w, time_b
                elif (
                    mousepos[0] > 375
                    and mousepos[0] < 450
                    and mousepos[1] > 262.5
                    and mousepos[1] < 337.5
                ):
                    return "R", time_w, time_b
                elif (
                    mousepos[0] > 450
                    and mousepos[0] < 525
                    and mousepos[1] > 262.5
                    and mousepos[1] < 337.5
                ):
                    return "B", time_w, time_b
                elif (
                    mousepos[0] > 525
                    and mousepos[0] < 600
                    and mousepos[1] > 262.5
                    and mousepos[1] < 337.5
                ):
                    return "N", time_w, time_b
        # fill the background
        screen.fill((112, 102, 119))
        # draw black pieces
        if side:
            screen.blit(piece_q, (300, 262.5))
            screen.blit(piece_r, (375, 262.5))
            screen.blit(piece_b, (450, 262.5))
            screen.blit(piece_n, (525, 262.5))
        # draw white pieces
        else:
            screen.blit(piece_Q, (300, 262.5))
            screen.blit(piece_R, (375, 262.5))
            screen.blit(piece_B, (450, 262.5))
            screen.blit(piece_N, (525, 262.5))
        # show results and cap fps at 60
        pygame.display.flip()
        clock.tick(60)


# game function
def game(
    screen,
    clock,
    turn=False,
    time_control=(-1, -1),
    position="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",
):
    # initialize board, font
    gameboard = board.Board(turn=turn, position=position)
    running = True
    font = pygame.font.Font("freesansbold.ttf", 32)
    # set selected squares, valid move squares and the squares to render(flipped for black) to empty
    selected = None
    squares = []
    squares_render = []
    game_over = False
    # status is white to play and set the clock for white and black
    status = "White To Play!"
    time_w = time_b = time_control[0]
    # set timer for clock at 1 second
    pygame.time.set_timer(0, 1000)
    # running loop
    while running:
        # fill background
        screen.fill((250, 247, 246))
        # unselect selected square once game is over in order to remove green highlighting after game
        if game_over and selected != None:
            selected = None
        # check if the game is over if its not over
        if not game_over:
            # check for stalemate and checkmate on whites side
            if gameboard.all_valid_moves(False) == []:
                if gameboard.king_safe(gameboard.find_king(False), False):
                    game_over = True
                    status = "Stalemate!"
                else:
                    game_over = True
                    status = "Black Wins!"
            # check for stalemate and checkmate on blacks side
            elif gameboard.all_valid_moves(True) == []:
                if gameboard.king_safe(gameboard.find_king(True), True):
                    game_over = True
                    status = "Stalemate!"
                else:
                    game_over = True
                    status = "White Wins!"
            # check for threefold
            elif gameboard.board_history.count(gameboard.board) == 3:
                game_over = True
                status = "Threefold!"
            # check for fifty move draw
            elif gameboard.fifty_move():
                game_over = True
                status = "Fifty Move!"
            # check for insufficient material draw
            elif gameboard.insufficient_material():
                game_over = True
                status = "Insufficient\nMaterial!"
            # check if white or black ran out of time
            elif time_w == 0:
                game_over = True
                status = "Black Wins!"
            elif time_b == 0:
                game_over = True
                status = "White Wins!"
            # if no one one or lost set status to reflect the current turn
            elif not gameboard.turn:
                status = "White To Play!"
            else:
                status = "Black To Play!"
        # if a square is currently selected to move
        if selected != None:
            # set the valid moves
            squares = gameboard.valid_moves(selected)
            # if its blacks turn set the squares to render to the flip of what they actually are
            if gameboard.turn:
                squares_render = squares.copy()
                for square in range(len(squares_render)):
                    squares_render[square] = flip_square(squares_render[square], True)
            else:
                squares_render = squares
        else:
            # if no piece is selected clear the squares and sqaures for rendering
            squares = []
            squares_render = []
        # event loop
        for event in pygame.event.get():
            # quit on quit
            if event.type == pygame.QUIT:
                running = False
            # subtract from time
            elif event.type == 0 and time_control != (-1, -1) and not game_over:
                if gameboard.turn:
                    time_b -= 1
                else:
                    time_w -= 1
            # mouse press
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                # get position
                mousepos = pygame.mouse.get_pos()
                # set the mouse square to the opposite of what it is if its blacks turn
                mousesquare = flip_square(
                    (mousepos[1] // 75, mousepos[0] // 75), gameboard.turn
                )
                # if the mouse was clicked inside of the board
                if (
                    mousesquare[0] >= 0
                    and mousesquare[0] <= 7
                    and mousesquare[1] >= 0
                    and mousesquare[1] <= 7
                ):
                    # if there is nothing on the selected square
                    if gameboard.board[mousesquare[0]][mousesquare[1]] == None:
                        # if some piece has previously been selected to move
                        if selected != None:
                            # is the move valid?
                            if squares.count(mousesquare) == 1:
                                # promotion
                                if gameboard.board[selected[0]][
                                    selected[1]
                                ].type == "P" and (
                                    mousesquare[0] == 0 or mousesquare[0] == 7
                                ):
                                    promo, time_w, time_b = promote(
                                        gameboard.turn,
                                        time_control,
                                        time_w,
                                        time_b,
                                        screen,
                                        clock,
                                    )
                                    # exit on None as that indicates an exit from the promote function
                                    if promo == None:
                                        running = False
                                    # add the increment to the side that just played
                                    if time_control != (-1, -1):
                                        if gameboard.turn:
                                            time_b += time_control[1]
                                        else:
                                            time_w += time_control[1]
                                    # make move
                                    gameboard.move(selected, mousesquare, promo=promo)
                                    # unselect squares
                                    selected, squares, squares_render = None, [], []
                                # not promotion
                                else:
                                    # add increment and move
                                    if time_control != (-1, -1):
                                        if gameboard.turn:
                                            time_b += time_control[1]
                                        else:
                                            time_w += time_control[1]
                                    gameboard.move(selected, mousesquare)
                                    # unselect squares
                                    selected, squares, squares_render = None, [], []
                            selected = None
                    # captures or selecting a piece
                    else:
                        # if selecting or unselecting a piece
                        if (
                            gameboard.board[mousesquare[0]][mousesquare[1]].color
                            == gameboard.turn
                        ):
                            # if the selected piece is pressed, unset it
                            if mousesquare == selected:
                                selected = None
                            # if another piece is selected, select it instead
                            else:
                                selected = mousesquare
                        # if capture
                        else:
                            if selected != None:
                                # is it valid?
                                if squares.count(mousesquare) == 1:
                                    # promotion
                                    if gameboard.board[selected[0]][
                                        selected[1]
                                    ].type == "P" and (
                                        mousesquare[0] == 0 or mousesquare[0] == 7
                                    ):
                                        promo, time_w, time_b = promote(
                                            gameboard.turn,
                                            time_control,
                                            time_w,
                                            time_b,
                                            screen,
                                            clock,
                                        )
                                        # exit on none as thats how promo function transfers exit
                                        if promo == None:
                                            running = False
                                        # add increment
                                        if time_control != (-1, -1):
                                            if gameboard.turn:
                                                time_b += time_control[1]
                                            else:
                                                time_w += time_control[1]
                                        # move
                                        gameboard.move(
                                            selected, mousesquare, promo=promo
                                        )
                                        # unselect all
                                        selected, squares, squares_render = None, [], []
                                    # normal capture
                                    else:
                                        # add increment
                                        if time_control != (-1, -1):
                                            if gameboard.turn:
                                                time_b += time_control[1]
                                            else:
                                                time_w += time_control[1]
                                        # move and unselect all
                                        gameboard.move(selected, mousesquare)
                                        selected, squares, squares_render = None, [], []
                                selected = None
                # mouse not pressed on board
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
                            status = "Black Wins!"
                        else:
                            game_over = True
                            status = "White Wins!"
        # draw frame
        draw_everything(
            screen,
            gameboard,
            time_control,
            time_b,
            time_w,
            font,
            squares_render,
            status,
        )
        # display frame and cap fps at 60
        pygame.display.update()
        clock.tick(60)


# draw the pieces on the board
def draw_pieces(gameboard, screen):
    # flip the board if its blacks turn
    board_flip = flip_board(gameboard.board, gameboard.turn)
    # go through board drawing pieces
    for rank in range(8):
        for file in range(8):
            check = False
            if board_flip[rank][file] != None:
                if board_flip[rank][file].color:
                    if board_flip[rank][file].type == "B":
                        piece = piece_b
                    elif board_flip[rank][file].type == "K":
                        piece = piece_k
                        # check highlighter
                        check = not gameboard.king_safe(gameboard.find_king(True), True)
                    elif board_flip[rank][file].type == "N":
                        piece = piece_n
                    elif board_flip[rank][file].type == "P":
                        piece = piece_p
                    elif board_flip[rank][file].type == "Q":
                        piece = piece_q
                    elif board_flip[rank][file].type == "R":
                        piece = piece_r
                else:
                    if board_flip[rank][file].type == "B":
                        piece = piece_B
                    elif board_flip[rank][file].type == "K":
                        piece = piece_K
                        # check highlighter
                        check = not gameboard.king_safe(
                            gameboard.find_king(False), False
                        )
                    elif board_flip[rank][file].type == "N":
                        piece = piece_N
                    elif board_flip[rank][file].type == "P":
                        piece = piece_P
                    elif board_flip[rank][file].type == "Q":
                        piece = piece_Q
                    elif board_flip[rank][file].type == "R":
                        piece = piece_R
                # draw check highlighter
                if check:
                    pygame.draw.rect(
                        screen, (255, 0, 0), (75 * file, 75 * rank, 75, 75)
                    )
                # place piece
                screen.blit(piece, (75 * file, 75 * rank))


# flip a square
def flip_square(square: tuple, flip: bool):
    # flip it if the flip is True otherwise just return the square
    if flip:
        return (7 - square[0], 7 - square[1])
    else:
        return square


# flip the board
def flip_board(Board: list, flip: bool):
    # return flipped board if flip is True otherwise just return the normal board
    if flip:
        Board = deepcopy(Board)
        Board.reverse()
        for rank in Board:
            rank.reverse()
        return Board
    else:
        return Board


# draw the board squares
def draw_board(screen):
    for i in range(8):
        for j in range(8):
            if i % 2 == 0 and j % 2 == 0:
                # white squares
                color = (204, 183, 174)
            elif i % 2 == 0 and j % 2 != 0:
                # black squares
                color = (112, 102, 119)
            elif i % 2 != 0 and j % 2 == 0:
                # black squares
                color = (112, 102, 119)
            else:
                # white squares
                color = (204, 183, 174)
            # draw square
            pygame.draw.rect(screen, color, (75 * i, 75 * j, 75, 75))


# draw the valid move highlighters
def draw_valid_moves(gameboard, screen, squares):
    for square in squares:
        Board = flip_board(gameboard.board, gameboard.turn)
        if Board[square[0]][square[1]] == None:
            # dotted indicator for non captures
            pygame.draw.rect(
                screen,
                (0, 255, 0),
                (square[1] * 75 + 25, square[0] * 75 + 25, 25, 25),
            )
        else:
            # outline for captures
            pygame.draw.rect(
                screen,
                (0, 255, 0),
                (square[1] * 75, square[0] * 75, 75, 75),
                width=5,
            )


# draw the sidebar
def draw_sidebar(screen, time_control, time_b, time_w, font, turn):
    # flip the timers if its blacks turn
    if turn:
        placeholder = time_w
        time_w = time_b
        time_b = placeholder
    # if there is a time control, render the times
    if not time_control == (-1, -1):
        white_clock = font.render(
            str(datetime.timedelta(seconds=time_w)),
            False,
            (0, 0, 0),
        )
        black_clock = font.render(
            str(datetime.timedelta(seconds=time_b)),
            False,
            (0, 0, 0),
        )
        white_clock_rect = white_clock.get_rect()
        black_clock_rect = black_clock.get_rect()
        white_clock_rect.center = (700, 500)
        black_clock_rect.center = (700, 100)
        screen.blit(white_clock, white_clock_rect)
        screen.blit(black_clock, black_clock_rect)


# draw the previous move highlighter
def draw_previous_move(gameboard, screen):
    # only if there is a previous move, draw purple indicators on the start and end squares of the previous move
    if len(gameboard.history) > 0:
        prev_move_start = flip_square(
            gameboard.history[len(gameboard.history) - 1][0], gameboard.turn
        )
        prev_move_end = flip_square(
            gameboard.history[len(gameboard.history) - 1][1], gameboard.turn
        )
        pygame.draw.rect(
            screen,
            (255, 0, 255),
            (
                prev_move_start[1] * 75,
                prev_move_start[0] * 75,
                75,
                75,
            ),
        )
        pygame.draw.rect(
            screen,
            (255, 0, 255),
            (
                prev_move_end[1] * 75,
                prev_move_end[0] * 75,
                75,
                75,
            ),
        )


# draw the game status
def draw_status(screen, status):
    font = pygame.font.Font("freesansbold.ttf", 25)
    message_box = font.render(status, True, (0, 0, 0))
    message_rect = message_box.get_rect()
    message_rect.center = (700, 250)
    screen.blit(message_box, message_rect)


# draw the resign and takeback buttons
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


# call all draw functions
def draw_everything(
    screen, gameboard, time_control, time_b, time_w, font, squares, status
):
    draw_board(screen)
    draw_previous_move(gameboard, screen)
    draw_valid_moves(gameboard, screen, squares)
    draw_pieces(gameboard, screen)
    draw_sidebar(screen, time_control, time_b, time_w, font, gameboard.turn)
    draw_status(screen, status)
    draw_buttons(screen)
