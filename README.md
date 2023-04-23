# sign-language-recogniser
## COMPSYS 302 Project 1 - Sign Language Recognition Application
**Version 1.0**

**Date: 2023-04-23**

### Table of Contents
- Description
- Installation
- Usage
- Key Features

### Description
This project for COMPSYS 302, Semester One 2023 is a Sign Language Recognition application

### Installation 
To install this application:
1. Clone the repository to your local machine.

### Usage
To use the application:
1. Navigate to the project directory.
2. Launch the application using the following command
```
python MainUI.py
```
The user interface will be displayed which you can use to interact with the application and explore its features.

### Key Features
There are three main tabs within the application:
- **Dataset:** In this tab, you can either select the MNIST dataset or upload your own csv files, one for training and another for testing.
- **Train:** In this tab, you can filter and view images in your dataset, then continue to training your model. Select the CNN model, set the hyperparameters, and the train/validate ratio. Upon training, you should see a dialog with the progress and statistics. At the end you can save your model for testing.
- **Test:** In this tab, you can select any saved models, and either images from your dataset or capture images from the camera to predict. 
