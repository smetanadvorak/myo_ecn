import sys, time, string
import myo
import numpy as np
from myo_ecn.listeners       import Collector, ConnectionChecker

 # This script performs a single acquisition EMG data for a specified amount of seconds.
 # Number of seconds and output file name can be specified as arguments when running the script:
 # python acquisition.py 10 filename
 # Output format: .csv

EMG_SAMPLING_RATE = 200

def main():
    # ================== setup myo-python (do not change) =====================
    myo.init(sdk_path='../../myo_sdk') # Compile Python binding to Myo's API
    hub = myo.Hub() # Create a Python instance of MYO API
    if not ConnectionChecker().ok: # Check connection before starting acquisition:
        quit()
    # =========================================================================

    # Parce command line inputs, if any
    filename = 'emg'
    acquisition_len = 10
    if len(sys.argv) > 1:
        acquisition_len = int(sys.argv[1])
    if len(sys.argv) > 2:
        filename = sys.argv[2]

    listener = Collector(acquisition_len * EMG_SAMPLING_RATE)

    print('\rStarted recording EMG for', str(acquisition_len), 'seconds. Cancel with ctrl-c.')

    with hub.run_in_background(listener.on_event):
        while hub.running:
            time.sleep(0.5)
            print('\rRecording ... %d percent done.' % (100 * listener.emg_data.shape[0]/acquisition_len/EMG_SAMPLING_RATE), end='')  
        print()


    with open(filename+'.csv', 'w') as csvfile:
        for row in listener.emg_data:
            csvfile.write(', '.join(map(str,list(row)))+'\n')    
            
            
if __name__ == '__main__':
    main() 