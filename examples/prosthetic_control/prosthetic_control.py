import myo
import time, keyboard
import numpy as np
from TwoChannelMyocontrol import TwoChannelMyoControl
from myo_ecn.listeners    import Buffer, ConnectionChecker

from Alpes.Prosthesis import AlpesProsthesis, GRASPS

# ================== setup myo-python (do not change) =====================
myo.init(sdk_path='../../myo_sdk') # Compile Python binding to Myo's API
hub = myo.Hub() # Create a Python instance of MYO API
if not ConnectionChecker().ok: # Check connection before starting acquisition:
    quit()
# =========================================================================

EMG_SAMPLING_RATE = 200
winsec  = 0.1 # Window duration in seconds
winlen  = int(winsec * EMG_SAMPLING_RATE) # Window length in samples
extensors_chan = 3
flexors_chan = 0
listener = Buffer(buffer_len = winlen)

mc = TwoChannelMyoControl(
# Absolute values of EMG are spanned between 0 and 127.
# thresholds are approximately measure as percentage of total muscle contraction.
# thresholds[0] corresponds to flexors, thresholds[1] correspons to extensors.
                                thresholds = [10,15],
# cc_lock_duration filters out some unwanted control decisions after a co-contraction.
# cc_lock_duration is measured in number of 'winlen's (see variable above).
# Increase cc_lock_duration if unwanted motions appear after co-contraction or if
# co-contraction gets detected twice instead of once in a short amount of time.
                                cc_lock_duration = 1)

grasps = [GRASPS().CYLINDRICAL, GRASPS().LATERAL, GRASPS().PINCH]
grasp = 0

# Connect the hand to the computer and switch it on. First run after connection
# will initialise the hand. Consecutive runs won't.
p = AlpesProsthesis()
p.initialise()
p.set_grasp(grasps[grasp])
mav2command = [0.02, 0.02] #mapping from mean absolute signal to the control variable.


with hub.run_in_background(listener):
    print('Streaming EMG ... Press ctrl-c or shift-c to stop.')
    while hub.running:
        time.sleep(winsec)
        # Pull recent EMG data from the buffer
        emg_data = listener.get_emg_data()
        # Transform it to numpy matrix
        emg_data = np.array([[x[1][flexors_chan], x[1][extensors_chan]] for x in emg_data])
        # Interpret EMG, produce decision
        decision, mav = mc.decide(emg_data)

        # If co-contraction detected, change grasp
        if decision == mc.STATES['cc']:
            grasp = (grasp + 1) % len(grasps)
            print('Changing grasp to %s ...' % grasps[grasp].name)
            p.set_grasp(grasps[grasp])

        # If closing or opening intent detected, move the hand
        if decision == mc.STATES['close'] or decision == mc.STATES['open']:
            command = mav[0] * mav2command[0] - mav[1] * mav2command[1]
            command = min(1, max(-1, command))
            p.proportional_control_current(command)
            print('Opening/Closing, ', 'Command: %2.2f' % command)

        # If static intent detected, stop the hand
        if decision == mc.STATES['idle']:
            p.proportional_control_current(0)
            print('Idle', 'MAV: [%2.2f, %2.2f]' % tuple(mav), 'Tresholds: ', mc.thresholds)

        # if keyboard.is_pressed('C'):
        #     print('Stop.')
        #     break
