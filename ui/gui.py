import pygame

TILE_SIZE = 80
BOARD_SIZE = TILE_SIZE * 8
LIGHT_SQUARES_DEFAULT_COLOR = (240, 238, 210)
DARK_SQUARES_DEFAULT_COLOR = (87, 199, 133)


class ChessGUI:
    def __init__(self, game):
        pygame.init()
        self.screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
        pygame.display.set_caption("Chess")
        self.game = game
        self.running = True

        # Load piece images
        self.images = {}
        self._load_images()

    def _load_images(self):
        pieces = ["pawn", "rook", "knight", "bishop", "queen", "king"]
        colors = ["white", "black"]
        for color in colors:
            for piece in pieces:
                path = f"assets/pieces/{color}_{piece}.png"
                self.images[(color, piece)] = pygame.transform.scale(
                    pygame.image.load(path), (TILE_SIZE, TILE_SIZE)
                )

    def draw_board(self):
        colors = [LIGHT_SQUARES_DEFAULT_COLOR, DARK_SQUARES_DEFAULT_COLOR]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                pygame.draw.rect(
                    self.screen, color, pygame.Rect(
                        col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.game.board.grid[row][col]
                if piece:
                    img = self.images[(piece.color, piece.name)]
                    self.screen.blit(img, (col*TILE_SIZE, row*TILE_SIZE))

    def handle_click(self, pos):
        col = pos[0] // TILE_SIZE
        row = pos[1] // TILE_SIZE
        if not self.game.selected_piece:
            self.game.select_piece((row, col))
        else:
            self.game.move_selected_piece((row, col))

    def main_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())

            self.draw_board()
            self.draw_pieces()
            pygame.display.flip()

        pygame.quit()
