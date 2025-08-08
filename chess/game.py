# chess/game.py
class Game:
    def __init__(self):
        from .board import Board
        self.board = Board()
        self.current_turn = "white"
        self.selected_piece = None

    def select_piece(self, pos):
        piece = self.board.get_piece(pos)
        if piece and piece.color == self.current_turn:
            self.selected_piece = piece
            return True
        return False

    def move_selected_piece(self, pos):
        if self.selected_piece:
            self.board.move_piece(self.selected_piece.position, pos)
            self._switch_turn()

    def _switch_turn(self):
        self.current_turn = "black" if self.current_turn == "white" else "white"
        self.selected_piece = None
