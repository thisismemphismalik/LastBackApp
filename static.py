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
    with open("./temp/event.json", "w+") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def read_event():
    with open("./temp/event.json", "r+") as file:
        data = json.load(file)
        return data


def magnify(field, text):
    if field.text == text and field.focused:
        field.text = ""

    elif field.text == "" and not field.focused:
        field.text = text


def add_event_key(key):
    with open("./temp/event.json", "r+") as file:
        new_data = dict()
        data = json.load(file)

        new_data[key] = data

        make_event(new_data)


def add_tickets(tickets):
    with open("./temp/event.json", "r+") as file:
        data = json.load(file)

        a = [i for i in data.keys()][0]
        a = data[a]
        a["tickets"] = tickets

        make_event(data)


CATEGORY = ["cinéma", "festival", "theatre", "musée", "sport", "concours", "mode"]

COLOR = ["black", "blue", "green", "red", "sky-blue", "violet", "yellow", "white"]
