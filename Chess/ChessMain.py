"""
this is the main driver file
responsible for
    handling user input
    displaying the current GameState
    determining current valid moves
    and keeping a move log.
"""

""" checks, checkmate and stalemate are now working fine (part 7) """

import pygame as p

from Chess import ChessEngine
from SmartMoveFinder import *
import time

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

"""
Initialize a global dictionary of images2. 
"""


def loadImages():
    pieces = ['br', 'bn', 'bb', 'bq', 'bk', 'bp', 'wr', 'wn', 'wb', 'wq', 'wk', 'wp']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f'../images/{piece}.png'), (SQ_SIZE, SQ_SIZE))


"""
Main Driver: Handling inputs & Updating the graphics.
"""


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  # when a move is made
    doanim = False
    loadImages()  # only do this once, b4 the while loop
    running = True
    selectedSq = ()
    over = False
    pl1 = False  # True if human is playing white else False
    pl2 = False  # Vice versa

    while running:
        humanTurn = (gs.whiteToMove and pl1) or (not gs.whiteToMove and pl2)

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # handling the human turn
            elif e.type == p.MOUSEBUTTONDOWN:
                if not over and humanTurn:
                    #  getting the mouse input.
                    loc = p.mouse.get_pos()  # (x, y)
                    col = loc[0] // SQ_SIZE
                    row = loc[1] // SQ_SIZE

                    if selectedSq:
                        for i in range(len(validMoves)):
                            #  make the move.
                            move = ChessEngine.Move(selectedSq, (row, col), gs.board)
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                print("Player goes:",move.getChessNotation())
                                # print(f'Castle rights: wks:{gs.castle.wks} / wqs:{gs.castle.wqs} / bks:{gs.castle.bks} / bqs:{gs.castle.bqs}')
                                # print_board(gs.board)
                                print('-----------------------------------------------------------------')
                                moveMade = True
                                doanim = True

                        # gs.makeMove(move)
                        selectedSq = ()  # deselect

                    if not moveMade:
                        if gs.board[row][col] != '--':
                            #  select the piece to move.
                            selectedSq = (row, col)
            # undoing a move
            elif e.type == p.KEYDOWN:
                if e.key == p.K_LEFT:
                    gs.undoMove()
                    moveMade = True
                    doanim = False

                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    selectedSq = ()
                    moveMade = False
                    doanim = False

        # AI moves
        if not over and not humanTurn:
            AImove = findbestmove(gs, validMoves)
            # AImove = None
            if AImove is None:
                AImove = randmove(validMoves)
                print("Randomized!!!!!!!!!!!")
            gs.makeMove(AImove)
            print("Compy goes:",AImove.getChessNotation())
            # print(
            #     f'Castle rights: wks:{gs.castle.wks} / wqs:{gs.castle.wqs} / bks:{gs.castle.bks} / bqs:{gs.castle.bqs}')

            # print_board(gs.board)
            print('---------')
            moveMade = True
            doanim = True

        if moveMade:
            if doanim:
                animate(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False

        #  update the board.
        drawGameState(screen, gs, validMoves, selectedSq)
        # time.sleep(0.3)
        if gs.checkmate:
            over = True
            if gs.whiteToMove:
                drawtext(screen, 'Black wins by Checkmate!')
            else:
                drawtext(screen, 'White wins by Checkmate!')

        elif gs.stalemate:
            over = True
            drawtext(screen, 'Stalemate')

        else:
            over = False

        clock.tick(MAX_FPS)
        p.display.flip()


"""
Highlight the square selected and possible moves for the selected piece
"""


def hightlightSqs(screen, gs, validmoves, selectedSq):
    if selectedSq:
        r, c = selectedSq
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            # hightlight selectedSq
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            # highligh possible moves for the selected piece
            s.fill(p.Color('yellow'))
            for m in validmoves:
                if m.startRow == r and m.startCol == c:
                    screen.blit(s, (SQ_SIZE * m.endCol, SQ_SIZE * m.endRow))


"""
Responsible for all the graphics within the current game state
"""


def drawGameState(screen, gs, validmoves, selectedSq):
    drawBoard(screen)
    hightlightSqs(screen, gs, validmoves, selectedSq)
    drawPieces(screen, gs.board)


"""
Draws the squares on the board.
"""


def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("grey")]
    for x in range(DIMENSION):
        for y in range(DIMENSION):
            color = colors[(x + y) % 2]
            p.draw.rect(screen, color, p.Rect(x * SQ_SIZE, y * SQ_SIZE, SQ_SIZE, SQ_SIZE))


"""
Draw the pieces on the board according to the current GameState.Board.
"""


def drawPieces(screen, board):
    for r in range(8):
        for c in range(8):
            rect = p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            piece = board[r][c]
            if piece != '--':
                img = IMAGES[piece]
                screen.blit(img, rect)


"""
Animations!
"""


def animate(move, screen, board, clock):
    global colors
    dr = move.endRow - move.startRow
    dc = move.endCol - move.startCol
    fps = 5  # frame per square
    framecount = (abs(dr) + abs(dc)) * fps
    for f in range(framecount + 1):
        r, c = (move.startRow + dr * f / framecount, move.startCol + dc * f / framecount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the moved piece from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endsq = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endsq)
        # blit the captured piece into the rectangle
        if move.capturedPiece != '--':
            screen.blit(IMAGES[move.capturedPiece], endsq)
        # draw the moving piece
        screen.blit(IMAGES[move.movedPiece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(90)


def drawtext(screen, txt):
    font = p.font.SysFont("Calibri", 32, True, False)
    txtobj = font.render(txt, 0, p.Color('Grey'))
    txtloc = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - txtobj.get_width() / 2, HEIGHT / 2 - txtobj.get_height() / 2)
    screen.blit(txtobj, txtloc)
    txtobj = font.render(txt, 0, p.Color('Black'))
    screen.blit(txtobj, txtloc.move(2, 2))


def print_board(board):
    for r in board:
        print(r)


if __name__ == '__main__':
    main()


