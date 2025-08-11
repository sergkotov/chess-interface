from typing import List, Tuple, Optional
Position = Tuple[int, int]  # (row, col) with 0..7


class Piece:
    def __init__(self, color: str, name: str):
        assert color in ("white", "black")
        self.color = color
        self.name = name
        self.position: Optional[Position] = None

    def clone(self):
        """Return a lightweight clone for move simulation."""
        cls = self.__class__
        new = cls(self.color)
        new.position = None if self.position is None else (
            self.position[0], self.position[1])
        return new

    def get_pseudo_legal_moves(self, board) -> List[Position]:
        """Return moves ignoring checks (override per-piece)."""
        return []

    def __repr__(self):
        return f"<{self.color[0].upper()}{self.name[0].upper()}@{self.position}>"


class King(Piece):
    def __init__(self, color: str):
        super().__init__(color, "king")

    def get_pseudo_legal_moves(self, board):
        moves = []
        r, c = self.position
        for dr in (-1,0,1):
            for dc in (-1,0,1):
                if dr == 0 and dc == 0:
                    continue
                pos = (r+dr, c+dc)
                if board.is_on_board(pos):
                    target = board.get_piece(pos)
                    if target is None or target.color != self.color:
                        moves.append(pos)
        # Note: castling not implemented here
        return moves

class SlidingPiece(Piece):
    """Shared logic for rook, bishop, queen."""
    directions = []  # override in subclasses

    def get_pseudo_legal_moves(self, board):
        moves = []
        r, c = self.position
        for dr, dc in self.directions:
            nr, nc = r + dr, c + dc
            while board.is_on_board((nr, nc)):
                target = board.get_piece((nr, nc))
                if target is None:
                    moves.append((nr, nc))
                else:
                    if target.color != self.color:
                        moves.append((nr, nc))
                    break
                nr += dr; nc += dc
        return moves

class Queen(SlidingPiece):
    def __init__(self, color: str):
        super().__init__(color, "queen")
    directions = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]


class Rook(SlidingPiece):
    def __init__(self, color: str):
        super().__init__(color, "rook")
    directions = [(1,0),(-1,0),(0,1),(0,-1)]


class Bishop(SlidingPiece):
    def __init__(self, color: str):
        super().__init__(color, "bishop")
    directions = [(1,1),(1,-1),(-1,1),(-1,-1)]


class Knight(Piece):
    def __init__(self, color: str):
        super().__init__(color, "knight")

    def get_pseudo_legal_moves(self, board):
        moves = []
        r, c = self.position
        deltas = [(2,1),(2,-1),(1,2),(1,-2),(-1,2),(-1,-2),(-2,1),(-2,-1)]
        for dr, dc in deltas:
            pos = (r+dr, c+dc)
            if board.is_on_board(pos):
                target = board.get_piece(pos)
                if target is None or target.color != self.color:
                    moves.append(pos)
        return moves


class Pawn(Piece):
    def __init__(self, color: str):
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
            start_row = 1 if self.color == "black" else 6
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
