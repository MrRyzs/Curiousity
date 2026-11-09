import pygame

from ui import tema
from ui.menu import Menu
from ui.select_char import PilihKarakter
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
        self.menu = Menu(
            select=["Start", "Settings", "Quit"]
        )
        self.menu_char = PilihKarakter(self.data_char)
        self.game_mode = "stage"
        self.menu_mode = Menu(
            title="Pilih Mode",
            select=["Stage", "Endless"]
        )
        self.settings = Menu(
            title="Settings",
            select=["Auto","Manual","Back"],
        )
        self.menu_gameover = Menu(
            title="Game Over",
            select=["Try Again","Select Character", "Main Menu"],
        )
        self.condition = "main_menu"

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
                if self.condition == "main_menu":
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.menu.slide(-1)

                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.menu.slide(1)

                    elif event.key == pygame.K_RETURN:
                        select = self.menu.active_select()
                        if select == "Start":
                            self.condition = "select_char"

                        elif select == "Settings":
                            self.settings.index=(
                                0 if self.aim_mode == "auto" else 1
                            )
                            self.condition = "settings"

                        elif select == "Quit":
                            self.run = False

                    elif event.key == pygame.K_ESCAPE:
                        self.run = False

                elif self.condition == "playing":
                    if event.key == pygame.K_ESCAPE:
                        self.condition = "main_menu"

                elif self.condition == "select_char":
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.menu_char.slide(-1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.menu_char.slide(1)
                    elif event.key == pygame.K_RETURN:
                        self.select_char = self.menu_char.active_select()
                        self.condition = "select_mode"
                    elif event.key == pygame.K_ESCAPE:
                        self.condition = "main_menu"

                elif self.condition == "select_mode":
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.menu_mode.slide(-1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.menu_mode.slide(1)
                    elif event.key == pygame.K_RETURN:
                        select = self.menu_mode.active_select()
                        self.game_mode = (
                            "stage" if select == "Stage" else "endless"
                        )
                        self.start_game()
                        self.condition = "playing"
                    elif event.key == pygame.K_ESCAPE:
                        self.condition = "select_char"

                elif self.condition == "settings":
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.settings.slide(-1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.settings.slide(1)
                    elif event.key == pygame.K_RETURN:
                        select = self.settings.active_select()
                        if select == "Auto":
                            self.aim_mode = "auto"
                        elif select == "Manual":
                            self.aim_mode = "manual"
                        self.condition = "main_menu"
                    elif event.key == pygame.K_ESCAPE:
                        self.condition = "main_menu"

                elif self.condition == "gameover":
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.menu_gameover.slide(-1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.menu_gameover.slide(1)
                    elif event.key == pygame.K_RETURN:
                        select = self.menu_gameover.active_select()
                        if select == "Try Again":
                            self.condition = "auto"
                        elif select == "Select Character":
                            self.condition = "manual"
                        elif select == "Main Menu":
                            self.condition = "main_menu"
                    elif event.key == pygame.K_ESCAPE:
                        self.condition = "main_menu"
                
                # if event.key == pygame.K_ESCAPE:
                #     self.run = False

    def update(self, timer):
        if self.condition != "playing":
            return

        if self.player.hp <= 0:
            self.menu_gameover.index = 0
            self.condition = "gameover"
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
        if self.condition == "main_menu":
            self.menu.gambar(self.layar)
            pygame.display.flip()
            return

        if self.condition == "select_char":
            self.menu_char.gambar(self.layar)
            pygame.display.flip()
            return

        if self.condition == "select_mode":
            self.menu_mode.gambar(self.layar)
            pygame.display.flip()
            return

        if self.condition == "settings":
            self.settings.title = (f"Settings - Aim : {self.aim_mode.upper()}")
            self.settings.gambar(self.layar)
            pygame.display.flip()
            return

        if self.condition == "gameover":
            self.menu_gameover.gambar(self.layar)
            pygame.display.flip()
            return

        # Gameplay 
        self.layar.fill(tema.LATAR) 

        self.musuh.gambar(self.layar, self.cam)
        self.player.gambar(self.layar, self.cam)
        self.weap.gambar(self.layar, self.cam)

        hp_txt = self.font_info.render(
            f"HP: {self.player.hp}/{self.player.max_hp}",
            True,
            tema.TEKS
        )

        mode_txt = self.font_info.render(
            f"Mode: {self.game_mode.upper()} | "
            f"Aim : {self.aim_mode.upper()}",
            True,
            tema.TEKS_REDUP
        )

        self.layar.blit(hp_txt, (20,20))
        self.layar.blit(mode_txt, (20,50))

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
