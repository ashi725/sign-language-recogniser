import threading

import numpy as np
import torch
from PyQt5.QtCore import QThread, pyqtSignal


# import the necessary packages
from torch.utils.data import random_split
from torch.utils.data import DataLoader
from torchvision.transforms import ToTensor
from torchvision.datasets import KMNIST
from torch.optim import Adam
from torch import nn
import matplotlib.pyplot as plt
import numpy as np
import argparse
import torch
import time

from torch import cuda, nn, optim
from torch.utils import data
from torchvision import datasets, transforms
import torchvision.models as models
import torch.nn.functional as F
import time

from models.pytorch_models.NetModel import Net
from models.pytorch_models.lenet5 import LeNet5


class ModelTrainerThread(QThread):
    progressBarChanged = pyqtSignal(int)
    statusUpdate = pyqtSignal(str)


    def __init__(self, hyperParametersSingleton, dataModelSingleton):
        super().__init__()
        self.stopFlag = threading.Event()
        self.shouldSaveFlag = threading.Event()
        self.hyperParametersSingleton = hyperParametersSingleton
        self.dataModelSingleton = dataModelSingleton

        self.model = None
        self.train_loader = None
        self.test_loader = None
        self.device = None
        self.opt = None
        self.criterion = None
        self.lossFn = None

    def run(self):
        batch_size = self.hyperParametersSingleton.batchsize
        self.device = 'cuda' if cuda.is_available() else 'cpu'

        train_dataset = self._loadTrainDataset()
        test_dataset = self._loadTestDataset()

        # Data Loader
        self.train_loader = data.DataLoader(
            dataset=train_dataset,
            batch_size=batch_size,
            shuffle=True
        )

        self.test_loader = data.DataLoader(
            dataset=test_dataset,
            batch_size=batch_size,
            shuffle=False
        )

        # Instantiate the LeNet5 model and move to specified device
        self.model = self._determine_pytorch_model() # Model on CPU
        self.model = self.model.to(self.device) # Move to GPU if supported

        # Loss function (cross-entropy) and optimizer with learning rate and momentum. CrossEntropyLoss
        if self.hyperParametersSingleton.modelName == 'resnet':
            print("Unsupported yet")
        elif self.hyperParametersSingleton.modelName == 'lenet5':
            self.lossFn = nn.NLLLoss()
            self.opt = Adam(self.model.parameters(), lr=1e-3)

        self.start_training_and_testing()

    # Calculate the accuracy
    # Out is the actual output. labels is real.
    def accuracy(self, out, labels):
        _, pred = torch.max(out, dim=1)
        return torch.sum(pred == labels).item()

    #  https://pyimagesearch.com/2021/07/19/pytorch-training-your-first-convolutional-neural-network-cnn/
    # This algorithm is heavily reliant on the code supplied from above.
    def start_training_and_testing(self):

        # measure how long training is going to take
        print("[INFO] training the network...")
        startTime = time.time()

        # initialize a dictionary to store training history
        H = {
            "train_loss": [],
            "train_acc": [],
            "val_loss": [],
            "val_acc": []
        }

        ############
        # TRAINING #
        ############
        # loop over our epochs
        for e in range(0, self.hyperParametersSingleton.epochs):
            # set the model in training mode
            self.model.train()
            # initialize the total training and validation loss
            totalTrainLoss = 0
            totalValLoss = 0
            # initialize the number of correct predictions in the training
            # and validation step
            trainCorrect = 0
            valCorrect = 0
            # loop over the training set
            for (x, y) in self.train_loader:
                # send the input to the device
                (x, y) = (x.to(self.device), y.to(self.device))
                # perform a forward pass and calculate the training loss
                pred = self.model(x)
                loss = self.lossFn(pred, y)
                # zero out the gradients, perform the backpropagation step,
                # and update the weights
                self.opt.zero_grad()
                loss.backward()
                self.opt.step()
                # add the loss to the total training loss so far and
                # calculate the number of correct predictions
                totalTrainLoss += loss
                trainCorrect += (pred.argmax(1) == y).type(torch.float).sum().item()

        print("[INFO] FINISH Tra the network...")
        ##############
        # Evaluation #
        #############
        # switch off autograd for evaluation
        with torch.no_grad():
            # set the model in evaluation mode
            self.model.eval()
            # loop over the validation set
            for (x, y) in self.test_loader:
                # send the input to the device
                (x, y) = (x.to(self.device), y.to(self.device))
                # make the predictions and calculate the validation loss
                pred = self.model(x)
                totalValLoss += self.lossFn(pred, y)
                # calculate the number of correct predictions
                valCorrect += (pred.argmax(1) == y).type(
                    torch.float).sum().item()
        print("[INFO] FINISH eva.jtatk g the network...")


    def stop(self):
        self.stopFlag.set()

    def cleanup_stop(self):
            print("Okay I stopped. Cleanup unfinished work!")
            self.statusUpdate.emit("Okay I stopped. Cleanup unfinished work!")
            # Todo make sure data is cleaned up

    def saveModel(self, filePath):
        print("Model runner told to stop!")
        self.statusUpdate.emit("Model runner told to stop!")
        self.shouldSaveFlag.set()

    def _determine_pytorch_model(self):
        if self.hyperParametersSingleton.modelName == 'resnet':
            resnet = models.resnet18(weights = None) # Load ResNet model architecture
            # Replace first convolutional layer and fully connected layer
            resnet.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
            resnet.fc = nn.Linear(512, 10)

        elif self.hyperParametersSingleton.modelName == 'lenet5':
            return Net()
        elif self.hyperParametersSingleton.modelName == 'resnet':
            pass
        # resnet = models.resnet18(weights = None) # Load ResNet model architecture
        else:
            print("ERR: NO model name found.")
            raise Exception("No modelname found!")

    def _loadTrainDataset(self):
        if self.hyperParametersSingleton.modelName == 'resnet':
            pass
        elif self.hyperParametersSingleton.modelName == 'lenet5':
            return self.dataModelSingleton.trainDataset
            # return  datasets.MNIST(root='./data',
            #                    train=True,
            #                    transform=transforms.ToTensor(),
            #                    download=True)
        else:
            print("Load Dataset Err")
            raise Exception("Load Dataset Err")

    def _loadTestDataset(self):
        if self.hyperParametersSingleton.modelName == 'resnet':
            pass

        elif self.hyperParametersSingleton.modelName == 'lenet5':
            return self.dataModelSingleton.testDataset
        else:
            print("Load Dataset Err")
            raise Exception("Load Dataset Err")

