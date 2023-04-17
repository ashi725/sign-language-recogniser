# ResNet CNN Model 
#
# Date: 14/04/2023
# Author: Anna Shimizu [ashi725]

# Load libraries
import torch
from torchvision import datasets, transforms
from torch.utils import data
import torchvision.models as models
import torch.nn as nn
import torch.optim as optim

# Training settings
batch_size = 128
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Training MNIST Model on {device}\n{"=" * 44}')

# MNIST Dataset
train_dataset = datasets.MNIST(root='mnist_data/',
                               train=True,
                               transform=transforms.ToTensor(),
                               download=True)

test_dataset = datasets.MNIST(root='mnist_data/',
                              train=False,
                              transform=transforms.ToTensor())

# Data Loader 
train_loader = data.DataLoader(dataset=train_dataset,
                               batch_size=batch_size,
                               shuffle=True)

test_loader = data.DataLoader(dataset=test_dataset,
                              batch_size=batch_size,
                              shuffle=False)

# ResNet Model
resnet = models.resnet18(pretrained=False) # Load ResNet model architecture

# Replace first convolutional layer and fully connected layer
resnet.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
resnet.fc = nn.Linear(512, 10)

model = resnet.to(device) # Move to specified device

# Loss function and optimizer with learning rate
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

def train(epoch):

    model.train() # Set model to training mode

    for batch_idx, (data, target) in enumerate(train_loader):

        data, target = data.to(device), target.to(device) # Move the input data and target labels
        optimizer.zero_grad() # Zero out the gradients
        output = model(data) # Pass data through the model
        loss = criterion(output, target) # Compute loss
        loss.backward() # Compute gradients of the loss with respect to model parameters
        optimizer.step() # Update model parameters based on computed gradients and optimizer

        # Print training progress
        if batch_idx % 10 == 0:
            print('Train Epoch: {} | Batch Status: {}/{} ({:.0f}%) | Loss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))
            

def test():
    model.eval()
    test_loss = 0
    correct = 0

    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device) # Move the input data and target labels
            output = model(data) # Pass data through the model
            test_loss += criterion(output, target).item() # Sum up batch loss
            pred = output.data.max(1, keepdim=True)[1] # Get the index of the max
            correct += pred.eq(target.data.view_as(pred)).cpu().sum() # Sum up the correct predictions

    test_loss /= len(test_loader.dataset)
    print(f'===========================\nTest set: Average loss: {test_loss:.4f}, Accuracy: {correct}/{len(test_loader.dataset)} '
          f'({100. * correct / len(test_loader.dataset):.0f}%)')
