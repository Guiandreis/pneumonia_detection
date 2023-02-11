import torch
import numpy as np
import cv2
import io
from PIL import Image
import base64
import albumentations as A

import load_model
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

IMG_SIZE = 224
val_transform = A.Compose(
    [        
        A.Resize(IMG_SIZE,IMG_SIZE),
        A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ]
)
def preprocess_image(message):
    ''' Preprocess and transform image to NN'''

    encoded = message['image']
    decoded = base64.b64decode(encoded)   
    image = io.BytesIO(decoded)
    image.seek(0)
    image = np.asarray(bytearray(image.read()), dtype=np.uint8)
    image = cv2.imdecode(image,0)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)    
    image = val_transform(image = image)['image']
    image = torch.from_numpy(image).unsqueeze(0)
    image_preprocessed = np.transpose(image,(0,3,1,2))

    return image_preprocessed

def get_model(path):
    ''' LOAD MODEL '''

    print('load model')
    model = load_model.resnet18model()
    model.load_state_dict(torch.load(path))
    print('model loaded')
    return model.eval()

path = 'model_path\model_pneumonia_resnet18.pt'
model = get_model(path)

@app.route('/predict', methods = ['POST'])
@cross_origin()
def predict():
    print('entrou post1')
    message = request.get_json(force = True)
    preprocessed_image = preprocess_image(np.array(message))
    prediction = model(preprocessed_image)
    pred_probs = torch.softmax(prediction, dim=1).data.numpy()
    
    response = {
        'prediction':{
            'normal': float(pred_probs[0][0]),
            'pneumonia' : float(pred_probs[0][1])
            }
        }
    print('response',response)
    return jsonify(response)
    