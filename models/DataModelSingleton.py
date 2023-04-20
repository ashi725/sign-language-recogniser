import uuid

# This singleton class stores data that can be accessed across the entire application.
class DataModelSingleton:

    # Creates singleton object if it doesnt exist
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataModelSingleton, cls).__new__(cls)
        return cls.instance

    trainDataset = None
    testDataset = None

class FingerDataset:
    def __init__(self):
        self.csvData = None
        self.databaseName = None
        self.labeledSet = {} # Dict. Key=Label name. Value=List of FingerImage classes
        self.totalImagesArray = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0]
        self.totalImages = 0

    def addFingerImage(self, key: str, fingerImageClass):
        if (key not in self.labeledSet):
            # New label if it doesnt exist.
            self.labeledSet[key] = []
        self.labeledSet[key].append(fingerImageClass)

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

class FingerImage:
    def __init__(self, label, numpyArr, pixmap):
        self.uniqueId = str(uuid.uuid4()) # A unique ID for each image. May come in handy for referencing imgs later.
        self.numpyImgArr = numpyArr
        self.pixMap = pixmap # This is the PixMap, Image used to display for PYQT
        self.label = label

# Create init singleton.
singleton = DataModelSingleton()
