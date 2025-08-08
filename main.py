from chess.game import Game
from ui.gui import ChessGUI

if __name__ == "__main__":
    game = Game()
    gui = ChessGUI(game)
    gui.main_loop()