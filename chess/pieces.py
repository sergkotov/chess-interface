from typing import List, Tuple, Optional
Position = Tuple[int, int]  # (row, col) with 0..7

class Piece:
    def __init__(self, color, name):
        self.color = color  # "white" or "black"
        self.name = name    # "king", "queen", "rook", "bishop", "knight", "pawn"
        self.position: Optional[Position] = None

    def get_pseudo_legal_moves(self, board) -> List[Position]:
        """Return moves ignoring checks (override per-piece)."""
        return []


class King(Piece):
    def __init__(self, color):
        super().__init__(color, "king")

    def get_legal_moves(self, board):
        return []


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, "queen")

    def get_legal_moves(self, board):
        return []


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, "rook")

    def get_legal_moves(self, board):
        return []


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, "bishop")

    def get_legal_moves(self, board):
        return []


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, "knight")

    def get_legal_moves(self, board):
        return []


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, "pawn")

    def get_pseudo_legal_moves(self, board):
        moves = []
        r, c = self.position
        direction = -1 if self.color == "white" else 1
        # One square forward
        forward = (r + direction, c)
        if board.is_on_board(forward) and board.get_piece(forward) is None:
            moves.append(forward)
            # Two squares from starting rank
            start_row = 6 if self.color == "black" else 1
            two_forward = (r + 2*direction, c)
            if r == start_row and board.get_piece(two_forward) is None:
                moves.append(two_forward)
        # Captures
        for dc in (-1, 1):
            cap = (r + direction, c + dc)
            if board.is_on_board(cap):
                target = board.get_piece(cap)
                if target and target.color != self.color:
                    moves.append(cap)
        # Note: en-passant not implemented
        return moves
