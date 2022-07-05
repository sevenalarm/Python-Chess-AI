"""
this is the main driver file
responsible for
    handling user input
    displaying the current GameState
    determining current valid moves
    and keeping a move log.
"""

import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

"""
Initialize a global dictionary of images. 
"""


def loadImages():
    pieces = ['br', 'bn', 'bb', 'bq', 'bk', 'bp', 'wr', 'wn', 'wb', 'wq', 'wk', 'wp']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f'images2/{piece}.png'), (SQ_SIZE, SQ_SIZE))


"""
Main Driver: Handling inputs & Updating the graphics.
"""


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    loadImages()  # only do this once, b4 the while loop
    running = True
    selectedSq = ()

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                #  getting the mouse input.
                loc = p.mouse.get_pos()  # (x, y)
                col = loc[0] // SQ_SIZE
                row = loc[1] // SQ_SIZE

                if selectedSq:
                    #  make the move.
                    move = ChessEngine.Move(selectedSq, (row, col), gs.board)
                    validMoves = gs.getPieceValidMoves(selectedSq[0], selectedSq[1])
                    vals = [m.getChessNotation() for m in validMoves]
                    print(vals)
                    if move.getChessNotation() in vals:
                        gs.makeMove(move)

                    # gs.makeMove(move)
                    selectedSq = ()  # deselect

                else:
                    if gs.board[row][col] != '--':
                        #  select the piece to move.
                        selectedSq = (row, col)
            elif e.type == p.KEYDOWN:
                if e.key == p.K_LEFT:
                    gs.undoMove()

        #  update the board.
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


"""
Responsible for all the graphics within the current game state
"""


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


"""
Draws the squares on the board.
"""


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("#5f7a85")]
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


if __name__ == '__main__':
    print()
    main()
