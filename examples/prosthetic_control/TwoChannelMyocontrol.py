import numpy as np

class TwoChannelMyoControl:

    STATES        = {'idle':0, 'close':1, 'open':2, 'cc':3} # 'cc' stands for co-contraction

    def __init__(self, thresholds = [10,20], cc_lock_duration = 2):
        self.thresholds = thresholds
        self.cc_lock_duration = cc_lock_duration
        self.cc_lock_timer = self.cc_lock_duration + 1

    def decide(self, emg):
        if len(emg)==0:
            return self.STATES['idle'], [0, 0]

        mav = self.mav(emg)
        # If co-contraction occured recently, lock output to 'idle' for some time,
        # to filter out other detected co-contractions and stuff detected during
        # the return from co-contraction.
        if self.cc_lock_timer <= self.cc_lock_duration:
            self.cc_lock_timer += 1
            return self.STATES['idle'], mav
        else:
            decision = self.decode_intent(mav)
            if decision == self.STATES['cc']:
                self.cc_lock_timer = 0
            return decision, mav


    def decode_intent(self, mav):
        above_below_threshold = [mav[i] > self.thresholds[i] for i in range(len(mav))]
        # Binary mapping that gives:
        # '0' for 'idle', '1' for 'up',
        # '2' for 'down', '3' for co-contraction:
        return above_below_threshold[0] + 2 * above_below_threshold[1]

    def mav(self, sig):
        res = abs(sig).mean(axis=0)
        return res.tolist()
