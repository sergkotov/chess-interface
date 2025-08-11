from .board import Board
from typing import Optional, Tuple

Position = Tuple[int, int]


class Game:
    def __init__(self):
        self.board = Board()
        self.current_turn = "white"
        self.selected_pos: Optional[Position] = None

    def select(self, pos: Position) -> bool:
        piece = self.board.get_piece(pos)
        if piece and piece.color == self.current_turn:
            # Only select if the piece has at least one legal move
            legal = self.board.get_legal_moves_for_piece(pos)
            if legal:
                self.selected_pos = pos
                return True
        # deselect on invalid selection
        self.selected_pos = None
        return False

    def move(self, dest: Position) -> bool:
        if not self.selected_pos:
            return False
        legal = self.board.get_legal_moves_for_piece(self.selected_pos)
        if dest in legal:
            self.board.move_piece(self.selected_pos, dest)
            self.selected_pos = None
            # switch turn
            self.current_turn = "black" if self.current_turn == "white" else "white"
            return True
        else:
            # invalid move
            return False

    def get_legal_destinations(self, pos):
        return self.board.get_legal_moves_for_piece(pos)

    def is_in_check(self, color: str):
        return self.board.is_in_check(color)
