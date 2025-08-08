# chess/pieces.py
class Piece:
    def __init__(self, color, name):
        self.color = color  # "white" or "black"
        self.name = name    # "pawn", "rook", etc.
        self.position = None  # (row, col)

    def get_legal_moves(self, board):
        """Override in subclasses to return a list of legal moves."""
        return []

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, "pawn")

    def get_legal_moves(self, board):
        return []

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, "rook")

    def get_legal_moves(self, board):
        return []



