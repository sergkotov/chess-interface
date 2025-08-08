# chess/board.py
class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self._setup_pieces()

    def _setup_pieces(self):
        """Place pieces in starting positions."""
        from .pieces import Pawn, Rook
        # Example setup
        # self.grid[1] = [Pawn("white") for _ in range(8)]
        # self.grid[6] = [Pawn("black") for _ in range(8)]
        # self.grid[0][0] = Rook("white")
        # self.grid[0][7] = Rook("white")
        # self.grid[7][0] = Rook("black")
        # self.grid[7][7] = Rook("black")
        # ... Add rest of pieces

        # Set piece positions
        for row in range(8):
            for col in range(8):
                if self.grid[row][col]:
                    self.grid[row][col].position = (row, col)

    def move_piece(self, start_pos, end_pos):
        """Move a piece from start to end position."""
        piece = self.get_piece(start_pos)
        if piece:
            self.grid[end_pos[0]][end_pos[1]] = piece
            self.grid[start_pos[0]][start_pos[1]] = None
            piece.position = end_pos

    def get_piece(self, pos):
        row, col = pos
        return self.grid[row][col]
