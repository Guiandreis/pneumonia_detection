import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import torchvision.models as models
import torchvision.transforms as transforms

from PIL import Image
import numpy as np
import cv2
import glob
import json
import os

def settings():
    
    device = 'cpu'
    path = '/home/ubuntu/pneumonia/model_pneumonia.pt'

    return device, path
    
class classify(nn.Module):
    ''' This is the model class'''


    def __init__(self,num_classes=2):

        super(classify,self).__init__()
        
         
        self.conv1=nn.Conv2d(
            in_channels=3, out_channels=12, kernel_size=3, stride=1, padding=1)
            
        self.bn1=nn.BatchNorm2d(num_features=12)
        self.relu1=nn.ReLU()        
        self.pool=nn.MaxPool2d(kernel_size=2)
        self.conv2=nn.Conv2d(
            in_channels=12,out_channels=20,kernel_size=3,stride=1,padding=1)

        self.bn2=nn.BatchNorm2d(num_features=20)
        self.relu2=nn.ReLU()
        self.conv3=nn.Conv2d(
            in_channels=20,out_channels=32,kernel_size=3,stride=1,padding=1)

        self.bn3=nn.BatchNorm2d(num_features=32)
        self.relu3=nn.ReLU()
        self.fc=nn.Linear(in_features=32 * 112 * 112,out_features=num_classes)
      
        
        #Feed forwad function
        
    def forward(self,input):

        output=self.conv1(input)
        output=self.bn1(output)
        output=self.relu1(output)
        output=self.pool(output)
        output=self.conv2(output)
        output=self.bn2(output)
        output=self.relu2(output)
        output=self.conv3(output)
        output=self.bn3(output)
        output=self.relu3(output)            
        output=output.reshape(-1,32*112*112)
        output=self.fc(output)
            
        return output

IMG_SIZE = 224
val_transform = transforms.Compose(
    [       
        transforms.ToTensor(),
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)

def preprocess_image(file_storage):
    ''' Preprocess and transform image to NN'''

    image = np.array(Image.open(file_storage),dtype=np.uint8)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB) 
    image = Image.fromarray(image)
    image = val_transform(image)
    image_preprocessed = image.unsqueeze(0)
    return image_preprocessed

def get_model(device,path):
    ''' LOAD MODEL '''
    
    print('load model')
    model = classify()
    model.load_state_dict(torch.load(path, map_location = torch.device(device)))
    print('model loaded')
    return model.eval()


def process_exam():
    '''This function is the main function'''

    images_to_process = glob.glob('/home/ubuntu/pneumonia/input/*')
    for file_storage in images_to_process:
        name = file_storage.split('/')[-1]

        if '.' in name[-5:]:
            new_name = name.split('.')[:-1]
            name = ''.join(new_name)

        device, path = settings()
        model = get_model(device,path)
        image_preprocessed = preprocess_image(file_storage)
        prediction = model(image_preprocessed)
        pred_probs = torch.softmax(prediction, dim=1).data.numpy()
        output = {  
                'Pneumonia detector chances in (%)' : '',
                'Normal Chance': float(pred_probs[0][0])*100, 
                'Pneumonia Chance' : float(pred_probs[0][1])*100 
                }

        json_object = json.dumps(output )

        with open('/home/ubuntu/pneumonia/output/' + name + ".json",
         "w") as outfile:
            outfile.write(json_object)
        os.remove(file_storage)
    return pred_probs

if __name__ == '__main__':
    pred_probs = process_exam()