from deepface import DeepFace
import os
import keras

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

models = [
    "VGG-Face", 
    "Facenet", 
    "Facenet512", 
    "OpenFace", 
    "DeepFace", 
    "DeepID", 
    "ArcFace", 
    "Dlib", 
    "SFace",
]
result = DeepFace.verify(img1_path = "img1.jpeg", img2_path = "img2.jpeg", model_name= models[0])


print(result)