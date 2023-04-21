import argparse
import threading

import torch
import cv2
import torch.nn.functional as F

# https://pyimagesearch.com/2021/07/19/pytorch-training-your-first-convolutional-neural-network-cnn/
from PyQt5.QtCore import QThread
from torch.utils.data import DataLoader

from models.PredictDataSingleton import PredictDataSingleton


class PredicterRunnerThread(QThread):

    def __init__(self, predictionSingleton):
        super().__init__()
        self.stopFlag = threading.Event()
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

        for (image, label) in predict_loader:
            # grab the original image and ground truth label
            origImage = image.numpy().squeeze(axis=(0, 1))

            # send the input to the device and make predictions on it
            image = image.to(device)
            pred = model(image)

            # find the class label index with the largest corresponding
            # probability
            idx = pred.argmax(axis=1).cpu().numpy()[0]
            print("Prediced ", idx)

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
