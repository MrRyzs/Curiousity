import pygame

from ui import tema

class Menu:
    def __init__(self, title = "Curiousity", select = None):
        self.title = title
        self.select = ["Start", "Quit"] if select is None else select
        self.index = 0

        self.font_title = pygame.font.Font(None, 72)
        self.font_select = pygame.font.Font(None, 36)

    def slide(self, step):
        self.index = (self.index + step) % len(self.select)

    def active_select(self):
        return self.select[self.index]

    def gambar(self, layar):
        layar.fill(tema.LATAR)

        lebar, tinggi = layar.get_size()

        title = self.font_title.render(
            self.title,
            True,
            tema.AKSEN,
        )

        layar.blit(
            title,
            title.get_rect(center=(
                lebar//2, tinggi//3
            ))
        )

        for index, text in enumerate(self.select):
            select = index == self.index
            color = tema.AKSEN if select else tema.TEKS

            label = self.font_select.render(
                f"> {text} <" if select else text,
                True,
                color
            )

            layar.blit(
                label,
                label.get_rect(center=(
                    lebar//2,
                    tinggi//2 + index * 55,
                ))
            )