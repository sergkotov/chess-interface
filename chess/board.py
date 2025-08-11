from typing import Optional, List, Tuple
from .pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King
Position = Tuple[int, int]


class Board:
    def __init__(self):
        # grid[row][col]: [0][0] - top, left; [7][7] - botton, right
        self.grid: List[List[Optional[Piece]]] = [[None]*8 for _ in range(8)]
        self._setup_pieces()
    
    def is_on_board(self, pos: Position) -> bool:
        r, c = pos
        return 0 <= r < 8 and 0 <= c < 8

    def _setup_pieces(self):
        """Place pieces in starting positions."""
        # Default starting position
        # Kings
        self.grid[7][4] = King("white")
        self.grid[0][4] = King("black")
        # Queens
        self.grid[7][3] = Queen("white")
        self.grid[0][3] = Queen("black")
        # Rooks
        self.grid[7][0] = Rook("white")
        self.grid[7][7] = Rook("white")
        self.grid[0][0] = Rook("black")
        self.grid[0][7] = Rook("black")
        # Bishops
        self.grid[7][2] = Bishop("white")
        self.grid[7][5] = Bishop("white")
        self.grid[0][2] = Bishop("black")
        self.grid[0][5] = Bishop("black")
        # Knights
        self.grid[7][1] = Knight("white")
        self.grid[7][6] = Knight("white")
        self.grid[0][1] = Knight("black")
        self.grid[0][6] = Knight("black")
        # Pawns
        self.grid[6] = [Pawn("white") for _ in range(8)]
        self.grid[1] = [Pawn("black") for _ in range(8)]

        # Set piece positions
        for row in range(8):
            for col in range(8):
                if self.grid[row][col]:
                    self.grid[row][col].position = (row, col)

    def get_piece(self, pos):
        row, col = pos
        return self.grid[row][col]

    def _place(self, piece: Piece, pos: Position):
        r, c = pos
        self.grid[r][c] = piece
        piece.position = (r, c)

    def move_piece(self, start: Position, end: Position):
        """Execute move without validation. Handles capture and promotion (to queen)."""
        piece = self.get_piece(start)
        if piece is None:
            raise ValueError(f"No piece at {start}")
        # capture if any
        target = self.get_piece(end)
        if target is not None:
            # captured - just replace
            pass
        # move
        self.grid[end[0]][end[1]] = piece
        self.grid[start[0]][start[1]] = None
        piece.position = end

        # Pawn promotion hook: promote automatically to queen when reaching last rank
        if isinstance(piece, Pawn):
            last_row = 0 if piece.color == "white" else 7
            if end[0] == last_row:
                # promote to Queen (simple default)
                promoted = Queen(piece.color)
                self._place(promoted, end)

    def find_king(self, color: str) -> Optional[Position]:
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p and p.color == color and isinstance(p, King):
                    return (r, c)
        return None

    def is_square_attacked(self, pos: Position, by_color: str) -> bool:
        """Return True if any piece of by_color attacks pos (ignores pins)."""
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p is None or p.color != by_color:
                    continue
                # set temporary pos to ensure piece has position attribute
                # p.position should already be correct
                pseudo = p.get_pseudo_legal_moves(self)
                if pos in pseudo:
                    return True
        return False
