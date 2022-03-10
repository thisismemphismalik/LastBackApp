import json
import os
from hashlib import sha256

from PIL import Image, ImageOps
from plyer import filechooser


def color(name):
    base = {
        "black": [0, 0, 0, 1],
        "blue": [0, 0, 1, 1],
        "green": [0, 1, 0, 1],
        "red": [1, 0, 0, 1],
        "sky-blue": [0, 1, 1, 1],
        "violet": [1, 0, 1, 1],
        "yellow": [1, 1, 0, 1],
        "white": [1, 1, 1, 1],
    }

    return base[name]


def correct_date(date):
    b = str(date)
    b = b.split("-")

    c = ""

    for i in range(len(b)):
        c += f"{b[~i]}/"

    return c[:~0]


def hasher(data):
    hasher = sha256()
    hasher.update(str(data).encode("utf-8"))
    data = hasher.hexdigest()
    return data


def convert(old_path, new_path):

    size = (555, 555)
    img = Image.open(old_path)
    img = ImageOps.fit(img, size, Image.ANTIALIAS)

    img.save(new_path, "JPEG", quality=75)


def make_event(data):
    with open("event.json", "w+") as file:
        json.dump(data, file, indent=4)


def magnify(field, text):
    if field.text == text and field.focused:
        field.text = ""

    elif field.text == "" and not field.focused:
        field.text = text


CATEGORY = ["cinéma", "festival", "theatre", "musée", "sport", "concours", "mode"]

COLOR = ["black", "blue", "green", "red", "sky-blue", "violet", "yellow", "white"]
