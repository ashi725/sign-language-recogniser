

class HyperParametersSingleton:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(HyperParametersSingleton, cls).__new__(cls)
        return cls.instance
    
    # Details and hyperparameters used for model.
    dataset = None
    modelName = None
    batchsize = None
    epochs = None
    train = None
    validation = None
    test = None

    # Latest model settings
    latestTrainedModel = None
    latestTrainedModelTrain = None
    latestTrainedModelValidate = None
    latestTrainedModelDnnName = None
    latestTrainedModelBatchSize = None
    latestTrainedModelEpoch = None


singleton = HyperParametersSingleton()
