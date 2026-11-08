import pygame
import json 
import random
from pathlib import Path

pygame.init()

width = 960
height = 540

# Ini setup buat screen/layar
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Curiousity")
state = "menu"
aim_mode = "auto"

font = pygame.font.Font(None, 36)

# Ini setup buat timer nya
time = pygame.time.Clock()

BASE_DIR = Path(__file__).resolve().parent

def load_json(filename):
    with open(BASE_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)

def load_frame(filename, frame_size, row, count, scale=2):
    sheet = pygame.image.load(str(BASE_DIR / filename)).convert_alpha()
    frame_width, frame_height = frame_size
    frames = []

    for col in range(count):
        area = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
        frame = sheet.subsurface(area).copy()
        frame = pygame.transform.scale(frame, (frame_width * scale, frame_height * scale))
        frames.append(frame)

    return frames

# player_idle = load_frame("assets/test.png", (48, 48), 0, 6)
# player_walk = load_frame("assets/test.png", (48, 48), 3, 6)
enemy_idle = load_frame("assets/slime.png", (32, 32), 0, 4)

def load_animations(sprite_data):
    animations = {}
    for animation_name, dir in sprite_data["animations"].items():
        animations[animation_name] = {}
        for dir_name, settings in dir.items():
            frames = load_frame(
                sprite_data["file"],
                tuple(sprite_data["frame_size"]),
                settings["row"],
                settings["count"],
                sprite_data.get("scale", 2),
            )
            animations[animation_name][dir_name] = {
                "frames": frames,
                "fps": settings["fps"],
            }
    return animations

animation_timer = 0
animation_speed = 6

char = load_json("char.json")
enemy = load_json("enemy.json")
select_char = "test"
select_enemy = "slime"
avail_char = [
    char_id
    for char_id, data in char.items() 
    if isinstance(data.get("sprite"), dict)
]
char_index = avail_char.index(select_char)

mode = ["auto", "manual"]
mode_index = mode.index(aim_mode)
status_msg = ""

# Declare Data Player
player_data = char[select_char]

facing_right = True
player_sprite_data = player_data["sprite"]
player_animations = load_animations(player_sprite_data)

pos = pygame.Vector2(width/2, height/2)
facing_dir = pygame.Vector2(1, 0)

speed = player_data["spd"]
radius = player_data["radius"]
max_hp = player_data["max_hp"]
hp = max_hp
dmg = player_data["atk"]
player_clr = tuple(player_data["color"])

# Declare Weapon
bullets = []
bullets_speed = 450
bullets_radius = 5

shot_delay = player_data["atk_spd"]
shot_timer = 0

# Declare Data Musuh
enemy_data = enemy[select_enemy]
enemy_pos = pygame.Vector2(random.randrange(1,width), random.randrange(1,height))
enemy_spd = enemy_data["spd"]
enemy_radius = enemy_data["radius"]
enemy_dmg = enemy_data["atk"]
enemy_max_hp = enemy_data["max_hp"]
enemy_hp = enemy_max_hp
enemy_atk_delay = enemy_data["atk_spd"]
enemy_atk_timer = 0
enemy_clr = tuple(enemy_data["color"])

move = True
kill = 0
surv_time = 0

def apply_char():
    global player_data, player_sprite_data, player_animations
    global speed, radius, max_hp, dmg, player_clr, shot_delay

    player_data = char[select_char]

    speed = player_data["spd"]
    radius = player_data["radius"]
    max_hp = player_data["max_hp"]
    dmg = player_data["atk"]
    player_clr = tuple(player_data["color"])
    shot_delay = player_data["atk_spd"]

    player_sprite_data = player_data["sprite"]
    player_animations = load_animations(player_sprite_data)

def draw_menu(title, lines):
    screen.fill((11, 17, 32))
    title_font = pygame.font.Font(None, 64)
    title_image = title_font.render(
        title, True, (109, 247, 200)
    )

    title_rect = title_image.get_rect(
        center=(width // 2, 110)
    )

    screen.blit(title_image, title_rect)

    line_spacing = 42
    start_y = 280 - (len(lines) - 1) * line_spacing / 2

    for i, text in enumerate(lines):
        image = font.render(text, True, (234, 243, 250))

        rect = image.get_rect(
            center=(
                width // 2,
                round(start_y + i * line_spacing),
            )
        )

        screen.blit(image, rect)


def reset():
    global pos, hp, facing_dir, facing_right, animation_timer
    global enemy_pos, enemy_hp, enemy_atk_timer
    global bullets, shot_timer
    global kill, surv_time

    # Reset Score
    kill = 0
    surv_time = 0
    animation_timer = 0

    # Reset Player
    apply_char( )
    pos = pygame.Vector2(width/2, height/2)
    hp = max_hp
    facing_dir = pygame.Vector2(1, 0)
    facing_right = True

    # Reset Enemy
    enemy_pos = pygame.Vector2(random.randrange(1,width), random.randrange(1,height))
    enemy_hp = enemy_max_hp
    enemy_atk_timer = 0

    # Reset Bullets
    bullets.clear()
    shot_timer = 0

# Gameplay Loop
while move:
    # Set timer/perhitungan waktu
    timer = min(time.tick(60) / 1000, 0.05)

    # Set untuk event game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            move = False

        if event.type == pygame.KEYDOWN:
            #  Main Menu
            if state == "menu":
                if event.key == pygame.K_RETURN:
                    state = "select_char"
                elif event.key == pygame.K_ESCAPE:
                    move = False
            # Chara Select
            elif state == "select_char":
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    char_index = (char_index -1) % len(avail_char)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    char_index = (char_index +1) % len(avail_char)
                elif event.key == pygame.K_RETURN:
                    select_char = avail_char[char_index]
                    state = "select_mode"
                elif event.key == pygame.K_ESCAPE:
                    state = "menu"
            # Select Mode
            elif state == "select_mode":
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    mode_index = (mode_index - 1) % len(mode)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    mode_index = (mode_index + 1) % len(mode)
                elif event.key == pygame.K_RETURN:
                    aim_mode = mode[mode_index]
                    reset()
                    state = "game"
                elif event.key == pygame.K_ESCAPE:
                    state = "select_char"
            # Game Over
            elif state == "gameover":
                if event.key == pygame.K_RETURN:
                    reset()
                    state = "game"
                elif event.key == pygame.K_c:
                    state = "select_char"
                elif event.key == pygame.K_ESCAPE:
                    state = "menu"

            # if state == "menu":
            #     if event.key == pygame.K_1:
            #         aim_mode = "auto"
            #     elif event.key == pygame.K_2:
            #         aim_mode = "manual"
            #     elif event.key == pygame.K_RETURN:
            #         reset()
            #         state = "game"

            # elif state == "gameover":
            #     if event.key == pygame.K_RETURN:
            #         reset()
            #         state = "game"

            #     elif event.key == pygame.K_ESCAPE:
            #             state = "menu"

    if not move:
        break

    # # Set up Main Menu
    # if state == "menu":
    #     screen.fill((11,17,32))

    #     menu_lines = [
    #         "Curiousity",
    #         "1. Auto Aim",
    #         "2. Manual Aim",
    #         f"Current Aim Mode: {aim_mode}",
    #         "Press Enter to Start"
    #     ]

    #     for i, text in enumerate(menu_lines):
    #         label = font.render(text, True, (234, 243, 250))
    #         screen.blit(label, (100, 100 + i * 55))

    #     pygame.display.flip()
    #     continue

    if state == "menu":
        draw_menu("CURIOUSITY", [
            "Arena Survival",
            "ENTER - Mulai",
            "ESC - Keluar",
        ])

    elif state == "select_char":
        preview_id = avail_char[char_index]
        preview_data = char[preview_id]

        draw_menu("SELECT CHARACTER", [
            f"< {preview_data['name']} >",
            f"HP: {preview_data['max_hp']}   SPD: {preview_data['spd']}",
            f"ATK: {preview_data['atk']}   Jeda: {preview_data['atk_spd']} dtk",
            "A / D atau panah - Ganti karakter",
            "ENTER - Lanjut",
            "ESC - Kembali",
        ])

    elif state == "select_mode":
        preview_mode = mode[mode_index]

        if preview_mode == "auto":
            description = "Tembakan otomatis membidik musuh"
        else:
            description = "Tembakan mengikuti arah gerakan terakhir"

        draw_menu("SELECT MODE", [
            f"< {preview_mode.upper()} >",
            description,
            "A / D atau panah - Ganti mode",
            "ENTER - Main",
            "ESC - Kembali",
        ])

    elif state == "gameover":
        minutes = int(surv_time) // 60
        seconds = int(surv_time) % 60

        draw_menu("GAME OVER", [
            f"Karakter: {player_data['name']}   Mode: {aim_mode.upper()}",
            f"Kill: {kill}   Waktu: {minutes:02d}:{seconds:02d}",
            "ENTER - Main lagi",
            "C - Pilih karakter",
            "ESC - Main menu",
        ])

    # Selama halaman menu terbuka, lewati gameplay.
    if state != "game":
        pygame.display.flip()
        continue

    # if state == "gameover":
    #     screen.fill((11,17,32))

    #     gameover_lines = [
    #         "Game Over",
    #         f"Kill: {kill} | Time Survived: {int(surv_time // 60):02}:{int(surv_time % 60):02}",
    #         "Tekan Enter Untuk Mulai Ulang",
    #         "Tekan Escape Untuk Kembali ke Menu"
    #     ]

    #     line_spacing = 45
    #     start_y = height / 2 - (len(gameover_lines) - 1) * line_spacing / 2

    #     for i, text in enumerate(gameover_lines):
    #         label = font.render(text, True, (234, 243, 250))
    #         label_rect = label.get_rect(center=(width // 2, round(start_y + i * line_spacing)))
    #         screen.blit(label, label_rect)

    #     pygame.display.flip()
    #     continue

    
    surv_time += timer
    animation_timer += timer

    # Setup agar inputan keyboard terbaca & Player Movement
    button = pygame.key.get_pressed()

    dir = pygame.Vector2(
        int(button[pygame.K_d] or button[pygame.K_RIGHT])
        - int(button[pygame.K_a] or button[pygame.K_LEFT]),
        int(button[pygame.K_s] or button[pygame.K_DOWN]) 
        - int(button[pygame.K_w] or button[pygame.K_UP])
    )

    is_move = dir.length_squared() > 0

    if is_move:
        dir = dir.normalize()
        facing_dir = dir.copy()

        if dir.x > 0:
            facing_right = True
        elif dir.x < 0:
            facing_right = False

    pos += dir * speed * timer

    # Menjaga pemain tetap berada di dalam jendela.
    pos.x = max(radius, min(width - radius, pos.x))
    pos.y = max(radius, min(height - radius, pos.y))

    # Enemy Movement
    enemy_dir = pos - enemy_pos

    if enemy_dir.length_squared() > 0:
        enemy_dir = enemy_dir.normalize()

    enemy_pos += enemy_dir * enemy_spd * timer

    # Logic Atk Player
    shot_timer -= timer

    if shot_timer <= 0:
        # bullets.append({
        #     "pos": pos.copy(),
        #     "dir": facing_dir.copy(),
        # })
        if aim_mode == "auto":
            shot_dir = enemy_pos - pos
        else:
            shot_dir = facing_dir.copy()

        if shot_dir.length_squared() > 0:
            shot_dir = shot_dir.normalize()
            bullets.append({
                "pos": pos.copy(),
                "dir": shot_dir.copy(),
            })
            shot_timer = shot_delay

    # Attack Logic Player
    for bullet in bullets[:]:
        bullet["pos"]+=(
            bullet["dir"] * bullets_speed * timer
        )

        dist = bullet["pos"].distance_to(enemy_pos)

        if dist <= bullets_radius + enemy_radius:
            enemy_hp -= dmg
            bullets.remove(bullet)

            if enemy_hp <= 0:
                kill += 1
                enemy_pos = pygame.Vector2(random.randrange(1, width), random.randrange(1, height))
                enemy_hp = enemy_max_hp
                enemy_atk_timer = 0

                break

    # bullets = [
    #     bullet for bullet in bullets
    #     if 0<= bullet["pos"].x <= width
    #     and 0<= bullet["pos"].y <= height
    # ]

    # Enemy Attack Logic
    enemy_atk_timer = max(0, enemy_atk_timer - timer)

    player_dist = enemy_pos.distance_to(pos)
    touching = player_dist <= radius + enemy_radius

    if touching and enemy_atk_timer <= 0:
        hp = max(0, hp - enemy_dmg)
        enemy_atk_timer = enemy_atk_delay

        if hp <= 0:
            state = "gameover"

    # Set Screen
    screen.fill((11,17,32))
    # Player
    # Fungsi lama 
    # if is_move:
    #     player_frame = player_walk
    #     player_animation_speed = 12
    # else:
    #     player_frame = player_idle
    #     player_animation_speed = 6

    # player_frame_index = int(animation_timer * player_animation_speed) % len(player_frame)
    # player_img = player_frame[player_frame_index]
    
    ani_name = "walk" if is_move else "idle"
    animation = player_animations[ani_name]["side"]
    frames = animation["frames"]
    frame_index = (int(animation_timer * animation["fps"])% len(frames))
    player_img = frames[frame_index]
    right_face = (player_sprite_data.get("side_faces", "right") == "right")
    if facing_right != right_face:
        player_img = pygame.transform.flip(player_img,True,False)

    player_rect = player_img.get_rect(center=(round(pos.x), round(pos.y)))
    screen.blit(player_img, player_rect)

    # player_frame_index = int(animation_timer * animation_speed) % len(player_idle)
    # player_img = player_idle[player_frame_index]
    # player_rect = player_img.get_rect(center=(round(pos.x), round(pos.y)))
    # screen.blit(player_img, player_rect)
    # pygame.draw.circle(
    #     screen,
    #     (player_clr),
    #     (round(pos.x), round(pos.y)),
    #     radius,
    # )

    # Enemy
    enemy_frame_index = int(animation_timer * animation_speed) % len(enemy_idle)
    enemy_img = enemy_idle[enemy_frame_index]
    enemy_rect = enemy_img.get_rect(center=(round(enemy_pos.x), round(enemy_pos.y)))
    screen.blit(enemy_img, enemy_rect)
    # pygame.draw.circle(
    #     screen,
    #     (enemy_clr),
    #     (round(enemy_pos.x), round(enemy_pos.y)),
    #     enemy_radius,
    # )

    # Gambar semua peluru
    for bullet in bullets:
        pygame.draw.circle(
            screen,
            (255, 220, 100),
            (
                round(bullet["pos"].x),
                round(bullet["pos"].y),
            ),
            bullets_radius,
        )

    bar_width = 40
    bar_height = 6
    bar_x = round(enemy_pos.x - bar_width / 2)
    bar_y = round(enemy_pos.y - enemy_radius - 14)
    # Bar Darah Player
    hp_label = font.render(f"HP: {hp}/{max_hp}", True, (234, 243, 250))
    screen.blit(hp_label, (10, 10))

    bar_xp = round(pos.x - bar_width / 2)
    bar_yp = round(pos.y - radius - 14)
    # Gambar Bar Darah Player
    pygame.draw.rect(
        screen,
        (60, 60, 75),
        (bar_xp, bar_yp, bar_width, bar_height),
    )
    # Sisa Darah Player
    hp_width = round(bar_width * (hp / max_hp))
    pygame.draw.rect(
        screen,
        (player_clr),
        (bar_xp, bar_yp, bar_width * (hp / max_hp), bar_height),
    )

    # Gambar Bar Darah Musuh
    pygame.draw.rect(
        screen,
        (60, 60, 75),
        (bar_x, bar_y, bar_width, bar_height),
    )
    # Sisa Darah Musuh
    hp_width = round(bar_width * (enemy_hp / enemy_max_hp))
    pygame.draw.rect(
        screen,
        (enemy_clr),
        (bar_x, bar_y, bar_width * (enemy_hp / enemy_max_hp), bar_height),
    )

    mins = int(surv_time // 60)
    secs = int(surv_time % 60)

    stats_label = font.render(f"Kill: {kill} | Time Survived: {mins:02}:{secs:02}", True, (234, 243, 250))
    screen.blit(stats_label, (10, 40))

    pygame.display.flip()

pygame.quit()