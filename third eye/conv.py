from db import read

filename = "speech1.json"
dataset = read(filename)

def conversation(query):
    reply = ""
    if query in dataset:
        return dataset[query]
    
    return reply