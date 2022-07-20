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

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.movedPiece
        self.moveLog.append(move)  # log the moves
        self.whiteToMove = not self.whiteToMove  # switch turns

    """
    Undo the last move made
    """

    def undoMove(self):
        if self.moveLog:
            move = self.moveLog.pop()
            self.board[move.endRow][move.endCol] = move.capturedPiece
            self.board[move.startRow][move.startCol] = move.movedPiece
            self.whiteToMove = not self.whiteToMove

    """
    All moves considering checks
    """

    def getValidMoves(self):
        return self.getAllPossibleMoves()  # for now

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
            if r - 1 > -1:  # fix this for pawn promotion !
                if self.board[r - 1][c] == "--":
                    moves.append(Move((r, c), (r - 1, c), self.board))
                    if r == 6 and self.board[r - 2][c] == "--":
                        moves.append(Move((r, c), (r - 2, c), self.board))
                if c - 1 >= 0:
                    if self.board[r - 1][c - 1][0] == 'b':  # enemy piece
                        moves.append(Move((r, c), (r - 1, c - 1), self.board))
                if c + 1 <= 7:
                    if self.board[r - 1][c + 1][0] == 'b':  # enemy piece
                        moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:
            if r + 1 < 8:  # fix this for pawn promotion !
                if self.board[r + 1][c] == "--":
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if r == 1 and self.board[r + 2][c] == "--":
                        moves.append(Move((r, c), (r + 2, c), self.board))
                if c - 1 >= 0:
                    if self.board[r + 1][c - 1][0] == 'w':  # enemy piece
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))
                if c + 1 <= 7:
                    if self.board[r + 1][c + 1][0] == 'w':  # enemy piece
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def getRookMoves(self, r, c, moves):
        for dr, dc in [(0, 1), (-1, 0), (0, -1), (1, 0)]:
            n = 1
            while 0 <= r+dr*n <= 7 and 0 <= c+dc*n <= 7:
                newr, newc = r+dr*n, c+dc*n
                if self.board[newr][newc] == "--":
                    moves.append(Move((r, c), (newr, newc), self.board))
                    n+=1
                else:
                    if self.board[newr][newc][0] != self.board[r][c][0]:
                        moves.append(Move((r, c), (newr, newc), self.board))
                    break

    def getKnightMoves(self, r, c, moves):
        for dr, dc in [(-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1)]:
            if 0 <= r+dr <= 7 and 0 <= c+dc <= 7:
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
