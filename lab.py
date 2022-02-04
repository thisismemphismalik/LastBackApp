def create_event(name, image, color, category, about, location, datetime):
    data = {
        "name": name,
        "image": image,
        "color": color,
        "category": category,
        "about": about,
        "location": location,
        "datetime": datetime
    }

    return data
