from db import read
import os
filename = "speech1.json"
filepath = os.path.join(os.getcwd(),'db', filename)
dataset = read(filepath)

def conversation(query):
    reply = ""
    if query in dataset:
        return dataset[query]
    else:
        return "test"
    