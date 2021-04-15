from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import tensorflow as tf
import numpy as np
from flask import Flask, jsonify, request
import urllib
import json
import PIL

model = ResNet50(weights='imagenet')

app = Flask(__name__)

@app.route('/', methods=['POST'])

def predict():
    link = request.get_json(force=True)
    link = link['Link']

    urllib.request.urlretrieve(link, "classify.jpg")

    img = PIL.Image.open("classify.jpg")
    img = img.resize((224, 224))

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)

    val=[]
    for i in range(len(decode_predictions(preds)[0])):
        print(decode_predictions(preds)[0][i][1])
        val.append(decode_predictions(preds)[0][i][1])

    cat="Invalid"

    for i in val:
        if "necklace" in i or "ring" in i or "bracelet" in i:
            cat = "Jewellery"
            break
        elif "shirt" in i or "pant" in i or "jean" in i or  "cloth" in i:
            cat = "Clothing"
            break
        elif "glasses" in i or "wallet" in i or "buckle" in i or "tie" in i or "hat" in i:
            cat = "Accessories"
            break
        elif "lipstick" in i or "face_powder" in i or "hair_spray" in i:
            cat = "Cosmetics"
            break
        
    #output={'results':link}
    return {'value':cat,'responseCode':200}

if __name__ == '__main__':
    app.run(port=5000, debug=True)
