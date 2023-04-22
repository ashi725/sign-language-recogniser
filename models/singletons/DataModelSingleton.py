import torch
from torch.utils.data import Dataset
from torchvision import transforms

class DataModelSingleton:
    """
    This class is a singleton.
    It stores the training and test datasets which can be referenced throughout the app
    """
    # Creates singleton object if it doesnt exist
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataModelSingleton, cls).__new__(cls)
        return cls.instance

    # The data that is shared
    trainDataset = None
    testDataset = None

class FingerDataset(Dataset):
    """
    This class represents a pytorch dataset.
    Note throughout this section there are two types of indices
    ArrayIndex -> This is the index of where the alphabet is in the array.
    AlphabetIndex -> This is the index of where the alphabet would correspond in the FULL Alphabet.
    """
    def __init__(self, transform = None):
        self.csvData = None
        self.databaseName = None
        self.labeledSet = {} # Dict. Key=Label name. In ALPHABET INDEX. Value=List of FingerImage classes
        self.totalImagesArray = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0]
        self.totalImages = 0

        # Arrays for Pytorch usage
        self.fingerLabelArray = []
        self.fingerImageArray = []

        # Pytorch Tensor transformation
        self.transform = None
        if (transform is not None):
            self.transform = transform
        else:
            self.transform = transforms.ToTensor()


    def addFingerImage(self, keyAlphabetIndex: str, fingerImageClass):
        """
        This method adds a FingerImage class into the dataset
        @param keyAlphabetIndex: The key in ALPHABET INDEX
        @param fingerImageClass: Obj to add to dataset
        @return: None
        """

        # Create new key if doesnt exist in dictonary
        if (keyAlphabetIndex not in self.labeledSet):
            self.labeledSet[keyAlphabetIndex] = []
        self.labeledSet[keyAlphabetIndex].append(fingerImageClass)

        # For usage in pytorch datasets
        fingerImageClass.uniqueId = self.totalImages
        self.fingerLabelArray.append(int(keyAlphabetIndex))
        self.fingerImageArray.append(fingerImageClass)

        # Increment counters for total images
        self.totalImages += 1
        self._addImagesCounterInLabel(int(keyAlphabetIndex))


    def getTotalImagesInLabel(self, label: int):
        """
        Get the total images in a label
        @param label: The class. In array index format
        @return:
        """
        return self.totalImagesArray[label-1]

    def _addImagesCounterInLabel(self, label: int):
        """
        Get total images for each class label.
        @param label: Takes index in Alphabet format
        @return: int total amount of images
        """
        label = convertSignIndexToArr(label)
        self.totalImagesArray[label-1] += 1

    ###########################
    # Pytorch Dataset Methods #
    ###########################
    def __len__(self):
        '''
        Used for pytorch.
        @return: Size of dataset
        '''
        return len(self.fingerLabelArray)

    def __getitem__(self, index: int):
        '''
        Used for pytorch dataset. Grabs one datapoint from an ARRAY
        @param index: A index for where the datapoint is.
        @return: Pillow image and label in alpbaet index
        '''

        # Fetch data from internal variables
        pillowImage = self.fingerImageArray[index].pillowImage
        labelInt = self.fingerLabelArray[index]
        labelTensor = torch.tensor(labelInt)

        # Apply transform to transfer into tensor
        if (self.transform is not None):
            pillowImage = self.transform(pillowImage)

        return pillowImage, labelTensor


class FingerImage:
    """
    This class represents one image.
    """
    def __init__(self, label, numpyArr, pixmap, pilImg):
        """
        Create a fingerimage obj
        @param label: This should be an integer
        @param numpyArr: Contains the grayscale image
        @param pixmap: Contains the pixmap for PYQT display
        @param pilImg: Contains the Pillow image format
        """
        self.uniqueId = None
        self.numpyImgArr = numpyArr
        self.pillowImage = pilImg
        self.pixMap = pixmap # This is the PixMap, Image used to display for PYQT
        self.label = label # Label is 0-9 10-24. (Correspoinding to alphabet)

def convertSignIndexToArr(index: int):
    """
    Helper method to convert from ALPHABET INDEX -> ARR INDEX
    @param index: Alphabet index
    @return: Array Index
    """
    if index <= 8:
        return index
    else:
        return index - 1

def convertIndexArrToAlphabetIndex(index: int):
    """
    Helper method to convert from ARR INDEX -> ALHABET INDEX
    @param index: Array index
    @return: Alphabet index
    """
    if index <= 8:
        return index
    else:
        return index + 1

# Create init singleton.
singleton = DataModelSingleton()
