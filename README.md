# MYO toolbox for Ecole Centrale de Nantes
 
## Requirements 
- Python 3

The following dependencies will be installed as you follow the installation instructions given below: 
- myo-python
- numpy
- scikit-learn
- matplotlib

 
## Installation

### 1. Install 'MyoConnect' 

Download MyoConnect from Thalmic's [official web-site](https://support.getmyo.com/hc/en-us/articles/360018409792). Available for Windows and MacOS, a simple installation.

### 2a. New python environment (With Anaconda)

In command line, navigate to the folder with this package. Then run the following command:
```
conda env create -f ./anaconda/myo_environment.yml
```

Now activate the environment that we have just created (its name is 'myo'):
```
conda activate myo
```
__Note:__ please remember that any time you want to run this code from a new command/terminal window, you need to activate the 'myo' environment again.

### 2b. New python environment (Without Anaconda)

...

__Note:__ please remember that any time you want to run this code from a new command/terminal window, you need to activate the 'myo' environment again.

### 3. Install 'myo-python' package

Install it from from my fork on Github. In command line, with 'myo' environment activated, run:
```
pip install git+https://github.com/smetanadvorak/myo-python
```

## How to run the code
First, part with MyoConnect, this should be done once before starting working:
- Insert the Bluetooth dongle in your USB port.
- Run MyoConnect and approach the dongle with your armband. It should automatically get paired with MyoConnect.
- Press 'Ping' to make sure that it not connected to another nearby armband. Your armband should vibrate in response to the ping.

Second, setup the environment and run the code:
- Open command line and activate the 'myo' environment:
```
conda activate myo
```
	
- Navigate to the folder with this package, then to __./examples/streaming__ and run a test script:
```
python emg_streaming.py
```
If everything is installed correctly, a matplotlib figure should appear with the EMG signals being traced in real time. This and other examples can be stopped by either pressing __ctrl-c__  or quicky tapping your middle and thumb fingers against each other twice.
	

General info:

These codes demonstrate the usage of 'myo-python' library in order to establish the connection with a MYO armband and collect data from it. 
Historically, the developers of MYO armband have issued an official C++ API to enable the users to create their own armband-based applications. Not long after that, programmer Niklas Rosenstein have developed a Python interface for this API, using CFFI module and CPython. His interface can be found here: https://github.com/NiklasRosenstein/myo-python. In this case, it is installed in step 3) of the afore-presented instructions.
Script 'emg_streaming.py' demonstrates a way to collect and plot EMG data from an armband in a real-time manner. Simply run it to see the results. This code is commented in a detailed way to help understand its' logic.
Scripts '1_dataset_acquisition.py', '2_training.py' and '3_inference.py' implement a three-step process of EMG data collection, classifier training and testing. Run them one after another.

All afore-mentioned scripts share a number of classes declared in files '_EmgClasses.py' and '_MyoListeners.py'. 
'_MyoListeners.py' contains classes 'EmgBuffer' and 'EmgCollector' that realize basic modes of signal acquisition: real-time buffering (see 'emg_streaming.py', '3_inference.py') and single batch (see '1_dataset_acquisition.py'). 
'_EmgClasses.py' contains classes 'MultichannelPlot' and 'FeatureExtractor'. The first helps to plot general multichannel data in an efficient way, its example can be seen in 'emg_streaming.py'. The second encapsulates the feature extraction functions and automates their application to the EMG signals (see '2_training.py'). 


What's next:

Presented codes are barebones for classic machine learning and signal processing problems. 
Script 'emg_streaming.py' can be further modified to implement real-time signal processing, such as filtering or feature extraction. For that, one can add processing in the while loop in 'emg_streaming.py' or redefine/inherit from class EmgBuffer.  
Script '2_training.py' can be modified to implement a different classifier. Modify class 'FeatureExtraction' if other types of features are needed. 
