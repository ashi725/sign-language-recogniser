import os
import pickle

import torch

from models.pytorch_models.NetModel import Net


class SaveMechanism():
    def __init__(self):
        pass

    def saveTorch(self, saveName, filePath, trainRatio, valRatio, dnnName, batchSize, epochNumber, torchModel):
        # Save the list to a file
        saves = []
        saves.extend(self._loadAll())

        torch.save(torchModel.state_dict(), filePath)
        saves.append(saveStructue(saveName, filePath, trainRatio, valRatio, dnnName, batchSize, epochNumber))


        with open("torchSaves.pickle", "wb") as f:
            pickle.dump(saves, f)

    def loadTorchData(self, saveName):
        saves = self._loadAll()
        for save in saves:
            if save.saveName == saveName:
                return save
        return None

    def loadTorchModel(self, saveName):
        modelData = self.loadTorchData(saveName)

        modelType = None

        # Create base model.
        if modelData is not None:
            if modelData.dnnName == 'resnet':
                print("not suppored")
            elif modelData.dnnName == 'lenet5':
                modelType = Net()
            else:
                print("ERR: NO model name found.")
                raise Exception("No modelname found!")

            # Load data into model

            modelType.load_state_dict(torch.load(modelData.filePath))
            modelType.eval()
        return modelType

    def _loadAll(self):
        # Check if the file exists before loading the data
        if os.path.exists("torchSaves.pickle"):
            with open("torchSaves.pickle", "rb") as f:
                return pickle.load(f)
        else:
            # Handle the case where the file does not exist
            return []

class saveStructue:
    def __init__(self, saveName, filePath, trainRatio, valRatio, dnnName, batchSize, epochNumber):
        self.saveName = saveName
        self.filePath = filePath
        self.trainRatio = trainRatio
        self.valRatio = valRatio
        self.dnnName = dnnName
        self.batchSize = batchSize
        self.epochNumber = epochNumber

