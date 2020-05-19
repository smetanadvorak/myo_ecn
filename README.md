# MYO toolbox for Ecole Centrale de Nantes
 
## Requirements 
Missing requirements will be installed as you follow the instructions given below. 
- _Python 3_
- _myo-python_
- _numpy_
- _scikit-learn_
- _scipy_
- _matplotlib_
- _keyboard_
- _pyserial_

## Description

This project contains Python scripts and classes that help to establish connection with Thalmic MYO armband, collect and plot EMG data, and implement a gesture recognition procedure. 

The developers of __Thalmic MYO__ have issued a C++ API that enables the users to create their own applications for the armband. After that, Niklas Rosenstein have developed __myo-python__, a Python interface for this API, using CFFI module and CPython. His implementation can be found here: https://github.com/NiklasRosenstein/myo-python. 

In this project, we build an infrastructure around __myo-python__ library that will help you develop EMG processing and EMG-based gesture recognition.
 
## Installation

### 0. Install Anaconda
If you are not familiar with Python and virtual environments, I suggest using Anaconda. Download a Python 3.7 Anaconda from [the official site](https://www.anaconda.com/products/individual) and install it. Use default installation options.

If you are familiar with virtual environments, create a new one and proceed to step __3__. 

### 1. Install MyoConnect

Download MyoConnect from Thalmic's [official web-site](https://support.getmyo.com/hc/en-us/articles/360018409792). Available for Windows and MacOS, a simple installation.

To set up MyoConnect for work, run it, then right-click on its icon in task bar, select __Preferences__, and uncheck all options in all tabs. Then, right-click on icon again, select __Application Manager__ and uncheck all options here too. 

### 2. Create a new __python 3.8__ virtual environment (explained for Anaconda):

On Windows, open __anaconda prompt__. On MacOS, run __Terminal__. Run the following commands and accept the changes:
```
conda create --name myo python=3.8 pip
```
Now activate the environment that we have just created (its name is __'myo'__):
```
conda activate myo
```
__Note:__ please remember that any time you want to run this project from a new command/terminal window, you need to activate this environment again.

### 3. Install _myo-python_ package

Install it from from our fork on Github. To do so, in command line, with 'myo' environment activated, run:
```
pip install https://github.com/smetanadvorak/myo-python/tarball/master
```
### 4. Setup the _myo-ecn_ package
[Download](https://github.com/smetanadvorak/myo_ecn/tarball/master) this project and put it in an appropriate directory on your disk. 
In command window, navigate to this project's folder and run:
```
pip install -e .
```

## How to run the code
### 1. Set up MyoConnect
This should be done only once at the beginning of your working session:

- Insert MYO's Bluetooth dongle in your USB port.
- Run MyoConnect, right-click on its icon in task bar, select __Armband Manager ...__.
- Approach the dongle with your armband. It should automatically get paired with MyoConnect.
- In MyoConnect, press 'Ping' to make sure that it is not connected to some other armband nearby. Your armband should vibrate in response to the ping.

<p align="center">
  <img width="500" src="docs/ping.png">
</p>

### 2. Setup the environment and run the code
- Open Anaconda Prompt (Windows) or Terminal (MacOS) and activate the 'myo' environment:
```
conda activate myo
```
	
- Navigate to the folder with this package, then to __./examples/streaming__ and run a test script:
```
python streaming.py
```
If everything is installed correctly, a matplotlib figure should appear with the EMG signals being traced in real time. 
This and other examples can be stopped by either pressing __ctrl-c__ (MacOS) or __shift-c__(Windows).

## Working with the examples

### 1. EMG streaming

Script [emg\_streaming.py](/examples/streaming/streaming.py) demonstrates a method to collect and plot EMG data from the armband in a real-time manner. Class [MultichannelPlot](/examples/streaming/MultichannelPlot.py) provides a solution for fast plotting of multichannel signals.

<p align="center">
  <img width="500" src="docs/streaming.png">
</p>

### 2. Acquisition to file
Script [emg\_streaming.py](/examples/acquisition/acquisition.py) demonstrates a method to collect a specified amount of EMG data from the armband and save it to a file. 
It uses Class [Collector](/myo_ecn/listeners.py). The following command will acquire the signal for 10 seconds and save it to file __filename.csv__:
```python
python acquistion.py 10 filename
```


### 3. Gesture classification
Scripts [1\_dataset_acquisition.py](/examples/classification/1_dataset_acquisition.py), [2\_training.py](/examples/classification/2_training.py) and [3\_inference.py](/examples/classification/3_inference.py) implement a three-step process of EMG data collection, classifier training and testing. A flowchart of the whole process is provided below:

<p align="center">
  <img width="1000" src="docs/gesture_recognition_workflow.png">
</p>


#### 3.a Dataset acquisition

In [1\_dataset_acquisition.py](/examples/classification/1_dataset_acquisition.py) may specify the the gestures (variable __gestures__) for which you want to collect the EMG data, as well as how many times to repeat the acquisition (variable __trials\_n__). When you run this script, it guides you through the acquisition by telling which gesture to perform and for which amount of time. The signals are automatically stored in the folder [__data__](/examples/classification/data/). 


<p align="center">
  <img width="500" src="docs/training.png">
</p>

Notes:
- If the script was aborted during data acquisition, on the next run it will continue from where it stooped.
- Empty [__data__](/examples/classification/data/) folder if you want to acquire a new dataset.
- You may expand an existing data set by augmenting __gestures__ and __trials_n__ variables.

#### 3.b Classifier training

In script [2\_training.py](/examples/classification/2_training.py) and utility file [EMG_classification.py](/examples/classification/EMG_classification.py) you may define the parameters of the feature extractor and of the classifier. Default feature is smoothed absolute signal (aka mean absolute value or MAV), default classifier is SVM. Run this code as is to see the results achieved by default setup. The resulting classification model is saved in folder [__models__](/examples/classification/data/). 

#### 3.c Inference

Script [3\_inference.py](/examples/classification/3_inference.py) takes the trained classification model and applies in real time to a newly acquired EMG data. Perform gestures in the same way you were performing them during training set acquisition (arm pose matters!). The script will output the label of the gesture in command line. 

### 4. Prosthetic control
To run this example, you will need to install [this package](https://github.com/smetanadvorak/alpes_hand_interface) in your 'myo' virtual environment. Then connect and power the robotic hand and start the script. Flexing the wrist will close the grip, while exenting will open it. Co-contract extensors and flexors at the same time to change the grip. 

### 5. _myo-python_ Examples
Folder [myo_python_examples](/examples/myo_python_examples/) contains the original examples distributed with __myo-python__. They may give you more insights on how to use this library. 

## What's next

Script [emg\_streaming.py](/examples/streaming/streaming.py) can be further modified to implement real-time signal processing, such as filtering or feature extraction. For that, one can add processing in the __while__ loop in 'streaming.py' or redefine/inherit from class EmgBuffer.

Classes __FeatureExtractor__ and __Classification_model__ in [EMG_classification.py](/examples/classification/EMG_classification.py) can be modified to implement a different classifier (ANN, for example). Modify class 'FeatureExtraction' to try other types of features. 

__Important note__: when writing your own code and adding the line that initialises the myo-python:
```python
myo.init(sdk_path='../../myo_sdk') # Compile Python binding to Myo's API
```
assign to __sdk\_path__ the relative location of __myo\_sdk__ folder which is in the root of this project. As you can see, all examples, being two directories below, refer to it as __'../../myo_sdk'__.


