# myo_ecn
 
Installation:

0) Install 'MyoConnect' from https://support.getmyo.com/hc/en-us/articles/360018409792. Conventional 'accept-accept-ok' installation.

1) Install 'Anaconda' for Python 3 from https://www.anaconda.com/.

2) Create a new python environment that will contain necessary dependencies. In command line, from this folder, run:
	conda env create -f ./anaconda/myo_environment.yml

3) Now activate the environment that we have just created (its name is 'myo'):
	conda activate myo

4) Install 'myo-python' package from my fork on Github. Command line:
	pip install git+https://github.com/smetanadvorak/myo-python
	
	
Running the code:
0) Open MyoConnect, and make sure that the armband is connected to it. 

1) Open command line and activate the 'myo' environment:
	conda activate myo
	
2) Navigate to this folder and run a test script:
	python emg_streaming.py

3) Run other scripts, too, if you want:
	python script_name.py
	

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
