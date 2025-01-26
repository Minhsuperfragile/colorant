import torch
from torch import nn
from torch.nn import functional as F
from dataclasses import dataclass
from typing import *

@dataclass
class ColorantBaseConfig():
    def __init__(self, 
                frame_size: Optional[Tuple[int,int]] = None , 
                roi_size: Optional[Tuple[int,int]] = None):
        
        self.frame_size = frame_size if frame_size is not None else (1920,1080) # (width,height)
        self.roi_size = roi_size if roi_size is not None else (100,24) # (width,height)
        self.input_size = self.roi_size[0] * self.roi_size[1]
    
class BinaryClassification(nn.Module):
    """
    This class implements a binary classification model using PyTorch, to determine if crosshair in on an enemy or not.
    """
    def __init__(self, config: ColorantBaseConfig):
        
        self.fully_connected_layer = nn.Linear(config.input_size, 1)

        pass

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool(x)
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

