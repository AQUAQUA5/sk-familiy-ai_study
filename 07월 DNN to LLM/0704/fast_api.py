from fastapi import FastAPI 
from pydantic import BaseModel 
from torchvision import transforms
from PIL import Image
import io
import base64
import torch

import torch.nn as nn
import torch.nn.functional as F

class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1, downsample=None):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.downsample = downsample

    def forward(self, x):
        identity = x
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        if self.downsample is not None:
            identity = self.downsample(x)
        out += identity
        out = self.relu(out)
        return out

def make_layer(block, in_channels, out_channels, num_blocks, stride):
    downsample = None
    if stride != 1 or in_channels != out_channels:
        downsample = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
            nn.BatchNorm2d(out_channels)
        )
    layers = []
    layers.append(block(in_channels, out_channels, stride, downsample))
    for _ in range(1, num_blocks):
        layers.append(block(out_channels, out_channels))
    return nn.Sequential(*layers)

class ResNet20(nn.Module):
    def __init__(self, num_classes=2):
        super(ResNet20, self).__init__()
        self.in_channels = 16
        self.conv = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn = nn.BatchNorm2d(16)
        self.relu = nn.ReLU(inplace=True)
        # 각 스테이지마다 3개 블록
        self.layer1 = make_layer(ResidualBlock, 16, 16, 3, stride=1)
        self.layer2 = make_layer(ResidualBlock, 16, 32, 3, stride=2)
        self.layer3 = make_layer(ResidualBlock, 32, 64, 3, stride=2)
        self.avg_pool = nn.AvgPool2d(8)
        self.fc = nn.Linear(64, num_classes)

    def forward(self, x):
        out = self.relu(self.bn(self.conv(x)))
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.avg_pool(out)
        out = out.view(out.size(0), -1)
        out = self.fc(out)
        return out

model = ResNet20(num_classes=2)
model.load_state_dict(torch.load('resnet20.pth', map_location='cpu'))
model.eval()

transform = transforms.Compose([
    transforms.Resize((32,32)),
    transforms.ToTensor()
])

class ImageItem(BaseModel):
    image_data : str 
    # filename : str 
    # create_date : int 

app = FastAPI() 

@app.post("/predict/")
async def inference(item: ImageItem):
    img_bytes = base64.b64decode(item.image_data)
    image = Image.open(io.BytesIO(img_bytes))
    input_tensor = transform(image)
    input_tensor = input_tensor.unsqueeze(0)
    with torch.no_grad():
        output = model(input_tensor)
        if output[0][0] > output[0][1]:
            return {"message" : "개"}
        else:
            return {"message" : "고양이"}