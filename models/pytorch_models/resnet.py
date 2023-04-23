# import the necessary packages
import torch.nn as nn
import torchvision.models as models


# Define ResNet model
class Resnet(nn.Module):
    def __init__(self):
        super(Resnet, self).__init__()
        self.resnet = models.resnet18(pretrained=False)
        self.resnet.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.resnet.fc = nn.Linear(512, 25)

    def forward(self, x):
        x = self.resnet(x.to(next(self.parameters()).device))
        return x