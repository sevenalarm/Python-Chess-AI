class GameState:

    def __init__(self):
        self.board = [
            ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']]
        self.moveFunctions = {"p": self.getPawnMoves, "r": self.getRookMoves, "n": self.getKnightMoves,
                              "b": self.getBishopMoves, "q": self.getQueenMoves, "k": self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []

        # saving the locations of the two kings on the board
        self.wkloc = (7, 4)
        self.bkloc = (0, 4)

        self.checkmate = False
        self.stalemate = False
        self.inCheck = False
        self.pins = []
        self.checks = []

    """
    Makes a given move
    """

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.movedPiece
        self.moveLog.append(move)  # log the moves
        self.whiteToMove = not self.whiteToMove  # switch turns

        # update kings location
        if move.movedPiece == "wk":
            self.wkloc = (move.endRow, move.endCol)
        elif move.movedPiece == "bk":
            self.bkloc = (move.endRow, move.endCol)

    """
    Undo the last move made
    """

    def undoMove(self):
        if self.moveLog:
            move = self.moveLog.pop()
            self.board[move.endRow][move.endCol] = move.capturedPiece
            self.board[move.startRow][move.startCol] = move.movedPiece
            self.whiteToMove = not self.whiteToMove
            if move.movedPiece == "wk":
                self.wkloc = (move.startRow, move.startCol)
            elif move.movedPiece == "bk":
                self.bkloc = (move.startRow, move.startCol)

    """
    All moves considering checks
    """

    def getValidMoves(self):
        # self.incheck, self.pins, self.checks = self.checkForPinsAndChecks()

        # get all the possible moves
        moves = self.getAllPossibleMoves()
        # for each move, make the move
        for i in range(len(moves) - 1, -1, -1):  # iterating backwards so we dont face bugs
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.incheck2():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        if len(moves) == 0:
            if self.incheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        return moves

    """
    Determine if the current player is in check
    """

    def incheck(self):
        if self.whiteToMove:
            return self.sqUnderAttack(self.wkloc[0], self.wkloc[1])
        else:
            return self.sqUnderAttack(self.bkloc[0], self.bkloc[1])

    def incheck2(self):
        if self.whiteToMove:
            king = self.wkloc
        else:
            king = self.bkloc
        r, c = king[0], king[1]

        # Vertical / Horizontal
        for dr, dc in [(0, 1), (-1, 0), (0, -1), (1, 0)]:
            n = 1
            while 0 <= r + dr * n <= 7 and 0 <= c + dc * n <= 7:
                newr, newc = r + dr * n, c + dc * n
                if self.board[newr][newc] != "--":  # not an empty square
                    if self.board[newr][newc][0] != self.board[r][c][0] and (
                            self.board[newr][newc][1] == 'r' or
                            self.board[newr][newc][1] == 'q'):
                        # enemy piece + rook or queen
                        return True
                    break
                else:
                    n += 1

        # Diagonal
        for dr, dc in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
            n = 1
            while 0 <= r + dr * n <= 7 and 0 <= c + dc * n <= 7:
                newr, newc = r + dr * n, c + dc * n
                if self.board[newr][newc] != "--":  # not an empty square
                    if self.board[newr][newc][0] != self.board[r][c][0] and (
                            self.board[newr][newc][1] == 'b' or
                            self.board[newr][newc][1] == 'q'):
                        # enemy piece + bishop or queen
                        return True
                    break
                else:
                    n += 1

        # Knight Check
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if 0 <= r + dr <= 7 and 0 <= c + dc <= 7:
                    newr, newc = r + dr, c + dc
                    if self.board[newr][newc] != "--":  # not an empty square
                        if self.board[newr][newc][0] != self.board[r][c][0] and (
                                self.board[newr][newc][1] == 'n'):
                            # enemy piece + knight
                            return True

        # Pawn Check
        if self.whiteToMove:
            if r - 1 > -1:
                if c - 1 >= 0:  # diagonally
                    if self.board[r - 1][c - 1] == 'bp':  # enemy piece
                        return True
                if c + 1 <= 7:  # diagonally
                    if self.board[r - 1][c + 1] == 'bp':  # enemy piece
                        return True
        else:
            if r + 1 < 8:
                if c - 1 >= 0:  # diagonally
                    if self.board[r + 1][c - 1] == 'wp':  # enemy piece
                        return True
                if c + 1 <= 7:  # diagonally
                    if self.board[r + 1][c + 1] == 'wp':  # enemy piece
                        return True



        # Kings in touch
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if 0 <= r + dr <= 7 and 0 <= c + dc <= 7:
                    newr, newc = r + dr, c + dc
                    if self.board[newr][newc][0] != self.board[r][c][0] and (
                            self.board[newr][newc][1] == 'k'):
                        # enemy piece + knight
                        return True

        return False

    """
    Determine if the enemy can attack the square (r,c)
    """

    def sqUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove  # switch to opponent's pov
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for m in oppMoves:
            if m.endRow == r and m.endCol == c:
                return True
        return False

    """
    All moves without considering checks
    """

    def getAllPossibleMoves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)

        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if r - 1 > -1:
                if self.board[r - 1][c] == "--":  # move forward 1 square
                    moves.append(Move((r, c), (r - 1, c), self.board))
                    if r == 6 and self.board[r - 2][c] == "--":
                        moves.append(Move((r, c), (r - 2, c), self.board))
                if c - 1 >= 0:  # take diagonally
                    if self.board[r - 1][c - 1][0] == 'b':  # enemy piece
                        moves.append(Move((r, c), (r - 1, c - 1), self.board))
                if c + 1 <= 7:  # take diagonally
                    if self.board[r - 1][c + 1][0] == 'b':  # enemy piece
                        moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:
            if r + 1 < 8:
                if self.board[r + 1][c] == "--":  # move forward 1 square
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if r == 1 and self.board[r + 2][c] == "--":
                        moves.append(Move((r, c), (r + 2, c), self.board))
                if c - 1 >= 0:  # take diagonally
                    if self.board[r + 1][c - 1][0] == 'w':  # enemy piece
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))
                if c + 1 <= 7:  # take diagonally
                    if self.board[r + 1][c + 1][0] == 'w':  # enemy piece
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def getRookMoves(self, r, c, moves):
        for dr, dc in [(0, 1), (-1, 0), (0, -1), (1, 0)]:
            n = 1
            while 0 <= r + dr * n <= 7 and 0 <= c + dc * n <= 7:
                newr, newc = r + dr * n, c + dc * n
                if self.board[newr][newc] == "--":
                    moves.append(Move((r, c), (newr, newc), self.board))
                    n += 1
                else:
                    if self.board[newr][newc][0] != self.board[r][c][0]:
                        moves.append(Move((r, c), (newr, newc), self.board))
                    break

    def getKnightMoves(self, r, c, moves):
        for dr, dc in [(-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1)]:
            if 0 <= r + dr <= 7 and 0 <= c + dc <= 7:
                newr, newc = r + dr, c + dc
                if self.board[newr][newc][0] != self.board[r][c][0]:
                    moves.append(Move((r, c), (newr, newc), self.board))

    def getBishopMoves(self, r, c, moves):
        for dr, dc in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
            n = 1
            while 0 <= r + dr * n <= 7 and 0 <= c + dc * n <= 7:
                newr, newc = r + dr * n, c + dc * n
                if self.board[newr][newc] == "--":
                    moves.append(Move((r, c), (newr, newc), self.board))
                    n += 1
                else:
                    if self.board[newr][newc][0] != self.board[r][c][0]:
                        moves.append(Move((r, c), (newr, newc), self.board))
                    break

    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if 0 <= r + dr <= 7 and 0 <= c + dc <= 7:
                    newr, newc = r + dr, c + dc
                    if self.board[newr][newc][0] != self.board[r][c][0]:
                        moves.append(Move((r, c), (newr, newc), self.board))


class Move:
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.movedPiece = board[self.startRow][self.startCol]
        self.capturedPiece = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    """Override the equals method"""

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        piece = self.movedPiece[1]
        if "p" in piece:
            return self.getRankFile(self.endRow, self.endCol)
        return self.movedPiece[1].capitalize() + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


if __name__ == '__main__':
    gs = GameState()
    gs.board = [
        ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
        ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['wp', 'wp', 'wp', 'wp', 'br', 'wp', 'wp', 'wp'],
        ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']]

    # vals = [m.getChessNotation() for m in gs.getAllValidMoves()]
    # print(vals)
    # print(gs.isCheck())
