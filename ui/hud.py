import pygame

from ui import tema

class HUD:
    def __init__(self, lebar):
        self.font = pygame.font.Font(None, 22)
        self.heading = pygame.font.Font(None, 28)

        self.pause_button = pygame.Rect(lebar - 112, 20, 92, 38)

        self.ikon = None

    def set_char(self, player):
        frame = player.animasi["idle"]["side"]["frames"][0]

        area = frame.get_bounding_rect()
        gambar = frame.subsurface(area).copy()
        skala = min(
            44/gambar.get_width(),
            54/gambar.get_height(),
        )

        self.ikon = pygame.transform.scale(gambar,(
            max(1, round(gambar.get_width()*skala)),
            max(1, round(gambar.get_height()*skala)),
        ))

    def teks(self, layar, isi, posisi, tengah = False, besar = False):
        font = self.heading if besar else self.font
        gambar= font.render(isi, True, tema.TEKS)

        area = gambar.get_rect()

        if tengah:
            area.center = posisi
        else:
            area.topleft = posisi

        layar.blit(gambar, area)

    def bar(self, layar, area, nilai, maks, color, teks):
        rasio = max(0, min(1, nilai / maks))

        titik = [
            (area.left + 7, area.top),
            (area.right, area.top),
            (area.right - 7, area.bottom),
            (area.left, area.bottom),
        ]

        pygame.draw.polygon(layar, tema.PANEL_SOROT, titik)

        # Logic Perhitungan Darah & XP biar smooth
        batas_a = layar.get_clip()
        batas_t = pygame.Rect(
            area.left,
            area.top,
            round(area.width * rasio),
            area.height
        )
        layar.set_clip(batas_a.clip(batas_t))
        pygame.draw.polygon(layar, color, titik)
        layar.set_clip(batas_a)

        pygame.draw.polygon(layar, tema.AKSEN_TERANG, titik, width=1)

        # Siluet angka di bar
        siluet = self.font.render(teks, True, tema.LATAR)
        posisi = siluet.get_rect(center=area.center)
        layar.blit(siluet, posisi.move(1,1))

        self.teks(layar,teks,area.center,tengah=True)

    def gambar(self, layar, player, xp, xp_limit, level, skor, time, stage):
        lebar = layar.get_width()
        # pygame.draw.rect(layar, tema.PANEL, (0,0,lebar,104))
        # pygame.draw.line(layar, tema.BINGKAI, (0,103), (lebar,103))

        # Ikon & Nama 
        area_ikon = pygame.Rect(16,18,58,68)
        pygame.draw.rect(layar, tema.LATAR, area_ikon)
        pygame.draw.rect(layar, tema.BINGKAI, area_ikon, width=1)

        if self.ikon is not None:
            layar.blit(self.ikon, self.ikon.get_rect(center=area_ikon.center))

        self.teks(
            layar,
            f"{player.nama} | Lv. {level}",
            (86,15),
        )

        # HP & XP
        rasio_hp = player.hp / player.max_hp
        if rasio_hp > 0.5:
            hp_color = tema.HP
        elif rasio_hp > 0.25:
            hp_color = tema.WARNING
        else:
            hp_color = tema.DANGER

        self.bar(
            layar,
            pygame.Rect(86, 39, 230, 20),
            player.hp,
            player.max_hp,
            hp_color,
            f"HP {player.hp} / {player.max_hp}"
        ) 

        self.bar(
            layar,
            pygame.Rect(86, 64, 230, 18),
            xp,
            xp_limit,
            tema.XP,
            f"XP {xp} / {xp_limit}"
        ) 

        # Info
        men= int(time) // 60
        det= int(time) % 60

        self.teks(
            layar, 
            f"Skor {skor}",
            (lebar//2, 22),
            tengah=True
        ) 

        self.teks(
            layar, 
            f"{men:02d}:{det:02d}",
            (lebar//2, 49),
            tengah=True,
            besar=True,
        ) 

        self.teks(
            layar, 
            f"Stage {stage}",
            (lebar//2, 78),
            tengah=True
        ) 

        # Pause
        pause = self.pause_button.collidepoint(pygame.mouse.get_pos())
        color = tema.PANEL_SOROT if pause else tema.LATAR

        pygame.draw.rect(layar, color, self.pause_button)
        pygame.draw.rect(layar, tema.BINGKAI, self.pause_button, width=1)

        self.teks(
            layar,
            "PAUSE",
            self.pause_button.center,
            tengah=True,
        )