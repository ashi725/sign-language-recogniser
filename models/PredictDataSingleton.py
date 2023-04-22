from models.DataModelSingleton import FingerDataset


class PredictDataSingleton:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PredictDataSingleton, cls).__new__(cls)
        return cls.instance

    latestCameraFeedImage = None
    predictionDataset = FingerDataset()

    # Latest model settings
    TrainedModel = None
    latestTrainedModelTrain = None
    latestTrainedModelValidate = None
    latestTrainedModelDnnName = None
    latestTrainedModelBatchSize = None
    latestTrainedModelEpoch = None

    imagePredictionList = []

class ImagePrediction:
    def __init__(self, numpyImg, predictedClass, predictionProb, predProbDist, actualLabel):
        self.imageNumpy = numpyImg
        self.predictedClass = predictedClass
        self.predictedClassProbability = predictionProb
        self.predictionProbabilityDistribution = predProbDist
        self.actualClass = actualLabel # This may not exist.


def convertLabelToClassName(alphaFormIndex: int):
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    if alphaFormIndex == -1:
        return "Camera"
    return alphabet[alphaFormIndex]


singleton = PredictDataSingleton()
