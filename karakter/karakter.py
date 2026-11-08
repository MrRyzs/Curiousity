import pygame
from systems.assets import load_animasi

class Karakter:
    def __init__(self,data,posisi_awal):
        # Data Player
        self.nama = data["name"]
        self.pos = pygame.Vector2(posisi_awal)

        self.max_hp = data["max_hp"]
        self.hp = self.max_hp

        self.spd = data["spd"]
        self.rad = data["rad"]
        self.atk = data["atk"]
        self.aspd = data["aspd"]

        # Setting arah movement
        self.hadap_ke = pygame.Vector2(1,0)
        self.hadap_kanan = True

        # Animasi
        self.sprite = data["sprite"]
        self.animasi = load_animasi(self.sprite)

        self.nm_animasi = "idle"
        self.time_animasi = 0

    def update(self, timer, button):
        arah = pygame.Vector2(
            int(button[pygame.K_d] or button[pygame.K_RIGHT])
            - int(button[pygame.K_a] or button[pygame.K_LEFT]),
            int(button[pygame.K_s] or button[pygame.K_DOWN])
            - int(button[pygame.K_w] or button[pygame.K_UP])
        )

        moving = arah.length_squared() > 0

        if moving:
            arah = arah.normalize()
            self.hadap_ke = arah.copy()

            if arah.x > 0:
                self.hadap_kanan = True
            if arah.x < 0:
                self.hadap_kanan = False

        self.pos += arah * self.spd * timer

        # Logic Animasi, saat ini masih temporary
        kondisi = "walk" if moving else "idle"

        if kondisi != self.nm_animasi:
            self.nm_animasi = kondisi
            self.time_animasi = 0

        self.time_animasi += timer

    def gambar(self, layar, cam):
        animasi = self.animasi[self.nm_animasi]["side"]
        list_frame = animasi["frames"]

        index = (int(self.time_animasi * animasi["fps"]) % len(list_frame))
        gambar = list_frame[index]
        arah_kanan = (self.sprite.get("side_faces", "right") == "right")
        
        if self.hadap_kanan != arah_kanan:
            gambar = pygame.transform.flip(gambar,True,False)

        posisi_layar = self.pos - cam

        area = gambar.get_rect(center=(
            round(posisi_layar.x),
            round(posisi_layar.y)
        ))

        if area.colliderect(layar.get_rect()):
            layar.blit(gambar, area)

    def terserang(self, dmg):
        self.hp = max(0, self.hp - dmg)