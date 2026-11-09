import pygame

from systems.assets import load_animasi

class Musuh:
    def __init__(self, data, posisi_awal):
        self.nama = data["name"]
        self.pos = pygame.Vector2(posisi_awal)

        self.max_hp = data["max_hp"]
        self.hp = self.max_hp

        self.spd = data["spd"]
        self.rad = data["rad"]
        self.atk = data["atk"]
        self.aspd = data["aspd"]
        self.timer_atk = 0

        self.hadap_kanan = True

        self.sprite = data["sprite"]
        self.animasi = load_animasi(self.sprite)

        self.nm_animasi = "idle"
        self.time_animasi = 0

    def update(self, timer, target):
        if self.hp <= 0:
            return

        # Ngejar Player
        sel = target.pos - self.pos
        jar = sel.length()

        # Berhenti Ngejar kalo udh sampe Player
        jar_stop = self.rad + target.rad
        moving = jar > jar_stop

        if moving:
            arah = sel.normalize()

            step = min(self.spd * timer, jar - jar_stop)
            self.pos += arah * step

            if arah.x > 0:
                self.hadap_kanan = True
            elif arah.x < 0:
                self.hadap_kanan = False

        kondisi = "walk" if moving else "idle"
        if kondisi != self.nm_animasi:
            self.nm_animasi = kondisi
            self.time_animasi = 0

        self.time_animasi += timer

    def gambar(self, layar, cam):
        if self.hp <= 0:
            return

        animasi = self.animasi[self.nm_animasi]["side"]
        list_frame = animasi['frames']

        index = (int(self.time_animasi * animasi["fps"]) % len(list_frame))
        gambar = list_frame[index]

        arah_kanan = (self.sprite.get("side_faces", "right") == "right")
        if self.hadap_kanan != arah_kanan:
            gambar = pygame.transform.flip(gambar, True, False)

        posisi_layar = self.pos - cam

        area = gambar.get_rect(center=(
            round(posisi_layar.x),
            round(posisi_layar.y)
        ))

        if area.colliderect(layar.get_rect()):
            layar.blit(gambar, area)

    def terserang(self, dmg):
        self.hp = max(0, self.hp - dmg)

    def serang(self, timer, target):
        self.timer_atk = max(0, self.timer_atk - timer)
        if self.hp <= 0 or target.hp <= 0:
            return

        jar = self.pos.distance_to(target.pos)

        rad = self.rad + target.rad + 0.5

        if jar <= rad and self.timer_atk <= 0:
            target.terserang(self.atk)
            self.timer_atk = self.aspd
