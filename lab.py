def create_event(infos: list):
    data = {
        "name": infos[0],
        "image": infos[1],
        "color": infos[2],
        "category": infos[3],
        "about": infos[4],
        "location": infos[5],
        "date": infos[6],
        "time": infos[7]
    }

    return data
