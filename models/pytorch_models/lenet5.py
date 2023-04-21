from models.pytorch_models.AbstractModel import AbstractModel
from torch import cuda, nn, optim
from torch.utils import data
from torchvision import datasets, transforms
import torch.nn.functional as F
import time


class LeNet5(nn.Module):

    # Definition of the architecture of the LeNet5 model
    def __init__(self):
        super(LeNet5, self).__init__()

        # First convolutional layer and max poooling
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=6, kernel_size=3, stride=1, padding=1)
        self.maxpool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        # Second convolutional layer and max pooling
        self.conv2 = nn.Conv2d(in_channels=6, out_channels=16, kernel_size=3, stride=1, padding=1)
        self.maxpool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        # Fully connected layers
        self.fc1 = nn.Linear(16 * 7 * 7, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 24)

    # Definition of the forward pass through the LeNet5 model
    def forward(self, x):
        # First and second convolution, ReLU and maxpooling
        x = self.maxpool1(F.relu(self.conv1(x)))
        x = self.maxpool2(F.relu(self.conv2(x)))

        # Flatten the output of second convolution
        x = x.view(-1, 16 * 7 * 7)

        # Fully connected layers and ReLU
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))

        # Apply final fully connected layer and return output.
        return self.fc3(x)