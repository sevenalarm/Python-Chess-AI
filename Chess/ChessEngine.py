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
        self.incheck, self.pins, self.checks = self.checkForPinsAndChecks()
        # print(self.pins)
        moves = []

        if self.whiteToMove:
            kr, kc = self.wkloc
        else:
            kr, kc = self.bkloc

        if self.incheck:
            print('check')
            if len(self.checks) == 1:  # only one check to deal with
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                crow, ccol = check[0], check[1]
                dir = (check[2], check[3])
                piece = self.board[crow][ccol]
                validSqs = []  # squares that pieces can move to
                if piece[1] == "n":  # if its a knight, it should be captured or the king must move.
                    validSqs = [(crow, ccol)]
                else:
                    for i in range(1, 8):
                        valsq = (kr + dir[0] * i, kc + dir[1] * i)
                        validSqs.append(valsq)
                        if valsq == (crow, ccol):
                            break

                # get rid of all the moves that don't stop the check
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].movedPiece[1] != "k":
                        if not (moves[i].endRow, moves[i].endCol) in validSqs:
                            moves.remove(moves[i])

            else:  # it's a double check
                self.getKingMoves(kr, kc, moves)
        else:  # not in check
            moves = self.getAllPossibleMoves()

        print('---------')
        return moves

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        incheck = False
        if self.whiteToMove:
            enm = "b"
            aly = "w"
            strow = self.wkloc[0]
            stcol = self.wkloc[1]
        else:
            enm = "w"
            aly = "b"
            strow = self.bkloc[0]
            stcol = self.bkloc[1]

        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]  # rook and bishop dirs
        for j in range(len(dirs)):
            d = dirs[j]
            posspin = ()
            for i in range(1, 8):
                endrow = strow + d[0] * i
                endcol = stcol + d[1] * i
                if 0 <= endrow <= 7 and 0 <= endcol <= 7:  # not out of board
                    piece = self.board[endrow][endcol]
                    if piece[0] == aly and piece[1] != "k":  # ally piece
                        if posspin == ():  # if there isn't a possible pin saved already
                            posspin = (endrow, endcol, d[0], d[1])
                        else:  # no potential checks or pins in this direction
                            break

                    elif piece[0] == enm:  # enemy piece, potential check or pin
                        type = piece[1]
                        if (0 <= j <= 3 and type == "r") or \
                                (4 <= j <= 7 and type == "b") or \
                                (i == 1 and type == "p" and (
                                        (enm == "w" and 4 <= j <= 5) or (enm == "b" and 6 <= j <= 7))) or \
                                (type == "q") or \
                                (i == 1 and type == "k"):  # check if the enemy piece is attacking the king
                            if posspin == ():  # if there is no ally piece in the middle, then it's a check
                                incheck = True
                                checks.append((endrow, endcol, d[0], d[1]))
                                break
                            else:  # if there is an ally piece in the middle, it would be pinned
                                pins.append(posspin)
                        else:  # the enemy piece is not attacking the king
                            break
                else:  # out of board, no need to continue
                    break

        knightDirs = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for d in knightDirs:
            endrow = strow + d[0]
            endcol = stcol + d[1]
            if 0 <= endrow <= 7 and 0 <= endcol <= 7:  # not out of board
                piece = self.board[endrow][endcol]
                if piece[0] == enm and piece[1] == "n":
                    incheck = True
                    checks.append((endrow, endcol, d[0], d[1]))
        return incheck, pins, checks

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
        for dr, dc in [(-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1)]:
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
        pinned = False
        dir = ()
        for p in self.pins:
            if p[0] == r and p[1] == c:
                pinned = True
                dir = (p[2], p[3])
                break

        if self.whiteToMove:
            if r - 1 > -1:
                if self.board[r - 1][c] == "--":  # move forward 1 square
                    if not pinned or dir == (-1, 0):
                        moves.append(Move((r, c), (r - 1, c), self.board))
                        if r == 6 and self.board[r - 2][c] == "--":  # move forward 2 squares
                            moves.append(Move((r, c), (r - 2, c), self.board))

                if c - 1 >= 0:  # take diagonally / left
                    if self.board[r - 1][c - 1][0] == 'b':  # enemy piece
                        if not pinned or dir == (-1, -1):
                            moves.append(Move((r, c), (r - 1, c - 1), self.board))
                if c + 1 <= 7:  # take diagonally / right
                    if self.board[r - 1][c + 1][0] == 'b':  # enemy piece
                        if not pinned or dir == (-1, 1):
                            moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:
            if r + 1 < 8:
                if self.board[r + 1][c] == "--":  # move forward 1 square
                    if not pinned or dir == (1, 0):
                        moves.append(Move((r, c), (r + 1, c), self.board))
                        if r == 1 and self.board[r + 2][c] == "--":  # move forward 2 squares
                            moves.append(Move((r, c), (r + 2, c), self.board))

                if c - 1 >= 0:  # take diagonally / left
                    if self.board[r + 1][c - 1][0] == 'w':  # enemy piece
                        if not pinned or dir == (1, -1):
                            moves.append(Move((r, c), (r + 1, c - 1), self.board))
                if c + 1 <= 7:  # take diagonally / right
                    if self.board[r + 1][c + 1][0] == 'w':  # enemy piece
                        if not pinned or dir == (1, 1):
                            moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def getRookMoves(self, r, c, moves):
        pinned = False
        dir = ()
        for p in self.pins:
            if p[0] == r and p[1] == c:
                pinned = True
                dir = (p[2], p[3])
                break

        for dr, dc in [(0, 1), (-1, 0), (0, -1), (1, 0)]:
            n = 1
            if not pinned or dir == (dr, dc) or dir == (-dr, -dc):
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
        for p in self.pins:
            if p[0] == r and p[1] == c:
                return
        for dr, dc in [(-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1)]:
            if 0 <= r + dr <= 7 and 0 <= c + dc <= 7:
                newr, newc = r + dr, c + dc
                if self.board[newr][newc][0] != self.board[r][c][0]:
                    moves.append(Move((r, c), (newr, newc), self.board))

    def getBishopMoves(self, r, c, moves):
        pinned = False
        dir = ()
        for p in self.pins:
            if p[0] == r and p[1] == c:
                pinned = True
                dir = (p[2], p[3])
                break

        for dr, dc in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
            n = 1
            if not pinned or dir == (dr, dc) or dir == (-dr, -dc):
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
        aly = "w" if self.whiteToMove else "b"
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if 0 <= r + dr <= 7 and 0 <= c + dc <= 7:
                    newr, newc = r + dr, c + dc
                    endsq = self.board[newr][newc]
                    if endsq[0] != aly:
                        if aly == "w":
                            self.wkloc = (newr, newc)
                        else:
                            self.bkloc = (newr, newc)
                        incheck, pins, checks = self.checkForPinsAndChecks()
                        if not incheck:
                            moves.append(Move((r, c), (newr, newc), self.board))
                        if aly == "w":
                            self.wkloc = (r, c)
                        else:
                            self.bkloc = (r, c)

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
