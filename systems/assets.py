import json
import pygame
from pathlib import Path

MAIN_FOLDER = Path(__file__).resolve().parent.parent

def read_json(nmfile):
    with open(MAIN_FOLDER / nmfile,"r",encoding = "utf-8") as file:
        return json.load(file)

def load_frame(nmfile, szframe, row, jum, skala=2):
    sprite = pygame.image.load(str(MAIN_FOLDER / nmfile)).convert_alpha()
    lbframe, tgframe = szframe
    list_frame = []

    for col in range(jum):
        area = pygame.Rect(
            col * lbframe,
            row * tgframe,
            lbframe,
            tgframe
        )

        frame = sprite.subsurface(area).copy()
        frame = pygame.transform.scale(frame, (lbframe * skala, tgframe * skala))
        list_frame.append(frame)

    return list_frame

def load_animasi(datasprite):
    list_animasi = {}
    for nmanimasi, list_arah in datasprite["animations"].items():
        list_animasi[nmanimasi] = {}

        for nm_arah, settings in list_arah.items():
            list_frame = load_frame(
                datasprite["file"],
                tuple(datasprite["frame_size"]),
                settings["row"],
                settings["count"],
                datasprite.get("scale", 2)
            )
            list_animasi[nmanimasi][nm_arah] = {
                "frames": list_frame,
                "fps": settings["fps"]
            }

    return list_animasi