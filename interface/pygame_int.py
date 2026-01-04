import pygame
from interface.carte_charge import CardLoader
from network.client import GameClient

WIDTH, HEIGHT = 1200, 700
BG_COLOR = (20, 120, 20)

class PygameUI:
    def __init__(self, host_ip):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Rumicube LAN")

        self.clock = pygame.time.Clock()
        self.running = True

        self.client = GameClient(host_ip)
        self.state = None

        self.loader = CardLoader()

    def draw_hand(self, hand):
        x = 50
        y = HEIGHT - 150

        for tile in hand:
            img = self.loader.get(tile["name"])
            self.screen.blit(img, (x, y))
            x += 90

    def run(self):
        self.state = self.client.send({"action": "draw"})

        while self.running:
            self.clock.tick(60)
            self.screen.fill(BG_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if self.state:
                player_hand = self.state["players"][1]["hand"]
                self.draw_hand(player_hand)

            pygame.display.flip()

        pygame.quit()
