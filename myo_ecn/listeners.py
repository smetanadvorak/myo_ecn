from collections import deque
from threading import Lock, Thread
import numpy as np
import time
import myo



class Buffer(myo.DeviceListener):
    #An instance of this class constantly collects new EMG data in a queue (buffer)
    def __init__(self, buffer_len):
        self.n = buffer_len
        self.lock = Lock()
        self.emg_data_queue = deque(maxlen=self.n)

    def get_emg_data(self):
        with self.lock:
            return list(self.emg_data_queue)

    # This function is called automatically by MYO API when
    # the armband is associated with the Hub object (basically, once per Hub's lifetime)
    def on_connected(self, event):
        event.device.stream_emg(True)
        print('Connected to MYO, hub is running...')

    # This function is called automatically by MYO API whenever
    # new EMG data has been received from the armband
    def on_emg(self, event):
        with self.lock:
            self.emg_data_queue.append((event.timestamp, event.emg))

#     def on_pose(self, event):
#         if event.pose == myo.Pose.double_tap:
#             print('Double tap detected, shutting down.')
#             return False



class Collector(myo.DeviceListener):
    #Collects EMG data for a specified amount of time
    def __init__(self, len):
        self.acquisition_len = len
        self.lock = Lock()
        self.emg_data = np.zeros((0,8))

    def on_connected(self, event):
        event.device.stream_emg(True)
        self.device = event.device

    def on_emg(self, event):
        with self.lock:
            # Make numpy matrix out of received data and concatenate with the stored data
            new_emg_data = np.array(event.emg).T
            self.emg_data = np.vstack((self.emg_data, new_emg_data))
            # Stop acquisition once required amount of data is received. Cut the excess.
            if self.emg_data.shape[0] > self.acquisition_len:
                self.emg_data = self.emg_data[:self.acquisition_len, :]
                return False #Tells to the hub object to stop transmission.


class ConnectionChecker:
    # Checks if connections to the MYO is available
    def __init__(self, timeout=5):
        self.ok = False
        checker = MyoCheckConnection(timeout)
        hub = myo.Hub()
        print('Checking if can connect to an armband ... ')
        with hub.run_in_background(checker):
            while not checker.check():
                pass
        if not checker.connected:
            print('Failed not connect to any armband. Please, check if any is paired with MYO Connect.')
            self.ok = False
        else:
            print("Successfully established connection with '%s' armband." % checker.device_name)
            self.ok = True


class MyoCheckConnection(myo.DeviceListener):
    def __init__(self, timeout=5):
        self.connected = False
        self.start = time.perf_counter()
        self.timeout = timeout
        self.device_name = None
    def on_connected(self, event):
        self.device_name = event.device_name
        self.connected = True
    def check(self):
        if self.connected or time.perf_counter() > self.start + self.timeout:
            return 1
        else:
            return 0
