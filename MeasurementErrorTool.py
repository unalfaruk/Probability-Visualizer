# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 14:27:13 2023

@author: personF
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons
import statistics

class Resistor:
    def __init__(self,ohm):
        self.ohm = ohm

class Sensor:
    def __init__(self,mean,std):
        self.inputVal = []
        self.outputVal = []
        self.err_std = std
        self.variance = std*std
        self.mean = mean        
    
    def measure(self,realVal):
        self.inputVal.append(realVal)
        self.outputVal.append(realVal+np.random.normal(self.mean,self.err_std))
        
    def meanOfResult(self):
        return np.sum(self.outputVal)/len(self.outputVal)
    
# GUI SETTINGS
# The sliders will be initialized
min_std = 0 #measurement std error
max_std = 100 #measurement std error
rep_num_max = 1000 #max num of repeat
plot_sigma = False
plot_real_val = False
plot_mean = False
    
# INIT OBJECTS
# Resistors and measurement devices (multimeters)
resistor = Resistor(355)

sensorCheap = Sensor(0,25)
sensorExpensive = Sensor(0,4)

# Initial measurement -> initial plot
for i in range(1,500):
    sensorCheap.measure(resistor.ohm)
    sensorExpensive.measure(resistor.ohm)
        
# The histograph of the measurements
fig, axs = plt.subplots(nrows=3)
axs[0].hist(sensorCheap.outputVal)

axs[0].set_title("Cheap Multimeter")
axs[0].set_ylabel("Num of Rep.")
axs[1].hist(sensorExpensive.outputVal)
axs[1].set_title("Expensive Multimeter")
axs[1].set_xlabel("ohm")
axs[1].set_ylabel("Num of Rep.")
axs[2].set_visible(False)
plt.setp(axs, xlim=(resistor.ohm-3*max_std, resistor.ohm+3*max_std))

axcolor = 'lightgoldenrodyellow'
ax_cheapSensor = plt.axes([0.38, 0.15, 0.5, 0.03], facecolor=axcolor)
ax_expensiveSensor = plt.axes([0.38, 0.1, 0.5, 0.03], facecolor=axcolor)
ax_repeatNum = plt.axes([0.38, 0.2, 0.5, 0.03], facecolor=axcolor)
ax_checkbox = plt.axes([0.10, 0.09, 0.1, 0.15])

slide_expensiveSensor = Slider(ax_expensiveSensor, 'Exp Sensor', min_std, max_std, valinit=int(sensorExpensive.err_std))
slider_cheapSensor = Slider(ax_cheapSensor, 'Cheap Sensor', min_std, max_std, valinit=int(sensorCheap.err_std))
slider_repeatNum = Slider(ax_repeatNum, 'Repeat Num', 1, rep_num_max, valinit=int(500))

labels = [r'${mean}$',r'${σ}$',r'${Val_{real}}$']
visibility = [False,False,False]
check = CheckButtons(ax_checkbox, labels, visibility)

def doMeasurement(repeatNum, resistorVal, cheapStdVal, expStdVal):
    resistor = Resistor(resistorVal)
    sensorCheap = Sensor(0,cheapStdVal)
    sensorExpensive = Sensor(0,expStdVal)
    
    # Number of measurement repeat
    for i in range(1,int(repeatNum)):
        sensorCheap.measure(resistor.ohm)
        sensorExpensive.measure(resistor.ohm)
        
    return sensorCheap.outputVal, sensorExpensive.outputVal

def updateCheap(val):
    global resistor
    cheapVal, expVal = doMeasurement(slider_repeatNum.val,resistor.ohm,slider_cheapSensor.val,slide_expensiveSensor.val)
    mean = statistics.mean(cheapVal)
    stdev = statistics.stdev(cheapVal)
    axs[0].cla()
    axs[0].hist(cheapVal)
    if(plot_real_val):
        axs[0].axvline(resistor.ohm,color = 'k')
    if(plot_mean):
        axs[0].axvline(mean,color = 'r')
    if(plot_sigma):
        axs[0].axvline(mean+stdev,color = 'm', linestyle='--')
        axs[0].axvline(mean-stdev,color = 'm', linestyle='--')
        axs[0].axvline(mean+2*stdev,color = 'y', linestyle='--')
        axs[0].axvline(mean-2*stdev,color = 'y', linestyle='--')
        axs[0].axvline(mean+3*stdev,color = 'c', linestyle='--')
        axs[0].axvline(mean-3*stdev,color = 'c', linestyle='--')
    axs[0].set_title("Cheap Multimeter")
    plt.draw()
    #hist.set_ydata(sensorCheap.outputVal)
    fig.canvas.draw_idle()
    plt.setp(axs, xlim=(resistor.ohm-3*max_std, resistor.ohm+3*max_std))
    #plt.setp(axs, xlim=axs[0].get_xlim())

def updateExp(val):
    global resistor
    cheapVal, expVal = doMeasurement(slider_repeatNum.val,resistor.ohm,slider_cheapSensor.val,slide_expensiveSensor.val)
    mean = statistics.mean(expVal)
    stdev = statistics.stdev(expVal)
    axs[1].cla()
    axs[1].hist(expVal)
    if(plot_real_val):
        axs[1].axvline(resistor.ohm,color = 'k')
    if(plot_mean):
        axs[1].axvline(mean,color = 'r')
    if(plot_sigma):
        axs[1].axvline(mean+stdev,color = 'm', linestyle='--')
        axs[1].axvline(mean-stdev,color = 'm', linestyle='--')
        axs[1].axvline(mean+2*stdev,color = 'y', linestyle='--')
        axs[1].axvline(mean-2*stdev,color = 'y', linestyle='--')
        axs[1].axvline(mean+3*stdev,color = 'c', linestyle='--')
        axs[1].axvline(mean-3*stdev,color = 'c', linestyle='--')
    axs[1].set_title("Expensive Multimeter")
    plt.draw()
    #hist.set_ydata(sensorCheap.outputVal)
    fig.canvas.draw_idle()
    plt.setp(axs, xlim=(resistor.ohm-3*max_std, resistor.ohm+3*max_std))
    #plt.setp(axs, xlim=axs[0].get_xlim())
    
def updateBoth(val):
    updateCheap(val)
    updateExp(val)
    
def checked(label):
    global plot_mean
    global plot_sigma
    global plot_real_val
    index = labels.index(label)
    if index == 0:
        plot_mean = not plot_mean
    elif index == 1:
        plot_sigma = not plot_sigma
    elif index == 2:
        plot_real_val = not plot_real_val
    updateBoth(None)
    #lines[index].set_visible(not lines[index].get_visible())
    #plt.draw()

check.on_clicked(checked)
slider_cheapSensor.on_changed(updateCheap)
slide_expensiveSensor.on_changed(updateExp)
slider_repeatNum.on_changed(updateBoth)

def resetSlider(event):
    slider_cheapSensor.reset()
    slide_expensiveSensor.reset()
    slider_repeatNum.reset()

fig.tight_layout()
plt.show()


