import copy

import random

pieceScore = {'k': 0, 'q': 9, 'r': 5, 'b': 3, 'n': 3, 'p': 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 4

"""
Chooses a random move
"""


def randmove(validmoves):
    return random.choice(validmoves)


"""
Finds the best move based on material
"""


# def findbestmove(gs, validmoves):
#     random.shuffle(validmoves)
#     turnmltp = 1 if gs.whiteToMove else -1
#     opminmax = CHECKMATE  # initially set to the highest value possible
#     bestmove = None
#     for move in validmoves:
#         gs.makeMove(move)
#         opmoves = gs.getValidMoves()  # possible moves for the opponent
#         if gs.checkmate:  # if this move leads to checkmate
#             opmax = -CHECKMATE  # opponent won't have a response and it'll be the lowest score for them(good for us)
#         elif gs.stalemate:  # if this move leads to stalemate
#             opmax = STALEMATE  # equal score
#         else:
#             opmax = -CHECKMATE  # highest score the opponent can get if we make this move, initially set to the lowest value
#             print('>>> Current move:', move.getChessNotation())
#             print("Checking for opponent moves now...")
#             for opmove in opmoves:
#                 gs.makeMove(opmove)
#                 gs.getValidMoves()  # to know in case its checkmate or stalemate
#                 if gs.checkmate:
#                     score = CHECKMATE  # if opponent can checkmate us
#                 elif gs.stalemate:
#                     score = STALEMATE  # if its a stalemate
#                 else:
#                     score = scoreMaterial(gs.board) * -turnmltp  # calculate material
#                 # print(opmove.getChessNotation(), "scores", score)
#
#                 if score > opmax:  # we are searching for the highest possible score for opponent
#                     opmax = score  # replace if its a higher score than the previous one
#                     print("> opmax now set to", opmax)
#                 gs.undoMove()
#
#         if opmax < opminmax:  # we want a move that gives the opponent the lowest score in their best way possible
#             opminmax = opmax  # replace if its a lower score than the previous one
#             print("---> opminmax now set to", opminmax)
#             bestmove = move
#             print("Best move set to...", bestmove.getChessNotation())
#         gs.undoMove()
#     print("<---------------------------->")
#     print("Best possible opp-score:", opminmax)
#     return bestmove


def encode(board):
    s = ''
    for r in board:
        for c in r:
            s += c
    return s


def findbestmove(gs, validmoves):
    global nextmove
    nextmove = None
    foo = copy.deepcopy(gs.castlelog)
    # random.shuffle(validmoves)
    # minmax(gs, validmoves, DEPTH, gs.whiteToMove, {}, {})
    negamaxalphabeta(gs, validmoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    gs.castlelog = foo
    gs.castle = foo[-1]
    return nextmove


def minmax(gs, validmoves, depth, wtm, wsco, bsco):
    random.shuffle(validmoves)
    global nextmove
    encoded = encode(gs.board)
    if depth == 0:
        return scoreboard(gs)

    if wtm:
        if encoded in wsco.keys():
            return wsco[encoded]
        max = -CHECKMATE
        for move in validmoves:
            gs.makeMove(move)
            opmoves = gs.getValidMoves()
            score = minmax(gs, opmoves, depth - 1, False, wsco, bsco)
            if score > max:
                max = score
                if depth == DEPTH:
                    nextmove = move
                    print(max)
            gs.undoMove()
        wsco[encoded] = max
        return max

    else:
        if encoded in bsco.keys():
            return bsco[encoded]
        min = CHECKMATE
        for move in validmoves:
            gs.makeMove(move)
            opmoves = gs.getValidMoves()
            score = minmax(gs, opmoves, depth - 1, True, wsco, bsco)
            if score < min:
                min = score
                if depth == DEPTH:
                    nextmove = move
                    print(min)
            gs.undoMove()
        bsco[encoded] = min
        return min


def negamax(gs, validmoves, depth, turnmltp):
    global nextmove
    if depth == 0:
        return turnmltp * scoreboard(gs)

    max = -CHECKMATE
    for move in validmoves:
        gs.makeMove(move)
        opmoves = gs.getValidMoves()
        score = -negamax(gs, opmoves, depth - 1, -turnmltp)
        if score > max:
            max = score
            if depth == DEPTH:
                nextmove = move
        gs.undoMove()
    return max


def negamaxalphabeta(gs, validmoves, depth, alpha, beta, turnmltp):
    global nextmove
    if depth == 0:
        return turnmltp * scoreboard(gs)

    max = -CHECKMATE
    for move in validmoves:
        gs.makeMove(move)
        opmoves = gs.getValidMoves()
        score = -negamaxalphabeta(gs, opmoves, depth - 1, -beta, -alpha,  -turnmltp)
        if score > max:
            max = score
            if depth == DEPTH:
                nextmove = move
        gs.undoMove()
        if max > alpha:
            alpha = max
        if alpha >= beta:
            break
    return max


def scoreboard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE  # bad for white
        else:
            return CHECKMATE  # bad for black

    if gs.stalemate:
        return STALEMATE

    score = 0
    for row in gs.board:
        for sq in row:
            if sq[0] == 'w':
                score += pieceScore[sq[1]]
            elif sq[0] == 'b':
                score -= pieceScore[sq[1]]

    return score


"""
Scores the board based on material
"""


def scoreMaterial(board):
    score = 0
    for row in board:
        for sq in row:
            if sq[0] == 'w':
                score += pieceScore[sq[1]]
            elif sq[0] == 'b':
                score -= pieceScore[sq[1]]

    return score


if __name__ == '__main__':
    b = [
        ['br', '--', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
        ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
        ['wb', '--', 'bn', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', 'wp', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['wp', 'wp', 'wp', 'wp', '--', 'wp', 'wp', 'wp'],
        ['wr', 'wn', 'wb', 'wq', 'wk', '--', 'wn', 'wr']]
