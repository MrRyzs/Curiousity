from senjata.peluru import Peluru

class Pistol:
    def __init__(self, damage, dur, range = 600, speed = 450):
        self.damage = damage
        self.dur = dur
        self.range = range
        self.speed = speed

        self.timer = 0
        self.list_peluru = []

    def update(self, timer, player, list_musuh, mode):
        self.timer = max(0, self.timer - timer)

        # Movement Peluru
        for peluru in self.list_peluru[:]:
            peluru.update(timer)

            hit_musuh = False

            for musuh in list_musuh:
                if musuh.hp <= 0:
                    continue

                if peluru.hit(musuh):
                    musuh.terserang(peluru.damage)
                    hit_musuh = True
                    break

            if hit_musuh or peluru.jarak <= 0:
                self.list_peluru.remove(peluru)

        # Atk Cooldown dan Logic jika user kalah
        if player.hp <= 0 or self.timer > 0:
            return

        if mode == "auto":
            # Set auto lock
            target = None
            closest_musuh = float("inf")

            for musuh in list_musuh:
                if musuh.hp <= 0:
                    continue
            
                diff = player.pos.distance_to(musuh.pos)

                if diff <= self.range and diff < closest_musuh:
                    target = musuh
                    closest_musuh = diff

            if target is None:
                return

            arah = target.pos - player.pos
        else:
            arah = player.hadap_ke.copy()

        if arah.length_squared() == 0:
            return

        new_peluru = Peluru(
            player.pos,
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
