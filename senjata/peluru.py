import pygame

class Peluru:
    def __init__(self, posisi, arah, damage, speed, range):
        self.pos = pygame.Vector2(posisi)
        self.arah = pygame.Vector2(arah).normalize()

        self.damage = damage
        self.speed = speed
        self.jarak = range
        self.rad = 5

    def update(self, timer):
        step = min(self.speed * timer, self.jarak)
        self.pos += self.arah * step
        self.jarak -= step

    def hit(self, target):
        jarak = self.pos.distance_to(target.pos)
        return jarak <= self.rad + target.rad

    def gambar(self, layar, cam):
        posisi = self.pos - cam
        area = pygame.Rect(0, 0, self.rad * 2, self.rad * 2)
        area.center = (
            round(posisi.x),
            round(posisi.y)
        )

        if area.colliderect(layar.get_rect()):
            pygame.draw.circle(layar, (141, 216, 255), area.center, self.rad)