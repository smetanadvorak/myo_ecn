import myo
import numpy as np
import time
import keyboard

from myo_ecn.listeners                   import ConnectionChecker
from myo_ecn.listeners                   import Buffer
from MultichannelPlot                    import MultichannelPlot 

def main():
    # ================== setup myo-python (do not change) =====================
    myo.init(sdk_path='../../myo_sdk') # Compile Python binding to Myo's API
    hub = myo.Hub() # Create a Python instance of MYO API
    if not ConnectionChecker().ok: # Check connection before starting acquisition:
        quit()
    # =========================================================================


    # Setup our custom processor of MYO's events. 
    # EmgBuffer will acquire new data in a buffer (queue):
    listener = Buffer(buffer_len = 512) # At sampling rate of 200Hz, 512 samples correspond to ~2.5 seconds of the most recent data.

    # Setup multichannel plotter for visualisation:
    plotter = MultichannelPlot(nchan = 8, xlen = 512) # Number of EMG channels in MYO armband is 8


    # Tell MYO API to start a parallel thread that will collect the data and
    # command the MYO to start sending EMG data. 
    with hub.run_in_background(listener): # This is the way to associate our listener with the MYO API.
        print('Streaming EMG ... Press shift-c to stop.')
        while hub.running:                
            time.sleep(0.040)
            # Pull recent EMG data from the buffer
            emg_data = listener.get_emg_data()
            # Transform it to numpy matrix
            emg_data = np.array([x[1] for x in emg_data])    
            # Plot it
            plotter.update_plot(emg_data.T)    
            if keyboard.is_pressed('C'):
                print('Stop.')
                break
        
        
if __name__ == '__main__':
    main()