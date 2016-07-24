# -*- coding: utf-8 -*-
"""
Various methods of drawing scrolling plots.
"""
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

win = pg.GraphicsWindow()
win.setWindowTitle('Scrolling Plots')

chunkSize = 100
# Remove chunks after we have 10
maxChunks = 10
startTime = pg.ptime.time()
win.nextRow()
p5 = win.addPlot(colspan=2)
p5.setLabel('bottom', 'Time', 's')
p5.setXRange(-10, 0)
curves = []
data5 = np.empty((chunkSize+1, 2))
ptr5 = 0


def new_data(data):
    global p5, data5, ptr5, curves
    now = pg.ptime.time()
    for c in curves:
        c.setPos(-(now-startTime), 0)

    i = ptr5 % chunkSize
    if i == 0:
        curve = p5.plot()
        curves.append(curve)
        last = data5[-1]
        data5 = np.empty((chunkSize+1, 2))
        data5[0] = last
        while len(curves) > maxChunks:
            c = curves.pop(0)
            p5.removeItem(c)
    else:
        curve = curves[-1]
    data5[i+1, 0] = now - startTime
    data5[i+1, 1] = data
    curve.setData(x=data5[:i+2, 0], y=data5[:i+2, 1])
    ptr5 += 1


# update all plots
def update():
    new_data(np.random.rand())

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)


if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
