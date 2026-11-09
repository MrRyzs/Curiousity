import pygame

from ui import tema
from karakter.karakter import Karakter
from enemies.enemy import Musuh
from senjata.pistol import Pistol
from systems.assets import read_json

class Game:
    def __init__(self):
        pygame.init()

        self.lebar = 1200
        self.tinggi = 675

        self.layar = pygame.display.set_mode((self.lebar, self.tinggi))

        pygame.display.set_caption("Curiousity")

        self.time = pygame.time.Clock()
        self.font_info = pygame.font.Font(None, 28)
        self.run = True

        # Main Data
        self.data_char = read_json("data/characters.json")
        self.data_musuh= read_json("data/enemies.json")

        self.select_char = "test"
        self.select_musuh = "slime"
        self.aim_mode = "auto"

        self.start_game()

    def start_game(self):
        data = self.data_char[self.select_char]

        self.player = Karakter(data, (self.lebar/2, self.tinggi/2))
        self.musuh = Musuh(self.data_musuh[self.select_musuh], (150, 150))

        data_weap = data["senjata"]

        if data_weap["tipe"] == "pistol":
            self.weap = Pistol(
                damage=self.player.atk,
                dur=self.player.aspd,
                range=data_weap["range"],
                speed=data_weap["rof"],
            )
        else:
            raise ValueError(
                f"Tipe Senjata belum ditambahkan: "
                f"{data_weap['tipe']}"
            )

        self.cam = self.player.pos - pygame.Vector2(self.lebar/2, self.tinggi/2)

    def read_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.run = False

    def update(self, timer):
        if self.player.hp <= 0:
            return

        button = pygame.key.get_pressed()

        self.player.update(timer,button)
        self.musuh.update(timer,self.player)
        self.musuh.serang(timer,self.player)

        serang = self.weap.update(timer, self.player, self.musuh,self.aim_mode)
        if serang:
            self.player.serang()

        self.cam = self.player.pos - pygame.Vector2(self.lebar/2, self.tinggi/2)

    def gambar(self):
        self.layar.fill(tema.LATAR)

        self.musuh.gambar(self.layar, self.cam)
        self.player.gambar(self.layar, self.cam)
        self.weap.gambar(self.layar, self.cam)

        hp_txt = self.font_info.render(
            f"HP: {self.player.hp}/{self.player.max_hp}",
            True,
            tema.TEKS
        )

        self.layar.blit(hp_txt, (20,20))

        if self.player.hp <= 0:
            lose_txt = self.font_info.render(
                "Game Over",
                True,
                tema.DANGER
            )

            area = lose_txt.get_rect(center=(
                self.lebar//2,
                self.tinggi//2+70,
            ))

            self.layar.blit(lose_txt,area)

        pygame.display.flip()

    def running(self):
        try:
            while self.run:
                timer = min(self.time.tick(60) / 1000, 0.05)

                self.read_input()

                if not self.run:
                    break

                self.update(timer)
                self.gambar()

        finally:
            pygame.quit()