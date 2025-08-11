import pygame
from chess.game import Game

TILE_SIZE = 80
BOARD_SIZE = TILE_SIZE * 8
LIGHT_SQUARES_DEFAULT_COLOR = (240, 238, 210)
DARK_SQUARES_DEFAULT_COLOR = (87, 199, 133)


class ChessGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
        pygame.display.set_caption("Chess (hotseat)")
        self.clock = pygame.time.Clock()
        self.game = Game()
        self.running = True
        self.images = {}
        self._load_images()
        self.font = pygame.font.SysFont(None, 24)

    def _load_images(self):
        pieces = ["pawn", "rook", "knight", "bishop", "queen", "king"]
        colors = ["white", "black"]
        for color in colors:
            for piece in pieces:
                path = f"assets/pieces/{color}_{piece}.png"
                try:
                    img = pygame.image.load(path).convert_alpha()
                    img = pygame.transform.smoothscale(
                        img, (TILE_SIZE, TILE_SIZE))
                    self.images[(color, piece)] = img
                except Exception as e:
                    # Missing image fallback: simple colored circle
                    surf = pygame.Surface(
                        (TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                    pygame.draw.circle(
                        surf, (0, 0, 0), (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//3, 2)
                    self.images[(color, piece)] = surf

    def draw_board(self):
        light = LIGHT_SQUARES_DEFAULT_COLOR
        dark = DARK_SQUARES_DEFAULT_COLOR
        for r in range(8):
            for c in range(8):
                color = light if (r+c) % 2 == 0 else dark
                pygame.draw.rect(
                    self.screen, color, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def draw_pieces(self):
        for r in range(8):
            for c in range(8):
                p = self.game.board.get_piece((r, c))
                if p:
                    img = self.images.get((p.color, p.name))
                    if img:
                        self.screen.blit(img, (c*TILE_SIZE, r*TILE_SIZE))

    def highlight_square(self, pos, color=(0, 255, 0, 120)):
        s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        s.fill(color)
        self.screen.blit(s, (pos[1]*TILE_SIZE, pos[0]*TILE_SIZE))

    def draw_ui(self):
        text = f"Turn: {self.game.current_turn.capitalize()}"
        img = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(img, (5, 5))

    def pixel_to_board(self, px):
        x, y = px
        col = x // TILE_SIZE
        row = y // TILE_SIZE
        return (row, col)

    def main_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    bpos = self.pixel_to_board(pygame.mouse.get_pos())
                    # select if selecting your piece
                    if self.game.selected_pos is None:
                        self.game.select(bpos)
                    else:
                        moved = self.game.move(bpos)
                        if not moved:
                            # try selecting a different piece (if valid)
                            self.game.select(bpos)

            # draw
            self.draw_board()
            # highlight selected
            if self.game.selected_pos:
                self.highlight_square(
                    self.game.selected_pos, color=(50, 200, 50, 80))
                # highlight legal destinations
                dests = self.game.get_legal_destinations(
                    self.game.selected_pos)
                for d in dests:
                    self.highlight_square(d, color=(50, 50, 200, 80))
            self.draw_pieces()
            self.draw_ui()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
