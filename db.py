import json

def read(filename):
    data = {}
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def write(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def modify(filename, key, value):
    config_data = read(filename)
    config_data[key] = value
    write(config_data, filename)
