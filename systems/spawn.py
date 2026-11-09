import random

from enemies.enemy import Musuh

class Spawn:
    def __init__(self, data_musuh, jeda=1.5,limit_musuh = 6, total = None):
        self.data_musuh = data_musuh
        self.jeda = jeda
        self.limit_musuh = limit_musuh
        self.total = total

        self.timer = 0
        self.spawning = 0

    def pos_spawn(self, posisi_player, ukuran_layar):
        lebar, tinggi = ukuran_layar

        # Limit Koordinat
        kiri = posisi_player.x - lebar/2
        kanan= posisi_player.x + lebar/2
        atas = posisi_player.y - tinggi/2
        bawah= posisi_player.y + tinggi/2

        add_pos = random.uniform(80, 160)
        sisi = random.choice(["kiri", "kanan", "bawah", "atas"])
        if sisi == "kiri":
            return(kiri - add_pos, random.uniform(atas,bawah))
        if sisi == "kanan":
            return(kanan + add_pos, random.uniform(atas,bawah))
        if sisi == "atas":
            return(random.uniform(kiri,kanan), atas - add_pos)
        return(random.uniform(kiri,kanan), bawah + add_pos)

    def update(self, timer, player, list_musuh, ukuran_layar):
        self.timer = max(0, self.timer - timer)

        # Kalau ada max total spawn
        if self.total is not None:
            if self.spawning >= self.total:
                return []

        jml_spawn = sum(
            musuh.hp > 0 for musuh in list_musuh
        )

        if jml_spawn >= self.limit_musuh:
            return []

        if self.timer>0:
            return []

        pos = self.pos_spawn(
            player.pos,
            ukuran_layar
        )

        new_musuh = Musuh(self.data_musuh, pos)

        self.spawning += 1
        self.timer = self.jeda

        return [new_musuh]
