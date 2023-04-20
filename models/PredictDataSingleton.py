
class PredictDataSingleton:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PredictDataSingleton, cls).__new__(cls)
        return cls.instance

    latestCameraFeedImage = None
    listToPredict = []

class ImagePrediction:
    pixmap = None
    numpyArr = None
    actualLabel = "?"
    predictedLabel = None

singleton = PredictDataSingleton()
