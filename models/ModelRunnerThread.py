import threading

from PyQt5.QtCore import QThread, pyqtSignal

from torch import cuda, nn, optim
from torch.utils import data
from torchvision import datasets, transforms
import torch.nn.functional as F
import time

from models.pytorch_models.lenet5 import LeNet5


class ModelTrainerThread(QThread):
    progressBarChanged = pyqtSignal(int)
    statusUpdate = pyqtSignal(str)


    def __init__(self, hyperParametersSingleton):
        super().__init__()
        self.stopFlag = threading.Event()
        self.shouldSaveFlag = threading.Event()
        self.hyperParametersSingleton = hyperParametersSingleton

        self.model = None
        self.train_loader = None
        self.test_loader = None
        self.device = None
        self.optimizer = None
        self.criterion = None


    def run(self):
        batch_size = self.hyperParametersSingleton.batchsize
        self.device = 'cuda' if cuda.is_available() else 'cpu'

        train_dataset = self._loadTrainDataset()
        test_dataset = self._loadTestDataset()

        # Data Loader
        self.train_loader = data.DataLoader(
            dataset=train_dataset,
            batch_size=batch_size,
            shuffle=True
        )

        self.test_loader = data.DataLoader(
            dataset=test_dataset,
            batch_size=batch_size,
            shuffle=False
        )

        # Instantiate the LeNet5 model and move to specified device
        self.model = self._determine_pytorch_model()
        self.model.to(self.device)

        # Loss function (cross-entropy) and optimizer with learning rate and momentum
        self.optimizer = optim.SGD(self.model.parameters(), lr=0.01, momentum=0.5)
        self.criterion = nn.CrossEntropyLoss()

        self.start_training_and_testing()

    def start_training_and_testing(self):
        since = time.time()  # Starting time of whole training
        epochs = self.hyperParametersSingleton.epochs

        for epoch in range(1, epochs + 1):
            if (self.stopFlag.is_set()):
                break

            epoch_start = time.time()  # Starting time of this epoch

            # Train and print training time of epoch
            self.train(epoch)
            m, s = divmod(time.time() - epoch_start, 60)
            print(f'Training time: {m:.0f}m {s:.0f}s')
            self.statusUpdate.emit(f'Training time: {m:.0f}m {s:.0f}s')

            # Test and print testing time of epoch
            self.test()
            m, s = divmod(time.time() - epoch_start, 60)
            print(f'Testing time: {m:.0f}m {s:.0f}s')
            self.statusUpdate.emit(f'Testing time: {m:.0f}m {s:.0f}s')

        # Print total training time
        m, s = divmod(time.time() - since, 60)
        print(f'Total Time: {m:.0f}m {s:.0f}s\nModel was trained on {self.device}!')
        self.statusUpdate.emit(f'Total Time: {m:.0f}m {s:.0f}s\nModel was trained on {self.device}!')

        # If was told to stop. Perform cleanup
        if (self.stopFlag.is_set()):
            self.cleanup_stop()

    def stop(self):
        self.stopFlag.set()

    def cleanup_stop(self):
            print("Okay I stopped. Cleanup unfinished work!")
            self.statusUpdate.emit("Okay I stopped. Cleanup unfinished work!")
            # Todo make sure data is cleaned up

    def saveModel(self, filePath):
        print("Model runner told to stop!")
        self.statusUpdate.emit("Model runner told to stop!")
        self.shouldSaveFlag.set()

    def _determine_pytorch_model(self):
        if self.hyperParametersSingleton.modelName == 'resnet':
            pass
        elif self.hyperParametersSingleton.modelName == 'lenet5':
            return LeNet5()
        else:
            print("ERR: NO model name found.")
            raise Exception("No modelname found!")

    def _loadTrainDataset(self):
        if self.hyperParametersSingleton.modelName == 'resnet':
            pass
        elif self.hyperParametersSingleton.modelName == 'lenet5':
            return  datasets.MNIST(root='./data',
                               train=True,
                               transform=transforms.ToTensor(),
                               download=True)
        else:
            print("Load Dataset Err")
            raise Exception("Load Dataset Err")

    def _loadTestDataset(self):
        if self.hyperParametersSingleton.modelName == 'resnet':
            pass
        elif self.hyperParametersSingleton.modelName == 'lenet5':
            return datasets.MNIST(root='./data',
                              train=False,
                              transform=transforms.ToTensor())
        else:
            print("Load Dataset Err")
            raise Exception("Load Dataset Err")

    # Definition of the training function
    def train(self, epoch):

        self.model.train()  # Set model to training mode

        for batch_idx, (data, target) in enumerate(self.train_loader):
            if (self.stopFlag.is_set()):
                return

            data, target = data.to(self.device), target.to(self.device)  # Move the input data and target labels
            self.optimizer.zero_grad()  # Zero out the gradients
            output = self.model(data)  # Pass data through the model
            loss = self.criterion(output, target)  # Compute loss
            loss.backward()  # Compute gradients of the loss with respect to model parameters
            self.optimizer.step()  # Update model parameters based on computed gradients and optimizer

            # Print training progress
            if batch_idx % 10 == 0:
                print('Train Epoch: {} | Batch Status: {}/{} ({:.0f}%) | Loss: {:.6f}'.format(
                    epoch, batch_idx * len(data), len(self.train_loader.dataset),
                           100. * batch_idx / len(self.train_loader), loss.item()))

                self.statusUpdate.emit('Train Epoch: {} | Batch Status: {}/{} ({:.0f}%) | Loss: {:.6f}'.format(
                    epoch, batch_idx * len(data), len(self.train_loader.dataset),
                           100. * batch_idx / len(self.train_loader), loss.item()))

    # Definition of the testing function
    def test(self):
        self.model.eval()
        test_loss = 0
        correct = 0

        for data, target in self.test_loader:
            if (self.stopFlag.is_set()):
                return


            data, target = data.to(self.device), target.to(self.device)  # Move the input data and target labels
            output = self.model(data)  # Pass data through the model
            test_loss += self.criterion(output, target).item()  # sum up batch loss
            pred = output.data.max(1, keepdim=True)[1]  # get the index of the max
            correct += pred.eq(target.data.view_as(pred)).cpu().sum()  # Sum up the correct predictions

        test_loss /= len(self.test_loader.dataset)
        print(
            f'===========================\nTest set: Average loss: {test_loss:.4f}, Accuracy: {correct}/{len(self.test_loader.dataset)} '
            f'({100. * correct / len(self.test_loader.dataset):.0f}%)')

        self.statusUpdate.emit( f'===========================\nTest set: Average loss: {test_loss:.4f}, Accuracy: {correct}/{len(self.test_loader.dataset)} '
            f'({100. * correct / len(self.test_loader.dataset):.0f}%)')

