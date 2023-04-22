import os
import pickle

import torch

from models.pytorch_models.LeNet5 import LetNet5
from models.pytorch_models.ResNet import ResNet
import torchvision.models as models

import torch
from torch.utils import data
import torchvision.models as models
import torch.nn as nn
import torch.optim as optim

class SaveMechanism():
    """
    This class handles the saving and loading of pytorch models

    """
    def __init__(self):
        pass

    def saveTorch(self, saveName, filePath, trainRatio, valRatio, cnnName, batchSize, epochNumber, torchModel):
        """
        Save a pytorch model
        @param saveName: Name of the model
        @param filePath: Path where the pt file is located
        @param trainRatio: Ratio trained
        @param valRatio: Validation ratio trained
        @param cnnName: Name of the CNN
        @param batchSize: Size of batch trained
        @param epochNumber: Epoch trained
        @param torchModel: The physical pytorch model as an object
        @return:
        """
        # Save the list to a file
        saves = []
        saves.extend(self.loadAllMetadata())

        # Save the model and metadata
        torch.save(torchModel.state_dict(), filePath)
        saves.append(SaveStructue(saveName, filePath, trainRatio, valRatio, cnnName, batchSize, epochNumber))
        with open("torchSaves.pickle", "wb") as f:
            pickle.dump(saves, f)

    def loadTorchData(self, saveName):
        """
        This method loads the METADATA of the pytorch model
        @param saveName: Name of pytorch to load
        @return: A The pytorch metadata. It is a type SaveStructure
        """
        saves = self.loadAllMetadata()
        for save in saves:
            if save.saveName == saveName:
                return save
        return None

    def loadTorchModel(self, saveName):
        """
        This method loads a pytorch MODEL and sets it to eval mode
        @param saveName: Name of the model
        @return: A pytorch model
        """
        modelData = self.loadTorchData(saveName)

        modelType = None

       # Create the base model
        if modelData is not None:
            if modelData.cnnName == 'ResNet':
                modelType = ResNet()
            elif modelData.cnnName == 'LeNet5':
                modelType = LetNet5()
            else:
                print("ERR: NO model name found.")
                raise Exception("No modelname found!")

            # Load data state into model
            modelType.load_state_dict(torch.load(modelData.filePath))
            modelType.eval()
        return modelType

    def loadAllMetadata(self):
        """
        This method loads all pytorch metadata
        @return: Returns list of saveStructre objects
        """
        # Check if the file exists before loading the data
        if os.path.exists("torchSaves.pickle"):
            with open("torchSaves.pickle", "rb") as f:
                return pickle.load(f)
        else:
            # Handle the case where the file does not exist
            return []

class SaveStructue:
    """
    This class is a model of the data that is saved in the pickle
    """
    def __init__(self, saveName, filePath, trainRatio, valRatio, cnnName, batchSize, epochNumber):
        self.saveName = saveName
        self.filePath = filePath
        self.trainRatio = trainRatio
        self.valRatio = valRatio
        self.cnnName = cnnName
        self.batchSize = batchSize
        self.epochNumber = epochNumber

