import numpy as np
import torch
import torch.nn.functional as F

from PyQt5.QtCore import QThread, pyqtSignal
from torch.utils.data import DataLoader

from models.singletons.PredictDataSingleton import ImagePrediction


class PredicterRunnerThread(QThread):
    """
    This class runs a prediction based on the data stored in the prediction singleton
    The code is heavily reliant on the link below
    https://pyimagesearch.com/2021/07/19/pytorch-training-your-first-convolutional-neural-network-cnn/
    """
    # Flag to indicate finish predicting
    predictionFinished= pyqtSignal(int)

    def __init__(self, predictionSingleton):
        super().__init__()
        self.predictionSingleton = predictionSingleton

    def run(self):
        # Load device
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load predict dataset
        predict_dataset = self.predictionSingleton.predictionDataset
        if (predict_dataset is None):
            raise Exception("Predict dataset is none")
        predict_loader = DataLoader(dataset=predict_dataset, batch_size=1)

        model = self.predictionSingleton.TrainedModel
        model.eval()

        self.predictionSingleton.imagePredictionList = [] # Remove old predictions.

        for (image, label) in predict_loader:
            # grab the original image and ground truth label
            origImage = image.numpy().squeeze(axis=(0, 1))
            origImage = origImage * 255# Normalize range from 0-1 to 0-255
            origImage = np.array(origImage, dtype=np.uint8)

            actualLabel = label
            # send the input to the device and make predictions on it
            image = image.to(device)
            pred = model(image)

            # apply the softmax function to obtain a probability distribution
            probs = F.softmax(pred, dim=1)

            # find the class label index with the largest corresponding
            # probability
            idx = probs.argmax(axis=1).cpu().numpy()[0]
            print("Predicted class index: ", idx)

            # get the probability value for the predicted class
            prob = probs[0][idx]
            print("Probability of predicted class: ", prob.item())

            # get the probability values for all classes
            all_probs = probs.detach()[0].cpu().numpy()
            print("Probability distribution over all classes: ", all_probs)

            # Store predictions into memory
            self.predictionSingleton.imagePredictionList.append(
                ImagePrediction(origImage, idx, prob, all_probs, actualLabel)
            )
        self.predictionFinished.emit(0)