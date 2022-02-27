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


CATEGORY = ["cinéma", "festival", "theatre", "musée", "sport", "concours", "mode"]

COLOR = ["black", "blue", "green", "red", "sky-blue", "violet", "yellow", "white"]
