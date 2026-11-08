import random
import pygame
from ui import tema
from karakter.karakter import Karakter
from enemies.enemy import Musuh
from systems.assets import(
    read_json,
    load_frame,
    load_animasi
)

# Setup
pygame.init()
width = 1200
height = 675
screen = pygame.display.set_mode((width, height))

# Ambil data player & musuh
char = read_json("data/characters.json")
enemy = read_json("data/enemies.json")
select_char = "test"
select_enemy = "slime"
player = Karakter(char[select_char], (width/2, height/2))
musuh = Musuh(enemy[select_enemy], (width/2, height/2))

# Animasi Player & Musuh
# player_animation = load_frame()
# enemy_animation = load_frame("assets/slime.png", (32,32), 0, 4)

# Set Timer
time = pygame.time.Clock()
waktu_animasi = 0
fps_animasi = 6

# Temporary
# enemy_pos = pygame.Vector2(150, 150)
run = True

# Looping Game
while run:
    timer = min(time.tick(60) / 1000, 0.05)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    if not run:
        break

    button = pygame.key.get_pressed()

    musuh.update(timer, player)
    player.update(timer,button)
    musuh.serang(timer, player)

    cam = player.pos - pygame.Vector2(width/2,height/2)
    
    # Update Animasi
    waktu_animasi += timer
    # index_frame = (int(waktu_animasi * fps_animasi) % len(enemy_animation))
    # enemy_img = enemy_animation[index_frame]

    # UI
    screen.fill(tema.LATAR)
    font_info = pygame.font.Font(None, 28)
    musuh.gambar(screen, cam)
    player.gambar(screen, cam)

    # enemy_cur_pos = enemy_pos - cam
    # enemy_area = enemy_img.get_rect(
    #     center = (
    #         round(enemy_cur_pos.x),
    #         round(enemy_cur_pos.y)
    #     )
    # )

    # if enemy_area.colliderect(screen.get_rect()):
    #     screen.blit(enemy_img,enemy_area)

    text_hp = font_info.render(
        f"HP: {player.hp} / {player.max_hp}",
        True,
        tema.TEKS,
    )

    screen.blit(text_hp, (20,20))

    if player.hp <= 0:
        text_lose = font_info.render(
            "Game Over",
            True,
            tema.DANGER,
        )

        screen.blit(
            text_lose,
            text_lose.get_rect(center=(
                width//2,
                height//2 + 70,
            ))
        )

    pygame.display.flip()

pygame.quit()