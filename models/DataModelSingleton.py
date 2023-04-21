import uuid

# This singleton class stores data that can be accessed across the entire application.
import torch
from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image
from torchvision.transforms import ToTensor
import torch.nn.functional as F

class DataModelSingleton:

    # Creates singleton object if it doesnt exist
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataModelSingleton, cls).__new__(cls)
        return cls.instance

    trainDataset = None
    testDataset = None

class FingerDataset(Dataset):
    def __init__(self, transform = None):
        self.csvData = None
        self.databaseName = None
        self.labeledSet = {} # Dict. Key=Label name. Value=List of FingerImage classes
        self.totalImagesArray = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0]
        self.totalImages = 0

        # Pytorch. So can easily get item. EG FingerDataset.getitem(99)
        self.fingerLabelArray = []
        self.fingerImageArray = []

        # Apply default transofrm
        self.transform = None
        if (transform is not None):
            self.transform = transform
        else:
            self.transform = transforms.ToTensor()



    def addFingerImage(self, key: str, fingerImageClass):
        if (key not in self.labeledSet):
            # New label if it doesnt exist.
            self.labeledSet[key] = []
        self.labeledSet[key].append(fingerImageClass)

        # For usage in pytorch datasets
        fingerImageClass.uniqueId = self.totalImages
        self.fingerLabelArray.append(int(key))
        self.fingerImageArray.append(fingerImageClass)

        # Increment counters for total images
        self.totalImages += 1
        self._addImagesCounterInLabel(int(key))

    def getImagesByLabel(self, label):
        raise NotImplementedError()

    # Total images helper methods.
    def getTotalImagesInLabel(self, label: int):
        return self.totalImagesArray[label-1]

    def _addImagesCounterInLabel(self, label: int):
        self.totalImagesArray[label-1] += 1

    # Pytorch Dataset Methods
    def __len__(self):
        return len(self.fingerLabelArray)

    def __getitem__(self, index: int):
        pillowImage = self.fingerImageArray[index].pillowImage
        # pillowImage.resize((28, 28)) # Ensure 28x28 pixels
        labelInt = self.fingerLabelArray[index]
        labelTensor = torch.tensor(labelInt)

        if (self.transform is not None):
            pillowImage = self.transform(pillowImage)
        return pillowImage, labelTensor

class FingerImage:
    def __init__(self, label, numpyArr, pixmap, pilImg):
        self.uniqueId = None # This should automaticaly be remapped to an int.
        self.numpyImgArr = numpyArr
        self.pillowImage = pilImg
        self.pixMap = pixmap # This is the PixMap, Image used to display for PYQT
        self.label = label

        self.cameraImage = None # For high quality camera image. The vars above will be scaled down to 28x28px

# Create init singleton.
singleton = DataModelSingleton()
