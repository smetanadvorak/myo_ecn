import numpy as np
from matplotlib import pyplot as plt


class MultichannelPlot(object):
    # Plots multidimensional signals in a real-time fashion
    def __init__(self, nchan=8, xlen=512):
        self.nchan = nchan
        self.xlen = xlen
        self.fig = plt.figure(figsize=(10,8))
        self.axes = [self.fig.add_subplot(str(self.nchan) + '1' + str(i+1)) for i in range(self.nchan)]
        for (i,ax) in enumerate(self.axes):
            plt.sca(ax)
            plt.ylabel('Ch.%d' % (i+1))
        self.set_ylim([-128, 128])
        self.graphs = [ax.plot(np.arange(self.xlen), np.zeros(self.xlen))[0] for ax in self.axes]
    
    def set_ylim(self, lims):
        [(ax.set_ylim(lims)) for ax in self.axes]
        
    def update_plot(self, sig):
        for g, data in zip(self.graphs, sig):
            if len(data) < self.xlen:
                # Pad the left side with zeroes if not enough data to fill the axis
                data = np.concatenate([np.zeros(self.xlen - len(data)), data])
            if len(data) > self.xlen:
                data = data[-self.xlen:]
            g.set_ydata(data)
        plt.draw()
        plt.pause(0.040)