import json
import locale
import os
from datetime import datetime
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

    try:
        return base[name]

    except KeyError:
        return [0, 0, 0, 1]


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


def id_parser(old):
    ids = old
    ids = ' '.join([ids[i:i + 3] for i in range(0, len(ids), 3)])

    return ids


def make_tags():
    data = read_event()
    ids = [i for i in data.keys()][0]

    data = data[ids]

    all_tags = set()

    # add tags for long_fields ("location", "about", "name", "seller")
    long_fields = ["location", "about", "name", "seller"]

    for i in long_fields:

        for j in data[i].split(" "):
            all_tags.add(j.lower())

    # add category's tag
    all_tags.add(data["location"].lower())

    # date tags
    locale.setlocale(locale.LC_ALL, 'fr_FR.utf-8')
    date = data["date"].replace("/", "")
    date = datetime.strptime(date, "%d%m%Y")
    date = date.strftime("%A %d %B %Y")

    for i in date.split(" "):
        all_tags.add(i)

    # add tags for time
    time = data["time"]
    all_tags.add(time)
    all_tags.add(time.replace(":", "h"))
    all_tags.add(f"""{time.split(":")[0]}""")
    all_tags.add(f"""{time.split(":")[~0]}""")
    all_tags.add(f"""{time.split(":")[0] + "h"}""")

    # add tags for tickets
    tickets = data["tickets"]

    for i in tickets:
        # add "type"
        all_tags.add(i["type"].lower())

        # add "price"
        all_tags.add(i["price"])
        all_tags.add(i["price"].replace(" ", ""))
        all_tags.add(i["price"].replace(" ", "."))

        # add "advantage"
        for j in i["advantage"].split(" "):
            all_tags.add(j)

    return all_tags


CATEGORY = ["cinéma", "concert", "festival", "theatre", "musée", "sport", "concours", "mode"]

COLOR = ["black", "blue", "green", "red", "sky-blue", "violet", "yellow", "white"]

make_tags()
a = tuple()
