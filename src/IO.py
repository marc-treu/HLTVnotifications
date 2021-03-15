import json


def write(data):
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)


def read():
    try:
        with open('data.json') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        return []
    return data


