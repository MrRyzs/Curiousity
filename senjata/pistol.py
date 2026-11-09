from senjata.peluru import Peluru

class Pistol:
    def __init__(self, damage, dur, range = 600, speed = 450):
        self.damage = damage
        self.dur = dur
        self.range = range
        self.speed = speed

        self.timer = 0
        self.list_peluru = []

    def update(self, timer, owner, target, mode):
        self.timer = max(0, self.timer - timer)

        # Movement Peluru
        for peluru in self.list_peluru[:]:
            peluru.update(timer)

            if target.hp > 0 and peluru.hit(target):
                target.terserang(peluru.damage)
                self.list_peluru.remove(peluru)

            elif peluru.jarak <= 0:
                self.list_peluru.remove(peluru)

        # Atk Cooldown dan Logic jika user kalah
        if owner.hp <= 0 or self.timer > 0:
            return

        if mode == "auto":
            if target.hp <= 0:
                return
            
            diff = target.pos - owner.pos

            if diff.length() > self.range:
                return

            arah = diff

        else:
            arah = owner.hadap_ke.copy()

        if arah.length_squared() == 0:
            return

        new_peluru = Peluru(
            owner.pos,
            arah,
            self.damage,
            self.speed,
            self.range
        )

        self.list_peluru.append(new_peluru)
        self.timer = self.dur
        
        return True

    def gambar(self, layar, cam):
        for peluru in self.list_peluru:
            peluru.gambar(layar, cam)
