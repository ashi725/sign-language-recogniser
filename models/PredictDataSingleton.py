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





class ImagePrediction:
    pixmap = None
    numpyArr = None
    actualLabel = "?"
    predictedLabel = None

singleton = PredictDataSingleton()
