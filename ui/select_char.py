from ui.menu import Menu
from ui import tema

class PilihKarakter(Menu):
    def __init__(self, data_char):
        self.data_char = data_char

        self.list_id = [
            char_id
            for char_id, data in data_char.items()
            if isinstance(data.get("sprite"), dict)
            and "senjata" in data
        ]

        if not self.list_id:
            raise ValueError(
                "Belum ada konfigurasi"
                "Char dan Senjata"
            )

        list_name = [
            data_char[char_id]["name"]
            for char_id in self.list_id
        ]

        super().__init__(
            title="Select Karakter",
            select=list_name,
        )

    def active_select(self):
        return self.list_id[self.index]

    def gambar(self, layar):
        super().gambar(layar)

        char_id = self.active_select()
        data = self.data_char[char_id]

        text = (
            f"HP {data['max_hp']}   "
            f"SPD {data['spd']}   "
            f"ATK {data['atk']}   "
            f"Jeda {data['aspd']} dtk"
        )

        label = self.font_select.render(text, True, tema.TEKS_REDUP)

        layar.blit(
            label,
            label.get_rect(center=(
                layar.get_width()//2,
                round(layar.get_height() / 3 + 65)
            ))
        )
