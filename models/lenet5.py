# LeNet5 CNN Model 
#
# Date: 13/04/2023
# Author: Anna Shimizu [ashi725]

# Load libraries
from torch import cuda, nn, optim
from torch.utils import data
from torchvision import datasets, transforms
import torch.nn.functional as F
import time

from HyperParametersSingleton import HyperParametersSingleton

hyperParameters = HyperParametersSingleton()


# Training settings
batch_size = hyperParameters.batchsize
epochs = hyperParameters.epochs

device = 'cuda' if cuda.is_available() else 'cpu'

print(f'Training LeNet5 Model on {device}\n{"=" * 44}')

# Load Kaggle MNIST dataset
train_dataset = datasets.MNIST(root='./data', 
                               train=True, 
                               transform=transforms.ToTensor(), 
                               download=True)

test_dataset = datasets.MNIST(root='./data',
                              train=False,
                              transform=transforms.ToTensor())

# Data Loader 
train_loader = data.DataLoader(dataset=train_dataset,
                               batch_size=batch_size,
                               shuffle=True)

test_loader = data.DataLoader(dataset=test_dataset,
                              batch_size=batch_size,
                              shuffle=False)


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
        self.fc1 = nn.Linear(16*7*7, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    # Definition of the forward pass through the LeNet5 model
    def forward(self, x):

        # First and second convolution, ReLU and maxpooling
        x = self.maxpool1(F.relu(self.conv1(x)))
        x = self.maxpool2(F.relu(self.conv2(x)))

        # Flatten the output of second convolution 
        x = x.view(-1, 16*7*7)

        # Fully connected layers and ReLU
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))

        # Apply final fully connected layer and return output.
        return self.fc3(x)
    
# Instantiate the LeNet5 model and move to specified device
model = LeNet5()
model.to(device)

# Loss function (cross-entropy) and optimizer with learning rate and momentum
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.5)

# Definition of the training function
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

# Definition of the testing function
def test():
    model.eval() 
    test_loss = 0
    correct = 0

    for data, target in test_loader:

        data, target = data.to(device), target.to(device) # Move the input data and target labels
        output = model(data) # Pass data through the model
        test_loss += criterion(output, target).item() # sum up batch loss
        pred = output.data.max(1, keepdim=True)[1] # get the index of the max
        correct += pred.eq(target.data.view_as(pred)).cpu().sum() # Sum up the correct predictions

    test_loss /= len(test_loader.dataset)
    print(f'===========================\nTest set: Average loss: {test_loss:.4f}, Accuracy: {correct}/{len(test_loader.dataset)} '
          f'({100. * correct / len(test_loader.dataset):.0f}%)')

# Main
if __name__ == '__main__':

    since = time.time() # Starting time of whole training

    for epoch in range(1,epochs+1):

        epoch_start = time.time() # Starting time of this epoch

        # Train and print training time of epoch
        train(epoch)
        m, s = divmod(time.time() - epoch_start, 60)
        print(f'Training time: {m:.0f}m {s:.0f}s')

        # Test and print testing time of epoch
        test()
        m, s = divmod(time.time() - epoch_start, 60)
        print(f'Testing time: {m:.0f}m {s:.0f}s')

    # Print total training time
    m, s = divmod(time.time() - since, 60)
    print(f'Total Time: {m:.0f}m {s:.0f}s\nModel was trained on {device}!')
    