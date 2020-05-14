import time, string
import myo
import numpy as np
import sys, os, shutil
from myo_ecn.listeners       import Collector, ConnectionChecker
    
# Define constants
EMG_SAMPLING_RATE = 200

def make_single_acquisition(trial_len, message_to_the_user = False):
    # This function performs a single acquisition EMG data for a specified amount of seconds.
    # It also guides the user to perform a specific gesture within the specified time limits.
    hub = myo.Hub()
    listener = Collector(trial_len * EMG_SAMPLING_RATE)
    if message_to_the_user:
        print(message_to_the_user)
        for i in [3,2,1]:
            print('\rAcquisition starts in %d ...' % i , end='')
            time.sleep(1.25)
    print('\rStarted recording EMG for', str(trial_len), 'seconds.')
    
    with hub.run_in_background(listener.on_event):
        while hub.running:
            time.sleep(0.250)
            print('\rRecording ... %d percent done' % (100 * listener.emg_data.shape[0]/trial_len/EMG_SAMPLING_RATE), end='')  
        print()
    return listener.emg_data


def main():
    # ================== setup myo-python (do not change) =====================
    myo.init(sdk_path='../../myo_sdk') # Compile Python binding to Myo's API
    hub = myo.Hub() # Create a Python instance of MYO API
    if not ConnectionChecker().ok: # Check connection before starting acquisition:
        quit()
    # =========================================================================

    # Parce command line inputs, if any. When running this script from command line, 
    # you can specify the target data folder:
    # python scriptname.py foldername
    if len(sys.argv) > 1:
        data_folder = sys.argv[1]
    else: 
        data_folder = 'data'
    
    # Setup classification problem and training dataset parameters
    gestures = ['fist', 'open', 'rest']#, 'pron', 'supi'] # Classes to acquire data for
    trials_n = 3  # Number of trials for each class
    trial_len = 5 # Duration of each trial in seconds


    print('Starting the EMG data collection ...')
    # Get to the dataset folder, if doesn't exist, create it:
    if not os.path.exists(data_folder): os.mkdir(data_folder)
    os.chdir(data_folder)
    # EMG data is acquired in the following order: 
    # Class1-Trial1, Class2-Trial1 ... ClassN_Trial1,
    # Class2_Trial2, Class2-Trial2 ... ... ClassN_TrialM.
    for trial in range(1, trials_n+1):
        for gesture in gestures:
            # For each class, enter or create a specific folder that contains all of its trials:
            if not os.path.exists(gesture): os.mkdir(gesture)
            os.chdir(gesture)
            # Check if such trial for this class was already recorded (useful when continuing an interrupted acquisition)
            if os.path.exists(str(trial)+'.csv'):
                print('Trial', str(trial), 'of class %s already exists, moving forward ...' % gesture.upper())
            else:
                # Make new acquisition:
                emg_data = make_single_acquisition( trial_len, 
                                                    'Start performing %s gesture.' % gesture.upper())
                # ... and save it as Comma-Separated Values (CSV):
                with open(str(trial)+'.csv', 'w') as csvfile:
                    for row in emg_data:
                        csvfile.write(', '.join(map(str,list(row)))+'\n')            
            os.chdir('..')
        
        print('Data acquistion accomplished, signals are saved in', data_folder, 'folder.')
    os.chdir('..')


if __name__ == '__main__':
    main()