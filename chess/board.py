from typing import Optional, List, Tuple
from .pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King
Position = Tuple[int, int]


class Board:
    def __init__(self):
        # grid[row][col]: [0][0] - top, left; [7][7] - botton, right
        self.grid: List[List[Optional[Piece]]] = [[None]*8 for _ in range(8)]
        self.en_passant_target: Optional[Position] = None
        self._setup_pieces()

    def is_on_board(self, pos: Position) -> bool:
        r, c = pos
        return 0 <= r < 8 and 0 <= c < 8

    def _place(self, piece: Piece, pos: Position):
        r, c = pos
        self.grid[r][c] = piece
        piece.position = (r, c)

    def _setup_pieces(self):
        """Place pieces in starting positions."""
        # clear board
        self.grid = [[None]*8 for _ in range(8)]
        self.en_passant_target = None
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

    def move_piece(self, start: Position, end: Position):
        """Execute move without validation. Handles capture and promotion (to queen)."""
        piece = self.get_piece(start)
        if piece is None:
            raise ValueError(f"No piece at {start}")

        # --- En passant capture (use current en_passant_target if set) ---
        if isinstance(piece, Pawn) and self.en_passant_target is not None and end == self.en_passant_target:
            # The pawn being captured sits behind the target square (relative to the mover)
            direction = -1 if piece.color == "white" else 1
            captured_pos = (end[0] - direction, end[1])
            self.grid[captured_pos[0]][captured_pos[1]] = None

        # --- Castling: move rook accordingly if king moves two squares ---
        if isinstance(piece, King) and abs(end[1] - start[1]) == 2:
            back_rank = start[0]
            if end[1] == 6:  # kingside
                rook_start = (back_rank, 7)
                rook_end = (back_rank, 5)
            else:  # queenside
                rook_start = (back_rank, 0)
                rook_end = (back_rank, 3)
            rook = self.get_piece(rook_start)
            if rook:
                self.grid[rook_end[0]][rook_end[1]] = rook
                self.grid[rook_start[0]][rook_start[1]] = None
                rook.position = rook_end
                rook.has_moved = True

        # --- Move the piece itself ---
        self.grid[end[0]][end[1]] = piece
        self.grid[start[0]][start[1]] = None
        piece.position = end
        piece.has_moved = True

        # --- Pawn promotion (auto-queen) ---
        if isinstance(piece, Pawn):
            last_row = 0 if piece.color == "white" else 7
            if end[0] == last_row:
                promoted = Queen(piece.color)
                promoted.has_moved = True
                self._place(promoted, end)

        # --- Update en_passant_target: default clear, set only for pawn double-move ---
        self.en_passant_target = None
        if isinstance(piece, Pawn) and abs(end[0] - start[0]) == 2:
            middle_row = (start[0] + end[0]) // 2
            self.en_passant_target = (middle_row, start[1])

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
    
    def clone(self) -> "Board":
        """Create a deep-ish clone for move simulation (pieces cloned, positions preserved)."""
        new = Board.__new__(Board)  # bypass __init__
        new.grid = [[None]*8 for _ in range(8)]
        new.en_passant_target = None if self.en_passant_target is None else (self.en_passant_target[0], self.en_passant_target[1])
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p is not None:
                    p_clone = p.clone()
                    new.grid[r][c] = p_clone
                    p_clone.position = (r, c)
        return new
    
    def is_in_check(self, color: str) -> bool:
        king_pos = self.find_king(color)
        if king_pos is None:
            # Shouldn't happen in a normal game; treat as in-check to be safe
            return True
        enemy = "white" if color == "black" else "black"
        return self.is_square_attacked(king_pos, enemy)
    
    def get_legal_moves_for_piece(self, pos: Position) -> List[Position]:
        """Return moves for piece at pos, filtered so king isn't left in check."""
        piece = self.get_piece(pos)
        if piece is None:
            return []
        pseudo = piece.get_pseudo_legal_moves(self)
        legal = []
        for dest in pseudo:
            # simulate move on cloned board
            b_clone = self.clone()
            b_clone.move_piece(pos, dest)
            if not b_clone.is_in_check(piece.color):
                legal.append(dest)
        return legal
    
    def get_all_legal_moves(self, color: str):
        """Return dict mapping piece positions -> legal destinations."""
        moves = {}
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p and p.color == color:
                    lm = self.get_legal_moves_for_piece((r,c))
                    if lm:
                        moves[(r,c)] = lm
        return moves
