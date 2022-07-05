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

        self.whiteToMove = True
        self.moveLog = []
        if self.whiteToMove:
            self.turn = "w"
        else:
            self.turn = "b"

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
    Getting all the valid moves. (Not considering pins, castles, en-passant or checks for now)
    """

    def getAllValidMoves(self):
        validMoves = []
        b = self.board

        if self.whiteToMove:
            turn = "w"
        else:
            turn = "b"

        for r in range(8):
            for c in range(8):
                if b[r][c] != '--':
                    if b[r][c][0] == turn:

                        piece = b[r][c]

                        # Pawn
                        if piece[1] == "p":
                            validMoves += self.getPawnMoves(r, c)

                        # Rook
                        elif piece[1] == "r":
                            validMoves += self.getRookMoves(r, c)

                        # Knight
                        elif piece[1] == "n":
                            validMoves += self.getKnightMoves(r, c)

                        # Bishop
                        elif piece[1] == "b":
                            validMoves += self.getBishopMoves(r, c)

                        # Queen
                        if piece[1] == "q":
                            validMoves += self.getRookMoves(r, c)
                            validMoves += self.getBishopMoves(r, c)

                        # King
                        if piece[1] == "k":
                            validMoves += self.getKingMoves(r, c)

        return validMoves

    def getPieceValidMoves(self, r, c):
        piece = self.board[r][c]
        if self.whiteToMove:
            turn = "w"
        else:
            turn = "b"

        if piece[0] != turn:
            return []

        if piece[1] == "p":
            return self.getPawnMoves(r, c)

        elif piece[1] == "r":
            return self.getRookMoves(r, c)

        elif piece[1] == "n":
            return self.getKnightMoves(r, c)

        elif piece[1] == "b":
            return self.getBishopMoves(r, c)

        elif piece[1] == "q":
            return self.getBishopMoves(r, c) + self.getRookMoves(r, c)

        elif piece[1] == "k":
            return self.getKingMoves(r, c)

    def getPawnMoves(self, r, c):
        b = self.board
        if self.whiteToMove:
            turn = "w"
        else:
            turn = "b"
        validMoves = []

        # White Pawn
        if turn == "w":
            # Check if it can move 2 squares
            if r == 6:
                endSq = (r - 2, c)
                if b[endSq[0]][endSq[1]] == '--':
                    move = Move((r, c), endSq, b)
                    validMoves.append(move)

            # Move 1 square forward
            endSq = (r - 1, c)
            if not r - 1 < 0:
                if b[endSq[0]][endSq[1]] == '--':
                    move = Move((r, c), endSq, b)
                    validMoves.append(move)

            # Take a piece diagonally
            endSq = (r - 1, c - 1)
            if not (r - 1 < 0 or c - 1 < 0):
                if b[endSq[0]][endSq[1]] != '--':
                    move = Move((r, c), endSq, b)
                    validMoves.append(move)
            endSq = (r - 1, c + 1)
            if not (r - 1 < 0 or c + 1 > 7):
                if b[endSq[0]][endSq[1]] != '--':
                    move = Move((r, c), endSq, b)
                    validMoves.append(move)

        else:
            # Check if it can move 2 squares
            if r == 1:
                endSq = (r + 2, c)
                if b[endSq[0]][endSq[1]] == '--':
                    move = Move((r, c), endSq, b)
                    validMoves.append(move)

            # Move 1 square forward
            endSq = (r + 1, c)
            if not r + 1 > 7:
                if b[endSq[0]][endSq[1]] == '--':
                    move = Move((r, c), endSq, b)
                    validMoves.append(move)

            # Take a piece diagonally
            endSq = (r + 1, c - 1)
            if not (r + 1 > 7 or c - 1 < 0):
                if b[endSq[0]][endSq[1]] != '--':
                    move = Move((r, c), endSq, b)
                    validMoves.append(move)
            endSq = (r + 1, c + 1)
            if not (r + 1 > 7 or c + 1 > 7):
                if b[endSq[0]][endSq[1]] != '--':
                    move = Move((r, c), endSq, b)
                    validMoves.append(move)

        return validMoves

    def getRookMoves(self, r, c):
        b = self.board
        if self.whiteToMove:
            turn = "w"
        else:
            turn = "b"
        validMoves = []
        disl = c
        disr = 7 - c
        dist = r
        disb = 7 - r

        # to left
        for dc in range(1, disl + 1):
            endSq = (r, c - dc)
            if b[endSq[0]][endSq[1]] == '--':
                move = Move((r, c), endSq, b)
                validMoves.append(move)
            else:
                if b[endSq[0]][endSq[1]][0] != turn:
                    move = Move((r, c), endSq, b)
                    validMoves.append(move)
                break

        # to right
        for dc in range(1, disr + 1):
            endSq = (r, c + dc)
            if b[endSq[0]][endSq[1]] == '--':
                move = Move((r, c), endSq, b)
                validMoves.append(move)
            else:
                if b[endSq[0]][endSq[1]][0] != turn:
                    move = Move((r, c), endSq, b)
                    validMoves.append(move)
                break

        # to top
        for dr in range(1, dist + 1):
            endSq = (r - dr, c)
            if b[endSq[0]][endSq[1]] == '--':
                move = Move((r, c), endSq, b)
                validMoves.append(move)
            else:
                if b[endSq[0]][endSq[1]][0] != turn:
                    move = Move((r, c), endSq, b)
                    validMoves.append(move)
                break

        # to bottom
        for dr in range(1, disb + 1):
            endSq = (r + dr, c)
            if b[endSq[0]][endSq[1]] == '--':
                move = Move((r, c), endSq, b)
                validMoves.append(move)
            else:
                if b[endSq[0]][endSq[1]][0] != turn:
                    move = Move((r, c), endSq, b)
                    validMoves.append(move)
                break

        return validMoves

    def getKnightMoves(self, r, c):
        b = self.board
        if self.whiteToMove:
            turn = "w"
        else:
            turn = "b"
        validMoves = []
        for dr in [-1, 1]:
            for dc in [-2, 2]:
                endSq = (r + dr, c + dc)
                out_of_board = endSq[0] < 0 or endSq[0] > 7 or endSq[1] < 0 or endSq[1] > 7
                if not out_of_board and b[endSq[0]][endSq[1]][0] != turn:
                    move = Move((r, c), endSq, b)
                    validMoves.append(move)

        for dr in [-2, 2]:
            for dc in [-1, 1]:
                endSq = (r + dr, c + dc)
                out_of_board = endSq[0] < 0 or endSq[0] > 7 or endSq[1] < 0 or endSq[1] > 7
                if not out_of_board and b[endSq[0]][endSq[1]][0] != turn:
                    move = Move((r, c), endSq, b)
                    validMoves.append(move)

        return validMoves

    def getBishopMoves(self, r, c):
        b = self.board
        if self.whiteToMove:
            turn = "w"
        else:
            turn = "b"
        validMoves = []

        disl = c
        disr = 7 - c
        dist = r
        disb = 7 - r

        # top-left
        for d in range(1, min(disl, dist) + 1):
            endSq = (r - d, c - d)
            if b[endSq[0]][endSq[1]] == '--':
                move = Move((r, c), endSq, b)
                validMoves.append(move)
            else:
                if b[endSq[0]][endSq[1]][0] != turn:
                    move = Move((r, c), endSq, b)
                    validMoves.append(move)
                break

        # top-right
        for d in range(1, min(disr, dist) + 1):
            endSq = (r - d, c + d)
            if b[endSq[0]][endSq[1]] == '--':
                move = Move((r, c), endSq, b)
                validMoves.append(move)
            else:
                if b[endSq[0]][endSq[1]][0] != turn:
                    move = Move((r, c), endSq, b)
                    validMoves.append(move)
                break

        # bottom-left
        for d in range(1, min(disl, disb) + 1):
            endSq = (r + d, c - d)
            if b[endSq[0]][endSq[1]] == '--':
                move = Move((r, c), endSq, b)
                validMoves.append(move)
            else:
                if b[endSq[0]][endSq[1]][0] != turn:
                    move = Move((r, c), endSq, b)
                    validMoves.append(move)
                break

        # bottom-right
        for d in range(1, min(disr, disb) + 1):
            endSq = (r + d, c + d)
            if b[endSq[0]][endSq[1]] == '--':
                move = Move((r, c), endSq, b)
                validMoves.append(move)
            else:
                if b[endSq[0]][endSq[1]][0] != turn:
                    move = Move((r, c), endSq, b)
                    validMoves.append(move)
                break

        return validMoves

    def getKingMoves(self, r, c):
        b = self.board
        if self.whiteToMove:
            turn = "w"
        else:
            turn = "b"
        validMoves = []
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                endSq = (r + dr, c + dc)
                out_of_board = endSq[0] < 0 or endSq[0] > 7 or endSq[1] < 0 or endSq[1] > 7
                if not out_of_board and b[endSq[0]][endSq[1]][0] != turn:
                    move = Move((r, c), endSq, b)
                    validMoves.append(move)

        return validMoves

    def isCheck(self):
        b = self.board
        king = ()
        for r in range(8):
            for c in range(8):
                if b[r][c] == self.turn+"k":
                    king = (r, c)
        r, c = king[0], king[1]

        # Horizontally or Vertically in check (Rook / Queen)
        disl = c
        disr = 7 - c
        dist = r
        disb = 7 - r
        # to left
        for dc in range(1, disl + 1):
            if b[r][c-dc][1] != '--':
                if (b[r][c-dc][1] == 'r' or b[r][c-dc][1] == 'q') and not b[r][c-dc][0] == self.turn:
                    return True
                break
        # to right
        for dc in range(1, disr + 1):
            if b[r][c - dc][1] != '--':
                if (b[r][c + dc][1] == 'r' or b[r][c + dc][1] == 'q') and not b[r][c + dc][0] == self.turn:
                    return True
                break
        # to top
        for dr in range(1, dist + 1):
            if b[r][c - dr][1] != '--':
                if (b[r - dr][c][1] == 'r' or b[r - dr][c][1] == 'q') and not b[r - dr][c][0] == self.turn:
                    return True
                break
        # to bottom
        for dr in range(1, disb + 1):
            if b[r][c - dr][1] != '--':
                if (b[r + dr][c][1] == 'r' or b[r + dr][c][1] == 'q') and not b[r + dr][c][0] == self.turn:
                    return True
                break


        # Diagonally in check (Bishop / Queen)

        # Check with pawn

        # Check with knight

        # Kings in touch


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


