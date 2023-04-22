class HyperParametersSingleton:
    """
    This class is a singleton
    It contains all the information about training a model
    """
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
    latestTrainedModelCnnName = None
    latestTrainedModelBatchSize = None
    latestTrainedModelEpoch = None


singleton = HyperParametersSingleton()
