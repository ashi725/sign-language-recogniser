from models.singletons.DataModelSingleton import FingerDataset


class PredictDataSingleton:
    """
    This class is a singleton
    It stores all the information required for predictions
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PredictDataSingleton, cls).__new__(cls)
        return cls.instance

    # Store the dataset to predict
    predictionDataset = FingerDataset()

    # Latest model settings. This model will be used to predict
    TrainedModel = None
    latestTrainedModelTrain = None
    latestTrainedModelValidate = None
    latestTrainedModelDnnName = None
    latestTrainedModelBatchSize = None
    latestTrainedModelEpoch = None

    # This arr stores a list of ImagePrediction() objects. Aka results of predictions
    imagePredictionList = []

class ImagePrediction:
    """
    This class stores the result of predictions
    """
    def __init__(self, numpyImg, predictedClass, predictionProb, predProbDist, actualLabel):
        """
        @param numpyImg: Numpy Arr of image predicted
        @param predictedClass: The predicted class as int
        @param predictionProb: The prediction certainity
        @param predProbDist: The distribution probability of all classes
        @param actualLabel: The real class as tensor. Note: if none avaliable, it is -1
        """
        self.imageNumpy = numpyImg
        self.predictedClass = predictedClass
        self.predictedClassProbability = predictionProb
        self.predictionProbabilityDistribution = predProbDist
        self.actualClass = actualLabel # This may not exist.


def convertLabelToClassName(alphaFormIndex: int):
    """
    This method converts an index in alphabet form into the corresponding alphabet
    @param alphaFormIndex: Index in alpha form. -1 for camera
    @return: Char corresponding to the class
    """
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    if alphaFormIndex == -1:
        return "Camera"
    return alphabet[alphaFormIndex]


singleton = PredictDataSingleton()
