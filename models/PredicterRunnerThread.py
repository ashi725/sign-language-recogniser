import argparse
import threading

import numpy as np
import torch
import cv2
import torch.nn.functional as F

# https://pyimagesearch.com/2021/07/19/pytorch-training-your-first-convolutional-neural-network-cnn/
from PyQt5.QtCore import QThread, pyqtSignal
from torch.utils.data import DataLoader

from models.PredictDataSingleton import PredictDataSingleton, ImagePrediction


class PredicterRunnerThread(QThread):
    predictionFinished= pyqtSignal(int)

    def __init__(self, predictionSingleton):
        super().__init__()
        self.predictionSingleton = predictionSingleton

    def run(self):
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

            self.predictionSingleton.imagePredictionList.append(
                ImagePrediction(origImage, idx, prob, all_probs, actualLabel)
            )
        self.predictionFinished.emit(0)