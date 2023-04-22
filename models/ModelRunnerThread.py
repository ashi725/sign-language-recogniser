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
    finishStatus = pyqtSignal(int) # Emit -1 for failure. Emit 0 for pass

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

        # If was told to stop. Perform cleanup
        if (self.stopFlag.is_set()):
            self.cleanup_stop()
        else:
            print("Successfully trained")

            # Save latest trained model into memory
            self.hyperParametersSingleton.latestTrainedModel = self.model
            self.hyperParametersSingleton.latestTrainedModelTrain = self.hyperParametersSingleton.train
            self.hyperParametersSingleton.latestTrainedModelValidate = self.hyperParametersSingleton.validation
            self.hyperParametersSingleton.latestTrainedModelDnnName = self.hyperParametersSingleton.modelName
            self.hyperParametersSingleton.latestTrainedModelBatchSize = self.hyperParametersSingleton.batchsize
            self.hyperParametersSingleton.latestTrainedModelEpoch = self.hyperParametersSingleton.epochs
            self.finishStatus.emit("0") # Tell finish normally

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
        since = time.time()

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
            if (self.stopFlag.is_set()):
                    return

            # set the model in training mode
            self.model.train()
            # initialize the total training and validation loss
            totalTrainLoss = 0
            totalValLoss = 0
            # initialize the number of correct predictions in the training
            # and validation step
            trainCorrect = 0
            valCorrect = 0

            counter = 0
            # loop over the training set
            for (x, y) in self.train_loader:
                # Stop flag
                if (self.stopFlag.is_set()):
                    return

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

                # Status information
                if counter % 10 == 0:
                    print('Train Epoch: {} | Batch Status: ({:.0f}%) | Loss: {:.6f}'.format(
                        e+1,100. * counter / len(self.train_loader), loss.item()))

                    self.statusUpdate.emit('Train Epoch: {} | Batch Status:({:.0f}%) | Loss: {:.6f}'.format(
                        e+1,100. * counter / len(self.train_loader), loss.item()))

                    self.progressBarChanged.emit(int(100. * counter / len(self.train_loader)))
                counter += 1
        print("[INFO] Finished Training. Start Evaluation. Please Wait")
        self.statusUpdate.emit('Finished Training. Evaluating')
        self.progressBarChanged.emit(100)
        ##############
        # Evaluation #
        #############
        # switch off autograd for evaluation
        with torch.no_grad():
            # set the model in evaluation mode
            self.model.eval()
            # loop over the validation set
            for (x, y) in self.test_loader:
                if (self.stopFlag.is_set()):
                    return

                # send the input to the device
                (x, y) = (x.to(self.device), y.to(self.device))
                # make the predictions and calculate the validation loss
                pred = self.model(x)
                totalValLoss += self.lossFn(pred, y)
                # calculate the number of correct predictions
                valCorrect += (pred.argmax(1) == y).type(
                    torch.float).sum().item()
        print("[INFO] Finished Evaluation.")

        ##############
        # Statistics #
        ##############
        # calculate the average training and validation loss
        trainSteps = len(self.train_loader.dataset) // self.hyperParametersSingleton.batchsize
        valSteps = len(self.test_loader.dataset) // self.hyperParametersSingleton.batchsize
        avgTrainLoss = totalTrainLoss / trainSteps
        avgValLoss = totalValLoss / valSteps
        # calculate the training and validation accuracy
        trainCorrect = trainCorrect / len(self.train_loader.dataset)
        valCorrect = valCorrect / len(self.test_loader.dataset)
        # update our training history
        H["train_loss"].append(avgTrainLoss.cpu().detach().numpy())
        H["train_acc"].append(trainCorrect)
        H["val_loss"].append(avgValLoss.cpu().detach().numpy())
        H["val_acc"].append(valCorrect)

        m, s = divmod(time.time() - since, 60)
        statOne = "[INFO] EPOCH: {}/{}\n".format(e + 1, self.hyperParametersSingleton.epochs)
        statTwo = "Train loss: {:.6f}, Train accuracy: {:.4f}\n".format(avgTrainLoss, trainCorrect)
        statThree = "Val loss: {:.6f}, Val accuracy: {:.4f}\n".format(avgValLoss, valCorrect)
        statFour = f'Total Time: {m:.0f}m {s:.0f}s\nModel was trained on {self.device}!'
        print(statOne, statTwo, statThree)
        self.statusUpdate.emit("{}{}{}{}".format(statOne, statTwo, statThree, statFour))

    def stop(self):
        self.stopFlag.set()

    def cleanup_stop(self):
            print("Okay I stopped. Cleanup unfinished work!")
            self.statusUpdate.emit("Okay I stopped. Cleanup unfinished work!")
            self.finishStatus.emit("-1")
            # Todo make sure data is cleaned up

    def saveModel(self, filePath):
        print("Saving yes!")
        self.shouldSaveFlag.set()

    def _determine_pytorch_model(self):
        if self.hyperParametersSingleton.modelName == 'resnet':
            resnet = models.resnet18(weights = None) # Load ResNet model architecture
            # Replace first convolutional layer and fully connected layer
            resnet.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
            resnet.fc = nn.Linear(512, 10)

        elif self.hyperParametersSingleton.modelName == 'lenet5':
            return Net()
        # resnet = models.resnet18(weights = None) # Load ResNet model architecture
        else:
            print("ERR: NO model name found.")
            raise Exception("No modelname found!")

    def _loadTrainDataset(self):
        return self.dataModelSingleton.trainDataset

    def _loadTestDataset(self):
        return self.dataModelSingleton.testDataset
