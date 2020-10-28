import pywinauto
from pywinauto.application import Application
from pywinauto.timings import wait_until, Timings

import os, sys
import time, datetime
import statistics # 3.4+

import matplotlib.pyplot as plt
import numpy as np

def benchmark(func, N, xlabel):
    X = []
    Y = []
    for i in range(1, N+1):
        X.append(i)
        before = time.clock()
        func(i)
        Y.append(time.clock() - before)
        print('{} {}/{}'.format(xlabel, i, N))
    print('median of {}: {}'.format(xlabel, statistics.median(Y)))
    plt.plot(X, Y, 'bo')
    plt.xlabel(xlabel)
    plt.ylabel('time (ms)')
    plt.savefig('{}-{}.png'.format(xlabel.strip(), datetime.datetime.now().strftime("%Y%m%d-%H%M%S")))
    return plt

pywinauto.actionlogger.enable()
Timings.fast()

N = 5
MAX_DEPTH = 3

app = Application(backend="uia")
app.start(cmd_line=r"mainwindow.exe {} {}".format(0,0))
dlg = app.window(name="Qt Main Window Example")
dlg.wait('visible')
dlg = dlg.wrapper_object()    

print('window with 7 children elements, average depth 2, children())')
benchmark(lambda i: dlg.children(), N, 'iterations')

print('window with 7 children elements, average tree depth 2, descendants())'.format())
benchmark(lambda i: dlg.descendants(), N, 'iterations')

print('window with 7 children elements, average tree depth 2, descendants(depth={}))'.format(MAX_DEPTH))
benchmark(lambda i: dlg.descendants(depth=MAX_DEPTH), N, 'iterations')

app.kill()

app = Application(backend="uia")
app.start(cmd_line=r"mainwindow.exe {} {}".format(5,5))
dlg = app.window(name="Qt Main Window Example")
dlg.wait('visible')
dlg = dlg.wrapper_object()    

print('window with 12 children elements, average depth 7, children())')
benchmark(lambda i: dlg.children(), N, 'iterations')

print('window with 12 children elements, average tree depth 7, descendants())'.format())
benchmark(lambda i: dlg.descendants(), N, 'iterations')\

print('window with 12 children elements, average tree depth 7, descendants(depth={}))'.format(MAX_DEPTH))
benchmark(lambda i: dlg.descendants(depth=MAX_DEPTH), N, 'iterations')

app.kill()

app = Application(backend="uia")
app.start(cmd_line=r"mainwindow.exe {} {}".format(60,60))
dlg = app.window(name="Qt Main Window Example")
#dlg.wait('visible')
time.sleep(5)
dlg = dlg.wrapper_object()    

print('window with 67 children elements, average depth 62, children())')
benchmark(lambda i: dlg.children(), N, 'iterations')

print('window with 67 children elements, average tree depth 62, descendants())'.format())
benchmark(lambda i: dlg.descendants(), N, 'iterations')

print('window with 67 children elements, average tree depth 62, descendants(depth={}))'.format(MAX_DEPTH))
benchmark(lambda i: dlg.descendants(depth=MAX_DEPTH), N, 'iterations')

app.kill()

