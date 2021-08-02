from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import tensorflow as tf
import numpy as np
from flask_cors import CORS
from flask import Flask, jsonify, request, render_template
import urllib
import json
import PILkkk

model = ResNet50(weights='imagenet')

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    try:
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
            if "necklace" in i or "ring" in i or "bracelet" in i or "chain" in i:
                cat = "Jewellery"
                break
            elif "skirt" in i or "uniform" in i or "coat" in i or "shirt" in i or "pant" in i or "jean" in i or "cloth" in i or "cardigan" in i or "suit" in i or "vest" in i or "jersey" in i:
                cat = "Clothing"
                break
            elif "glasses" in i or "wallet" in i or "tie" in i or "hat" in i or "purse" in i or "bag" in i or "sock" in i:
                cat = "Accessories"
                break
            elif "lipstick" in i or "face_powder" in i or "hair_spray" in i or "lotion" in i or "sunscreen" in i:
                cat = "Cosmetics"
                break
            elif "sofa" in i or "chair" in i or "table" in i or "board" in i or "desk" in i or "couch" in i or "wardrobe" in i or "case" in i:
                cat = "Furniture"
                break
            elif "shoe" in i or "slippers" in i or "sandal" in i or "boot" in i or "loafer" in i:
                cat = "Footwear"
                break
            
        return {'value':cat,'responseCode':200}
    

    except:
        return {'error':'Some error occurred in processing.','responseCode':403}


if __name__ == '__main__':
    app.run()
