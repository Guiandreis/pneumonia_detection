import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import torchvision.models as models

class resnet18model(nn.Module):


  def __init__(self):

    super(resnet18model, self).__init__()
    self.feature_extractor = models.resnet18(weights = None)
    self.feature_extractor = torch.nn.Sequential(
        *(list(self.feature_extractor.children())[:-2]))

    self.classifier = nn.Sequential(
        nn.AdaptiveAvgPool2d(output_size=(1, 1)),
        nn.Flatten(),
        nn.Linear(512, 128),
        nn.ReLU(inplace=True),
        nn.Linear(128, 2)
        )
    
    self.gradient = None

  def activations_hook(self, grad):
    self.gradient = grad

  def forward(self, images):

    x = self.feature_extractor(images) ### feature maps / ACTIVATION MAPS
    h = x.register_hook(self.activations_hook)
    x = self.classifier(x)  ## top layers
    return x

  def get_activation_gradients(self): ##a1, a2, a3...ak
    return self.gradient

  def get_activation(self,x):   ### A1,A2,A3 .. ak
    return self.feature_extractor(x)