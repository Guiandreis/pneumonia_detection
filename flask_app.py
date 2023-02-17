import torch
import albumentations as A
import load_model
from PIL import Image
from io import BytesIO
import numpy as np
import cv2

from flask import Flask, request, send_file, render_template

def read_image( image_bytes):
    return np.array(Image.open(BytesIO(image_bytes))) 

IMG_SIZE = 224
val_transform = A.Compose(
    [        
        A.Resize(IMG_SIZE,IMG_SIZE),
        A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ]
)
def preprocess_image(file_storage):
    ''' Preprocess and transform image to NN'''

    image = np.array(Image.open(file_storage),dtype=np.uint8)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB) 
    image = val_transform(image = image)['image']
    image = torch.from_numpy(image).unsqueeze(0)
    image_preprocessed = np.transpose(image,(0,3,1,2))
    return image_preprocessed

def get_model(path):
    ''' LOAD MODEL '''
    
    print('load model')
    model = load_model.classify()
    model.load_state_dict(torch.load(path, map_location = torch.device(device)))
    print('model loaded')
    return model.eval()
device = 'cpu'
path = 'model_path\model_pneumonia.pt'
model = get_model(path)

app = Flask(__name__, template_folder='static')

@app.route('/')
def index():
    print('index ')
    return send_file('static\image.html')

@app.route('/image', methods=['POST'])
def receive_image():
    #message = request.get_json(force = True)
    file_storage = request.files.get('image')
    preprocessed_image = preprocess_image(file_storage)
    prediction = model(preprocessed_image)
    pred_probs = torch.softmax(prediction, dim=1).data.numpy()
    print('pred_probs',pred_probs)
    response = {
                'Pneumonia detector chances in (%)' : '',
                'Normal Chance': float(pred_probs[0][0])*100, 
                'Pneumonia Chance' : float(pred_probs[0][1])*100 
                }


    return render_template(
        'predictions.html', data = response)

if __name__ == '__main__':
    app.run(debug = True)