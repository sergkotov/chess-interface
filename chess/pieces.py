from typing import List, Tuple, Optional
Position = Tuple[int, int]  # (row, col) with 0..7


class Piece:
    def __init__(self, color: str, name: str):
        assert color in ("white", "black")
        self.color = color
        self.name = name
        self.position: Optional[Position] = None
        self.has_moved = False

    def clone(self):
        """Return a lightweight clone for move simulation."""
        cls = self.__class__
        new = cls(self.color)
        new.position = None if self.position is None else (
            self.position[0], self.position[1])
        new.has_moved = self.has_moved
        return new

    def get_pseudo_legal_moves(self, board) -> List[Position]:
        """Return moves ignoring checks (override per-piece)."""
        return []

    def __repr__(self):
        return f"<{self.color[0].upper()}{self.name[0].upper()}@{self.position}>"


class King(Piece):
    def __init__(self, color: str):
        super().__init__(color, "king")

    def get_pseudo_legal_moves(self, board, for_attack=False):
        moves = []
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        r, c = self.position
        for dr, dc in directions:
            pos = (r+dr, c+dc)
            if board.is_on_board(pos):
                target = board.get_piece(pos)
                if target is None or target.color != self.color:
                    moves.append(pos)
        if not for_attack and not self.has_moved:
            # Kingside
            if self._can_castle(board, kingside=True):
                moves.append((r, c + 2))
            # Queenside
            if self._can_castle(board, kingside=False):
                moves.append((r, c - 2))

        return moves


    def _can_castle(self, board, kingside: bool) -> bool:
        r, c = self.position
        back_rank = r
        if kingside:
            rook_pos = (back_rank, 7)
            empty_squares = [(r, c+1), (r, c+2)]
        else:
            rook_pos = (back_rank, 0)
            empty_squares = [(r, c-1), (r, c-2), (r, c-3)]

        rook = board.get_piece(rook_pos)
        if not rook or rook.has_moved:
            return False
        # Squares between king and rook must be empty
        for sq in empty_squares:
            if board.get_piece(sq) is not None:
                return False
        # Squares the king passes through must not be attacked
        for sq in [(r, c), (r, c + (2 if kingside else -2)), (r, c + (1 if kingside else -1))]:
            if board.is_square_attacked(sq, "white" if self.color == "black" else "black"):
                return False
        return True

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
        # Forward
        forward = (r + direction, c)
        if board.is_on_board(forward) and board.get_piece(forward) is None:
            moves.append(forward)
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
        # En-passant
        if board.en_passant_target:
            ep_row, ep_col = board.en_passant_target
            if r + direction == ep_row and abs(ep_col - c) == 1:
                moves.append((ep_row, ep_col))

        return moves
