import pygame

from ui import tema
from ui.menu import Menu
from ui.hud import HUD
from ui.select_char import PilihKarakter
from karakter.karakter import Karakter
from enemies.enemy import Musuh
from senjata.pistol import Pistol
from systems.assets import read_json
from systems.spawn import Spawn

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
        self.game_mode = "stage"

        self.hud = HUD(self.lebar)

        self.start_game()
        self.menu = Menu(
            select=["Start", "Settings", "Quit"]
        )
        self.menu_char = PilihKarakter(self.data_char)
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
        self.menu_pause = Menu(
            title="Pause",
            select=["Continue", "Retry", "Main Menu"],
        )
        self.condition = "main_menu"

    def start_game(self):
        data = self.data_char[self.select_char]

        # spawn_musuh = [(150,150),(950,150),(600,650)]
        self.list_musuh = []

        ttl_musuh = 20 if self.game_mode == "stage" else None

        self.spawn = Spawn(
            data_musuh=self.data_musuh[self.select_musuh],
            jeda=1.5,
            limit_musuh=6,
            total=ttl_musuh,
        )

        self.player = Karakter(data, (self.lebar/2, self.tinggi/2))
        self.list_musuh = [
            # Musuh(self.data_musuh[self.select_musuh], spawn) 
            # for spawn in spawn_musuh 
        ]

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

        self.hud.set_char(self.player)
        self.xp = 0
        self.xp_limit = 20
        self.level = 1

        self.skor = 0
        self.timer = 0
        self.stage = 1

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
                    if event.key in (pygame.K_ESCAPE, pygame.K_p):
                        self.menu_pause.index = 0
                        self.condition = "pause"

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
                            self.start_game()
                            self.condition = "playing"
                        elif select == "Select Character":
                            self.condition = "select_char"
                        elif select == "Main Menu":
                            self.condition = "main_menu"
                    elif event.key == pygame.K_ESCAPE:
                        self.condition = "main_menu"

                elif self.condition == "pause":
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.menu_pause.slide(-1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.menu_pause.slide(1)
                    elif event.key == pygame.K_RETURN:
                        select = self.menu_pause.active_select()
                        if select == "Continue":
                            self.condition = "playing"
                        elif select == "Retry":
                            self.start_game()
                            self.condition = "playing"
                        else:
                            self.condition = "main_menu"
                    elif event.key in (pygame.K_ESCAPE, pygame.K_p):
                        self.condition = "playing"
                    
                
                # if event.key == pygame.K_ESCAPE:
                #     self.run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if(
                    self.condition == "playing"
                    and event.button == 1
                    and self.hud.pause_button.collidepoint(event.pos)
                ):
                    self.menu_pause.index = 0
                    self.condition = "pause"

    def update(self, timer):
        if self.condition != "playing":
            return

        if self.player.hp <= 0:
            self.menu_gameover.index = 0
            self.condition = "gameover"
            return

        self.timer += timer

        button = pygame.key.get_pressed()

        self.player.update(timer,button)

        new_musuh = self.spawn.update(
            timer,
            self.player,
            self.list_musuh,
            (self.lebar,self.tinggi),
        )

        self.list_musuh.extend(new_musuh)

        for musuh in self.list_musuh:
            musuh.update(timer,self.player)
            musuh.serang(timer,self.player)

        ttl_hp_lama = sum(
            musuh.hp > 0
            for musuh in self.list_musuh
        )

        serang = self.weap.update(timer, self.player, self.list_musuh, self.aim_mode)

        if serang:
            self.player.serang()

        ttl_hp_baru = sum(
            musuh.hp > 0
            for musuh in self.list_musuh
        )

        self.skor += (ttl_hp_lama - ttl_hp_baru)

        # Hapus musuh yang sudah ded
        self.list_musuh = [
            musuh
            for musuh in self.list_musuh
            if musuh.hp > 0
        ]

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

        if self.condition == "pause":
            self.menu_pause.gambar(self.layar)
            pygame.display.flip()
            return

        # Gameplay 
        self.layar.fill(tema.LATAR) 

        for musuh in self.list_musuh: musuh.gambar(self.layar, self.cam)
        self.player.gambar(self.layar, self.cam)
        self.weap.gambar(self.layar, self.cam)

        stage = (self.stage if self.game_mode == "stage" else "-")

        self.hud.gambar(
            self.layar,
            self.player,
            self.xp,
            self.xp_limit,
            self.level,
            self.skor,
            self.timer,
            stage,
        )

        kuota = (
            str(self.spawn.total)
            if self.spawn.total is not None
            else "♾️"
        )

        spawn_txt = self.font_info.render(
            f"Musuh saat ini : {len(self.list_musuh)} | "
            f"Total Musuh : {self.spawn.spawning}/{kuota}",
            True,
            tema.TEKS_REDUP
        )

        self.layar.blit(spawn_txt, (20,115))

        # hp_txt = self.font_info.render(
        #     f"HP: {self.player.hp}/{self.player.max_hp}",
        #     True,
        #     tema.TEKS
        # )

        # mode_txt = self.font_info.render(
        #     f"Mode: {self.game_mode.upper()} | "
        #     f"Aim : {self.aim_mode.upper()}",
        #     True,
        #     tema.TEKS_REDUP
        # )

        # self.layar.blit(hp_txt, (20,20))
        # self.layar.blit(mode_txt, (20,50))

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
