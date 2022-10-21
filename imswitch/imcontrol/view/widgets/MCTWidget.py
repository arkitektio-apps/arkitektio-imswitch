import numpy as np
import pyqtgraph as pg
from qtpy import QtCore, QtWidgets

from imswitch.imcontrol.view import guitools
from .basewidgets import NapariHybridWidget


class MCTWidget(NapariHybridWidget):
    """ Widget containing mct interface. """


    sigMCTInitFilterPos = QtCore.Signal(bool)  # (enabled)
    sigMCTShowLast = QtCore.Signal(bool)  # (enabled)
    sigMCTStop = QtCore.Signal(bool)  # (enabled)
    sigMCTStart = QtCore.Signal(bool)  # (enabled)


    sigShowToggled = QtCore.Signal(bool)  # (enabled)
    sigPIDToggled = QtCore.Signal(bool)  # (enabled)
    sigUpdateRateChanged = QtCore.Signal(float)  # (rate)
    
    
    sigSliderLaser2ValueChanged = QtCore.Signal(float)  # (value)
    sigSliderLaser1ValueChanged = QtCore.Signal(float)  # (value)
    sigSliderLEDValueChanged = QtCore.Signal(float)  # (value)

    def __post_init__(self):
        #super().__init__(*args, **kwargs)


        self.mctFrame = pg.GraphicsLayoutWidget()
        
        # initialize all GUI elements
        
        # period
        self.mctLabelTimePeriod  = QtWidgets.QLabel('Period T (s):')
        self.mctValueTimePeriod = QtWidgets.QLineEdit('5')
        
        # duration
        self.mctLabelTimeDuration  = QtWidgets.QLabel('N Measurements:')
        self.mctValueTimeDuration = QtWidgets.QLineEdit('1')
        
        # z-stack
        self.mctLabelZStack  = QtWidgets.QLabel('Z-Stack (min,max,steps):')        
        self.mctValueZmin = QtWidgets.QLineEdit('-100')
        self.mctValueZmax = QtWidgets.QLineEdit('100')
        self.mctValueZsteps = QtWidgets.QLineEdit('10')
        
        # autofocus
        self.autofocusLabel = QtWidgets.QLabel('Autofocus (range, steps, every n-th measurement): ')        
        self.autofocusRange = QtWidgets.QLineEdit('200')
        self.autofocusSteps = QtWidgets.QLineEdit('20')
        self.autofocusPeriod = QtWidgets.QLineEdit('10')
        
        self.autofocusLaser1Checkbox = QtWidgets.QCheckBox('Laser 1')
        self.autofocusLaser1Checkbox.setCheckable(True)
        
        self.autofocusLaser2Checkbox = QtWidgets.QCheckBox('Laser 2')
        self.autofocusLaser2Checkbox.setCheckable(True)
        
        self.autofocusLED1Checkbox = QtWidgets.QCheckBox('LED 1')
        self.autofocusLED1Checkbox.setCheckable(True)
        
        self.autofocusSelectionLabel = QtWidgets.QLabel('Lightsource for AF:')        
        
        
        # Laser 1
        valueDecimalsLaser = 1
        valueRangeLaser = (0,2**15)
        tickIntervalLaser = 1
        singleStepLaser = 1
        
        self.sliderLaser1, self.mctLabelLaser1 = self.setupSliderGui('Intensity (Laser 1):', valueDecimalsLaser, valueRangeLaser, tickIntervalLaser, singleStepLaser)
        self.sliderLaser1.valueChanged.connect(
            lambda value: self.sigSliderLaser1ValueChanged.emit(value)
        )
        
        self.sliderLaser2, self.mctLabelLaser2 = self.setupSliderGui('Intensity (Laser 2):', valueDecimalsLaser, valueRangeLaser, tickIntervalLaser, singleStepLaser)
        self.sliderLaser2.valueChanged.connect(
            lambda value: self.sigSliderLaser2ValueChanged.emit(value)
        )
                        
        # LED
        valueDecimalsLED = 1
        valueRangeLED = (0,2**8)
        tickIntervalLED = 1
        singleStepLED = 1
        
        self.sliderLED, self.mctLabelLED = self.setupSliderGui('Intensity (LED):', valueDecimalsLED, valueRangeLED, tickIntervalLED, singleStepLED)
        self.sliderLED.valueChanged.connect(
            lambda value: self.sigSliderLEDValueChanged.emit(value)
        )
        
        self.mctLabelFileName  = QtWidgets.QLabel('FileName:')
        self.mctEditFileName  = QtWidgets.QLineEdit('MCT')
        self.mctNImages  = QtWidgets.QLabel('Number of images: ')

        self.mctStartButton = guitools.BetterPushButton('Start')
        self.mctStartButton.setCheckable(False)
        self.mctStartButton.toggled.connect(self.sigMCTStart)

        self.mctStopButton = guitools.BetterPushButton('Stop')
        self.mctStopButton.setCheckable(False)
        self.mctStopButton.toggled.connect(self.sigMCTStop)

        self.mctShowLastButton = guitools.BetterPushButton('Show Last')
        self.mctShowLastButton.setCheckable(False)
        self.mctShowLastButton.toggled.connect(self.sigMCTShowLast)

        self.mctInitFilterButton = guitools.BetterPushButton('Init Filter Pos.')
        self.mctInitFilterButton.setCheckable(False)
        self.mctInitFilterButton.toggled.connect(self.sigMCTInitFilterPos)
        
        self.mctDoZStack = QtWidgets.QCheckBox('Perform Z-Stack')
        self.mctDoZStack.setCheckable(True)
        
        # Defining layout
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        self.grid.addWidget(self.mctLabelTimePeriod, 0, 0, 1, 1)
        self.grid.addWidget(self.mctValueTimePeriod, 0, 1, 1, 1)
        self.grid.addWidget(self.mctLabelTimeDuration, 0, 2, 1, 1)
        self.grid.addWidget(self.mctValueTimeDuration, 0, 3, 1, 1)
        self.grid.addWidget(self.mctLabelZStack, 1, 0, 1, 1)
        self.grid.addWidget(self.mctValueZmin, 1, 1, 1, 1)
        self.grid.addWidget(self.mctValueZmax, 1, 2, 1, 1)
        self.grid.addWidget(self.mctValueZsteps, 1, 3, 1, 1)
        self.grid.addWidget(self.mctLabelLaser1, 2, 0, 1, 1)
        self.grid.addWidget(self.sliderLaser1, 2, 1, 1, 3)
        self.grid.addWidget(self.mctLabelLaser2, 3, 0, 1, 1)
        self.grid.addWidget(self.sliderLaser2, 3, 1, 1, 3)        
        self.grid.addWidget(self.mctLabelLED, 4, 0, 1, 1)
        self.grid.addWidget(self.sliderLED, 4, 1, 1, 3)

        self.grid.addWidget(self.mctLabelFileName, 5, 0, 1, 1)
        self.grid.addWidget(self.mctEditFileName, 5, 1, 1, 1)
        self.grid.addWidget(self.mctNImages, 5, 2, 1, 1)
        self.grid.addWidget(self.mctStartButton, 8, 0, 1, 1)
        self.grid.addWidget(self.mctStopButton, 8, 1, 1, 1)
        self.grid.addWidget(self.mctShowLastButton,8, 2, 1, 1)
        self.grid.addWidget(self.mctInitFilterButton,8, 3, 1, 1)
        
        self.grid.addWidget(self.mctDoZStack, 5, 3, 1, 1)

        self.grid.addWidget(self.autofocusLabel, 6, 0, 1, 1)
        self.grid.addWidget(self.autofocusRange, 6, 1, 1, 1)
        self.grid.addWidget(self.autofocusSteps, 6, 2, 1, 1)
        self.grid.addWidget(self.autofocusPeriod, 6, 3, 1, 1)
        
        self.grid.addWidget(self.autofocusSelectionLabel, 7, 0, 1, 1)        
        self.grid.addWidget(self.autofocusLaser1Checkbox, 7, 1, 1, 1)
        self.grid.addWidget(self.autofocusLaser2Checkbox, 7, 2, 1, 1)
        self.grid.addWidget(self.autofocusLED1Checkbox, 7, 3, 1, 1)
        
        self.layer = None
        
        
    def isAutofocus(self):
        if self.autofocusLED1Checkbox.isChecked() or self.autofocusLaser1Checkbox.isChecked() or self.autofocusLaser2Checkbox.isChecked():
            return True
        else:
            return False
        
    def getAutofocusValues(self):
        autofocusParams = {}
        autofocusParams["valueRange"] = self.autofocusRange.text()
        autofocusParams["valueSteps"] = self.autofocusSteps.text()
        autofocusParams["valuePeriod"] = self.autofocusPeriod.text()
        if self.autofocusLED1Checkbox.isChecked():
            autofocusParams["illuMethod"] = 'LED'
        elif self.autofocusLaser1Checkbox.isChecked():
            autofocusParams["illuMethod"] = 'Laser1'
        elif self.autofocusLaser2Checkbox.isChecked():
            autofocusParams["illuMethod"] = 'Laser2'
        else:
            autofocusParams["illuMethod"] = False
        
        return autofocusParams
 
 
    def setupSliderGui(self, label, valueDecimals, valueRange, tickInterval, singleStep):
        mctLabel  = QtWidgets.QLabel(label)     
        valueRangeMin, valueRangeMax = valueRange
        slider = guitools.FloatSlider(QtCore.Qt.Horizontal, self, allowScrollChanges=False,
                                        decimals=valueDecimals)
        slider.setFocusPolicy(QtCore.Qt.NoFocus)
        slider.setMinimum(valueRangeMin)
        slider.setMaximum(valueRangeMax)
        slider.setTickInterval(tickInterval)
        slider.setSingleStep(singleStep)
        slider.setValue(0)
        return slider, mctLabel
        
    def getImage(self):
        if self.layer is not None:
            return self.img.image
        
    def setImage(self, im, colormap="gray", name="", pixelsizeZ=1):
        if self.layer is None or name not in self.viewer.layers:
            self.layer = self.viewer.add_image(im, rgb=False, colormap=colormap, 
                                               scale=(1, 1, pixelsizeZ),
                                               name=name, blending='additive')
        self.layer.data = im
        
        
    def getZStackValues(self):
        valueZmin = -abs(float(self.mctValueZmin.text()))
        valueZmax = float(self.mctValueZmax.text())
        valueZsteps = float(self.mctValueZsteps.text())
        valueZenabled = bool(self.mctDoZStack.isChecked())
        
        return valueZmin, valueZmax, valueZsteps, valueZenabled
 
    def getTimelapseValues(self):
        mctValueTimePeriod = float(self.mctValueTimePeriod.text())
        mctValueTimeDuration = int(self.mctValueTimeDuration.text())
        return mctValueTimePeriod, mctValueTimeDuration
    
    def getFilename(self):
        mctEditFileName = self.mctEditFileName.text()
        return mctEditFileName
    
    def setNImages(self, nImages):
        nImages2Do = self.getTimelapseValues()[-1]
        self.mctNImages.setText('Number of images: '+str(nImages) + " / " + str(nImages2Do))
    
    
    
        
# Copyright (C) 2020-2021 ImSwitch developers
# This file is part of ImSwitch.
#
# ImSwitch is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ImSwitch is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
