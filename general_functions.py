import json


def read_settings(path):
    """ Returns the settings json with browser settings  """
    with open(str(path) + '/settings.json', 'rb') as f:
        return json.load(f)


