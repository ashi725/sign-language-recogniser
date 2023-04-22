

class HyperParametersSingleton:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(HyperParametersSingleton, cls).__new__(cls)
        return cls.instance
    
    # Details and hyperparameters used for model.
    dataset = None
    modelName = "lenet5"
    batchsize = 100
    epochs = 2
    train = 50
    validation = 50
    test = 0

    # Latest model settings
    latestTrainedModel = None
    latestTrainedModelTrain = None
    latestTrainedModelValidate = None
    latestTrainedModelDnnName = None
    latestTrainedModelBatchSize = None
    latestTrainedModelEpoch = None


singleton = HyperParametersSingleton()
