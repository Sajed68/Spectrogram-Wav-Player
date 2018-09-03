# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtGui import QPen, QColor, QBrush, QLinearGradient
from PyQt5.QtCore import QRectF, QRect, QPointF, QTimer
from PyQt5.QtWidgets import QWidget, QGridLayout, QGraphicsView, QPushButton, QGraphicsScene, QSlider, QGraphicsDropShadowEffect, QDial, QStackedWidget, QListWidget, QFileDialog, QListWidgetItem, QCheckBox, QLabel, QTabWidget, QRadioButton, QGroupBox, QLCDNumber, QHBoxLayout, QDoubleSpinBox, QSpinBox
from PyQt5.Qt import QPixmap, QImage, QPolygonF, QSize
import numpy as np
import pyaudio
from PIL import Image
from scipy.io import wavfile
from os import listdir
import coreprocessor


class Ui_MainWindow(QWidget):
    def __init__(self, audio=None):
        super(Ui_MainWindow, self).__init__()
        self.setWindowTitle("Player")
        self.resize(720, 460)
        #self.setMaximumSize(QtCore.QSize(720, 460))
        
        #self.timer = QTimer(self)
        #self.timer.timeout.connect(self.animate)
        #self.timer.start(1)
        
        self.layout = QHBoxLayout()
        self.setLayout(self.layout) 
        
        
        self.AudioFrame = QGraphicsView()
        #self.AudioFrame.setMaximumSize(QSize(192,120))
        
        
        self.page1 = QWidget(None)
        self.page1.layout = QGridLayout()
        self.page1.setLayout(self.page1.layout)
        
        self.go_next_page_B = QPushButton('>')
        self.go_next_page_B.setStyleSheet('border-radius:30')
        self.go_next_page_B.clicked.connect(self.go_next_page)
        #self.go_next_page_B.setMaximumSize(QSize(93,18))
        
        self.page2 = QWidget(None)
        self.page2.layout = QGridLayout()
        self.page2.setLayout(self.page2.layout)
        
        self.go_prev_page_B = QPushButton('<')
        self.go_prev_page_B.setStyleSheet('border-radius:30')
        self.go_prev_page_B.clicked.connect(self.go_prev_page)
        #self.go_prev_page_B.setMaximumSize(QSize(93,18))
        
        
        self.Volume_Dial = QDial(None)
        self.vl = 100
        self.Volume_Dial.setRange(0,100)
        self.Volume_Dial.setValue(self.vl-1)
        self.Volume_Dial.valueChanged.connect(self.volumeChange)
        
        self.page1.layout.addWidget(self.Volume_Dial, 0, 1, 2, 2)
        
        self.playSymbolChar = '▶️' 
        self.pauseSymbolChar = '⏸'#'🛠'
        self.Play = QPushButton(self.playSymbolChar)
        self.Play.setStyleSheet("QPushButton{border: 2px solid #8f8f91;border-radius: 30px;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #f6f7fa, stop: 1 #dadbde);min-width: 30px;width = 30px;}\nQPushButton:pressed {background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2:1,stop: 0 #dadbde, stop: 1 #f6f7fa);}\nQPushButton:flat {border: none;}\nQPushButton:default {border-color: navy;}")

        self.Play.clicked.connect(self.toggleplaypause)
        
        self.page1.layout.addWidget(self.Play, 0, 3, 1,1)
        
        self.nextAudio =  QPushButton('▼')
        self.nextAudio.setStyleSheet("QPushButton{border: 2px solid #8f8f91;border-radius: 30px;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #f6f7fa, stop: 1 #dadbde);min-width: 30px;width = 30px;}\nQPushButton:pressed {background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2:1,stop: 0 #dadbde, stop: 1 #f6f7fa);}\nQPushButton:flat {border: none;}\nQPushButton:default {border-color: navy;}")

        self.page1.layout.addWidget(self.nextAudio, 1, 3, 1,1)
        self.nextAudio.clicked.connect(self.next_audio)
        
        self.prevAudio =  QPushButton('▲')
        self.prevAudio.setStyleSheet("QPushButton{border: 2px solid #8f8f91;border-radius: 30px;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #f6f7fa, stop: 1 #dadbde);min-width: 30px;width = 30px;}\nQPushButton:pressed {background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2:1,stop: 0 #dadbde, stop: 1 #f6f7fa);}\nQPushButton:flat {border: none;}\nQPushButton:default {border-color: navy;}")

        self.page1.layout.addWidget(self.prevAudio, 1, 0, 1,1)
        self.prevAudio.clicked.connect(self.previous_audio)
        
        self.playList =  QPushButton('░')
        self.playList.setStyleSheet("QPushButton{border: 2px solid #8f8f91;border-radius: 30px;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #f6f7fa, stop: 1 #dadbde);min-width: 30px;width = 30px;}\nQPushButton:pressed {background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2:1,stop: 0 #dadbde, stop: 1 #f6f7fa);}\nQPushButton:flat {border: none;}\nQPushButton:default {border-color: navy;}")
        
        self.page1.layout.addWidget(self.playList, 0, 0, 1,1)
        
        self.playList.clicked.connect(self.toggleplaylistview)
        
        
        self.settingsB = QPushButton('⚙️')
        self.settingsB.setStyleSheet("QPushButton{border: 2px solid #8f8f91;border-radius: 30px;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #f6f7fa, stop: 1 #dadbde);min-width: 30px;width = 30px;}\nQPushButton:pressed {background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2:1,stop: 0 #dadbde, stop: 1 #f6f7fa);}\nQPushButton:flat {border: none;}\nQPushButton:default {border-color: navy;}")
        self.page2.layout.addWidget(self.settingsB, 0,0,1,1)
        self.settingsB.clicked.connect(self.Processors)
        
        self.exploreB = QPushButton('🔍')
        self.exploreB.setStyleSheet("QPushButton{border: 2px solid #8f8f91;border-radius: 30px;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #f6f7fa, stop: 1 #dadbde);min-width: 30px;width = 30px;}\nQPushButton:pressed {background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2:1,stop: 0 #dadbde, stop: 1 #f6f7fa);}\nQPushButton:flat {border: none;}\nQPushButton:default {border-color: navy;}")
        self.page2.layout.addWidget(self.exploreB, 0,1,1,1)
        self.exploreB.clicked.connect(self.Opennewfile)
        
        
        self.voiceremove_B = QPushButton('👂')
        self.voiceremove_B.setCheckable(True)
        self.page2.layout.addWidget(self.voiceremove_B, 1, 0, 1, -1)
        
        
        self.Listplaylist = QListWidget()
        self.isshowplaylist = True
        self.Listplaylist.itemPressed.connect(self.getNewFromPlayList)
        #self.Listplaylist.setMaximumSize(QSize(740, 305))
        
        
        self.ControlFrame = QStackedWidget()
        self.ControlFrame.addWidget(self.page1)
        self.ControlFrame.addWidget(self.page2)
        self.ControlFrame.setCurrentIndex(0)
        #self.ControlFrame.setMaximumSize(QSize(192,120))
        
        
        self.scene = QGraphicsScene()
        self.AudioFrame.setScene(self.scene)
        
        self.audio_progress = QSlider(0x1)
        self.audio_progress.setMinimum(0)
        self.audio_progress.valueChanged.connect(self.jump_audio)
        self.audio_progress.setStyleSheet('QSlider::groove:horizontal{border: 0px solid rgb(0, 255, 255);height: 1px;margin: 2px 0;}QSlider::handle:horizontal {background: rgb(170,0,0);border: 2px solid rgb(170,0,0);width: 8px;height: 2px;margin: -2px 0;border-radius: 3px;}QSlider::sub-page:vertical, QSlider::add-page:horizontal {	background: #353535;}QSlider::add-page:vertical, QSlider::sub-page:horizontal {background: rgb(0, 255, 255);}')
        #self.audio_progress.setMaximumSize(QSize(192,20))
        
        
        effect = QGraphicsDropShadowEffect();effect.setBlurRadius(5);effect.setXOffset(0);effect.setYOffset(5);effect.setColor(QColor(10,170,170));
        self.AudioFrame.setGraphicsEffect(effect)
        #effect = QGraphicsDropShadowEffect();effect.setBlurRadius(5);effect.setXOffset(0);effect.setYOffset(5);effect.setColor(QColor(10,170,170));
        #self.audio_progress.setGraphicsEffect(effect)
        effect = QGraphicsDropShadowEffect();effect.setBlurRadius(5);effect.setXOffset(0);effect.setYOffset(5);effect.setColor(QColor(10,170,170));
        self.Play.setGraphicsEffect(effect)
        effect = QGraphicsDropShadowEffect();effect.setBlurRadius(5);effect.setXOffset(0);effect.setYOffset(5);effect.setColor(QColor(10,170,170));
        self.playList.setGraphicsEffect(effect)
        effect = QGraphicsDropShadowEffect();effect.setBlurRadius(5);effect.setXOffset(0);effect.setYOffset(5);effect.setColor(QColor(10,170,170));
        self.prevAudio.setGraphicsEffect(effect)
        effect = QGraphicsDropShadowEffect();effect.setBlurRadius(5);effect.setXOffset(0);effect.setYOffset(5);effect.setColor(QColor(10,170,170));
        self.nextAudio.setGraphicsEffect(effect)
        effect = QGraphicsDropShadowEffect();effect.setBlurRadius(5);effect.setXOffset(0);effect.setYOffset(5);effect.setColor(QColor(10,170,170));
        self.ControlFrame.setGraphicsEffect(effect)
        
        self.AudioFrame.setStyleSheet('background-color :rgba(89, 233, 255, 255)')
        self.setStyleSheet('background-color: rgba(33, 91, 176, 100)')
        
        
        '''Processors:'''
        self.processor_frame = QGroupBox()
        self.processor_frame.layout = QGridLayout()
        self.processor_frame.setMinimumWidth(1000)
        self.processor_frame.setLayout(self.processor_frame.layout)

        self.isshowprocess = False
        self.processor_frame.setVisible(self.isshowprocess)
        
        self.processors_stack = QTabWidget()
        self.processor_frame.layout.addWidget(self.processors_stack, 0, 0, -1, -1)
        
        ## phase shift and time stretching:
        self.phaseshift_page = QWidget()
        self.phaseshift_page.layout = QGridLayout()
        self.phaseshift_page.setLayout(self.phaseshift_page.layout)
        self.phaseshift_slider = QSlider(0x01)
        self.phaseshift_slider.setStyleSheet('QSlider::groove:horizontal{border: 2px solid rgb(0, 255, 255);background: rgb(0,255,255);height: 5px;margin: 2px 0;}QSlider::handle:horizontal {background: rgb(170,0,0);border: 2px solid rgb(170,0,0);width: 8px;height: 2px;margin: -2px 0;border-radius: 3px;}')
        self.phaseshift_slider.valueChanged.connect(self.phaseshift_slider_change)
        self.phaseshift_slider.setRange(-800, 800)
        self.phaseshift_slider.setValue(0)
        self.phaseshift_slider.setTickInterval(50)
        self.phaseshift_slider_2 = QSlider(0x01)
        self.phaseshift_slider_2.setRange(-800, 800)
        self.phaseshift_slider_2.setValue(800)
        self.phaseshift_slider_2.setTickInterval(50)
        self.phaseshift_slider_2.setTickPosition(QSlider.TicksBothSides)
        

        self.phaseshift_slider.setValue(0)
        self.phaseshift_label = QLabel(str(self.phaseshift_slider.value()))
        
        self.phaseshift_check = QCheckBox('Enable')
        self.phaseshift_check.setEnabled(False)
        self.timestretch_check = QCheckBox('Do Time Stretching')
        self.timestretch_check.setEnabled(False)
        
        self.phaseshift_check.stateChanged.connect(self.do_phaseshifting)
        
        self.phaseshift_page.layout.addWidget(self.phaseshift_slider_2, 0, 0, 1, 2)
        self.phaseshift_page.layout.addWidget(self.phaseshift_slider, 0, 0, 1, 2)
        self.phaseshift_page.layout.addWidget(self.phaseshift_label, 0, 2, 1, 1)
        self.phaseshift_page.layout.addWidget(self.timestretch_check, 1, 0, 1, 1)
        self.phaseshift_page.layout.addWidget(self.phaseshift_check, 1, 1, 1, 1)
        
        self.processors_stack.addTab(self.phaseshift_page, 'Phase shift & Time Stretch')
        
        
        ## reverbation:
        self.reverbation_page = QWidget()
        self.reverbation_page.layout = QGridLayout()
        self.reverbation_page.setLayout(self.reverbation_page.layout)
        self.processors_stack.addTab(self.reverbation_page, 'Reverbation')
        
        self.reverb_simple_group = QGroupBox('Simple reverbation:')
        self.reverb_simple_group.layout = QGridLayout()
        self.reverb_simple_group.setLayout(self.reverb_simple_group.layout)
        
        self.reverb_simple_check = QCheckBox('Enable')
        self.reverb_simple_check.setEnabled(True)
        self.reverbator, self.reverb_simple_zp, self.reverb_simple_length = coreprocessor.Reverb(reverb_zp=2, reverb_length=2500)
        self.reverb_simple_group.layout.addWidget(self.reverb_simple_check,1, 4, 1, -1)
        
        
        self.reverb_simple_check.stateChanged.connect(self.do_simple_reverbation)
        self.reverb_simple_zp_spinbox = QDoubleSpinBox()
        self.reverb_simple_zp_label = QLabel('zero/pole:')
        self.reverb_simple_length_spinbox = QSpinBox()
        self.reverb_simple_length_label = QLabel('order:')
        self.reverb_simple_zp_spinbox.valueChanged.connect(self.get_zp_simple_reverb)
        self.reverb_simple_zp_spinbox.setValue(2)
        self.reverb_simple_zp_spinbox.setRange(1.001, 5)
        self.reverb_simple_zp_spinbox.setSingleStep(0.01)
        self.reverb_simple_length_spinbox.setRange(1000, 2500)
        self.reverb_simple_length_spinbox.valueChanged.connect(self.get_len_simple_reverb)
        self.reverb_simple_length_spinbox.setValue(2500)
        self.reverb_simple_length_spinbox.setSingleStep(100)
        self.reverb_simple_group.layout.addWidget(self.reverb_simple_zp_label,0, 1, 1, 1)
        self.reverb_simple_group.layout.addWidget(self.reverb_simple_zp_spinbox,0, 2, 1, 1)
        self.reverb_simple_group.layout.addWidget(self.reverb_simple_length_label,0, 3, 1, 1)
        self.reverb_simple_group.layout.addWidget(self.reverb_simple_length_spinbox,0, 4, 1, 1)
        self.reverbation_page.layout.addWidget(self.reverb_simple_group, 0, 0, -1 , 1)
        
        self.reverb_group = QGroupBox('Repeat-base reverbation:')
        self.reverb_group.layout = QGridLayout()
        self.reverb_group.setLayout(self.reverb_group.layout)
        
        self.reverb_repeatnum = QDial()
        self.reverb_repeatnum.setRange(1, 100)
        self.reverb_repeatnum_label = QLabel()
        self.reverb_repeatnum.valueChanged.connect(self.reverb_repeatnum_changed)
        self.reverb_repeatnum.setValue(2)
        
        self.reverb_repeatdalay = QDial()
        self.reverb_repeatdalay.setRange(1, 1000)
        self.reverb_repeatdalay_label = QLabel()
        self.reverb_repeatdalay.valueChanged.connect(self.reverb_repeatdalay_changed)
        self.reverb_repeatdalay.setValue(100)
        
        self.reverb_atten = QDial()
        self.reverb_atten.setRange(0, 99)
        self.reverb_atten_label = QLabel()
        self.reverb_atten.valueChanged.connect(self.reverb_atten_changed)
        self.reverb_atten.setValue(99)
        
        
        self.reverb_check = QCheckBox('Enable')
        self.reverb_check.setEnabled(True)
        self.reverb_check.stateChanged.connect(self.do_reverbation)
        
        self.reverb_group.layout.addWidget(self.reverb_repeatnum_label, 0, 0, 1, 1)
        self.reverb_group.layout.addWidget(self.reverb_repeatnum, 1, 0, 1, 1)
        self.reverb_group.layout.addWidget(self.reverb_repeatdalay_label, 0, 1, 1, 1)
        self.reverb_group.layout.addWidget(self.reverb_repeatdalay, 1, 1, 1, 1)
        self.reverb_group.layout.addWidget(self.reverb_atten_label, 0, 2, 1, 1)
        self.reverb_group.layout.addWidget(self.reverb_atten, 1, 2, 1, 1)
        self.reverb_group.layout.addWidget(self.reverb_check, 2, 2, 1, -1)
        
    
        self.reverbation_page.layout.addWidget(self.reverb_group, 0, 1, -1, 1)
        
        ## flanging:
        self.flanging_page = QWidget()
        self.flanging_page.layout = QGridLayout()
        self.flanging_page.setLayout(self.flanging_page.layout)
        self.processors_stack.addTab(self.flanging_page, 'Flanging')
        
        self.flanging_check = QCheckBox("Enable")
        self.flange_max_delay = QDial()
        self.flange_max_delay.setRange(1, 1000)
        self.flange_max_delay_label = QLabel()
        self.flange_max_delay.valueChanged.connect(self.flange_max_delay_changed)
        self.flange_max_delay.setValue(2)
        self.flanging_duration = QDial()
        self.flanging_duration.setRange(1, 10000)
        self.flanging_duration_label = QLabel()
        self.flanging_duration.valueChanged.connect(self.flanging_duration_change)
        self.flanging_duration.setValue(10000)
        self.flanging_gain = QDial()
        self.flanging_gain.setRange(1, 99)
        self.flanging_gain_label = QLabel()
        self.flanging_gain.valueChanged.connect(self.flanging_gain_changed)
        self.flanging_gain.setValue(90)
        self.fs_text = QLabel('Fs: ------ (Hz)')
        
        self.could_flanging_enabled = False
        
        self.flanging_page.layout.addWidget(self.flange_max_delay_label, 0, 0, 1, 1)
        self.flanging_page.layout.addWidget(self.flange_max_delay, 1, 0, 1, 1)
        self.flanging_page.layout.addWidget(self.flanging_duration_label, 0, 1, 1, 1)
        self.flanging_page.layout.addWidget(self.flanging_duration, 1, 1, 1, 1)
        self.flanging_page.layout.addWidget(self.flanging_gain_label, 0, 2, 1, 1)
        self.flanging_page.layout.addWidget(self.flanging_gain, 1, 2, 1, 1)

        
        self.flanging_check.setEnabled(self.could_flanging_enabled)
        self.flanging_check.stateChanged.connect(self.do_flanging_effect)
        self.flanging_page.layout.addWidget(self.flanging_check, 2, 2, 1, -1)
        self.flanging_page.layout.addWidget(self.fs_text, 2, 0, 1, 1)
        
        
        ## phasing:
        ###TODO
        self.phasing_check = QCheckBox('Enable')
        self.phasing_check.stateChanged.connect(self.do_phasing_effect)
        
        self.phasing_page = QWidget()
        self.phasing_page.layout = QGridLayout()
        self.phasing_page.setLayout(self.phasing_page.layout)
        self.processors_stack.addTab(self.phasing_page, 'Phasing Effect')
        
        self.phasing_zp_1 = QDoubleSpinBox()
        self.phasing_zp_1.setDecimals(3)
        self.phasing_zp_1.setRange(0, 0.999)
        self.phasing_zp_1.valueChanged.connect(self.phasing_changed)
        self.phasing_zp_1.setValue(0.5)
        self.phasing_zp_1.setSingleStep(0.001)
        self.phasing_od_1 = QSpinBox()
        self.phasing_od_1.valueChanged.connect(self.phasing_changed)
        self.phasing_od_1.setRange(0, 500)
        self.phasing_od_1.setValue(50)
        
        
        self.phasing_zp_2 = QDoubleSpinBox()
        self.phasing_zp_2.setDecimals(3)
        self.phasing_zp_2.setRange(0, 0.999)
        self.phasing_zp_2.valueChanged.connect(self.phasing_changed)
        self.phasing_zp_2.setValue(0.5)
        self.phasing_zp_2.setSingleStep(0.001)
        self.phasing_od_2 = QSpinBox()
        self.phasing_od_2.valueChanged.connect(self.phasing_changed)
        self.phasing_od_2.setRange(0, 500)
        self.phasing_od_2.setValue(50)
        
        
        self.phasing_zp_3 = QDoubleSpinBox()
        self.phasing_zp_3.setDecimals(3)
        self.phasing_zp_3.setRange(0, 0.999)
        self.phasing_zp_3.valueChanged.connect(self.phasing_changed)
        self.phasing_zp_3.setValue(0.5)
        self.phasing_zp_3.setSingleStep(0.001)
        self.phasing_od_3 = QSpinBox()
        self.phasing_od_3.valueChanged.connect(self.phasing_changed)
        self.phasing_od_3.setRange(0, 500)
        self.phasing_od_3.setValue(50)
        
        
        self.phasing_zp_4 = QDoubleSpinBox()
        self.phasing_zp_4.setDecimals(3)
        self.phasing_zp_4.setRange(0, 0.999)
        self.phasing_zp_4.valueChanged.connect(self.phasing_changed)
        self.phasing_zp_4.setValue(0.5)
        self.phasing_zp_4.setSingleStep(0.001)
        self.phasing_od_4 = QSpinBox()
        self.phasing_od_4.valueChanged.connect(self.phasing_changed)
        self.phasing_od_4.setRange(0, 500)
        self.phasing_od_4.setValue(50)
        
        
        self.phasing_zp_5 = QDoubleSpinBox()
        self.phasing_zp_5.setDecimals(3)
        self.phasing_zp_5.setRange(0, 0.999)
        self.phasing_zp_5.valueChanged.connect(self.phasing_changed)
        self.phasing_zp_5.setValue(0.5)
        self.phasing_zp_5.setSingleStep(0.001)
        self.phasing_od_5 = QSpinBox()
        self.phasing_od_5.valueChanged.connect(self.phasing_changed)
        self.phasing_od_5.setRange(0, 500)
        self.phasing_od_5.setValue(50)
        
        
        self.phasing_zp_6 = QDoubleSpinBox()
        self.phasing_zp_6.setDecimals(3)
        self.phasing_zp_6.setRange(0, 0.999)
        self.phasing_zp_6.valueChanged.connect(self.phasing_changed)
        self.phasing_zp_6.setValue(0.5)
        self.phasing_zp_6.setSingleStep(0.001)
        self.phasing_od_6 = QSpinBox()
        self.phasing_od_6.valueChanged.connect(self.phasing_changed)
        self.phasing_od_6.setRange(0, 500)
        self.phasing_od_6.setValue(50)
        
        
        self.phasing_zp_7 = QDoubleSpinBox()
        self.phasing_zp_7.setDecimals(3)
        self.phasing_zp_7.setRange(0, 0.999)
        self.phasing_zp_7.valueChanged.connect(self.phasing_changed)
        self.phasing_zp_7.setValue(0.5)
        self.phasing_zp_7.setSingleStep(0.001)
        self.phasing_od_7 = QSpinBox()
        self.phasing_od_7.valueChanged.connect(self.phasing_changed)
        self.phasing_od_7.setRange(0, 500)
        self.phasing_od_7.setValue(50)

        
        self.phasing_zp_8 = QDoubleSpinBox()
        self.phasing_zp_8.setDecimals(3)
        self.phasing_zp_8.setRange(0, 0.999)
        self.phasing_zp_8.valueChanged.connect(self.phasing_changed)
        self.phasing_zp_8.setValue(0.5)
        self.phasing_zp_8.setSingleStep(0.001)
        self.phasing_od_8 = QSpinBox()
        self.phasing_od_8.valueChanged.connect(self.phasing_changed)
        self.phasing_od_8.setRange(0, 500)
        self.phasing_od_8.setValue(50)
        
        
        self.phasing_zp_9 = QDoubleSpinBox()
        self.phasing_zp_9.setDecimals(3)
        self.phasing_zp_9.setRange(0, 0.999)
        self.phasing_zp_9.valueChanged.connect(self.phasing_changed)
        self.phasing_zp_9.setValue(0.5)
        self.phasing_zp_9.setSingleStep(0.001)
        self.phasing_od_9 = QSpinBox()
        self.phasing_od_9.valueChanged.connect(self.phasing_changed)
        self.phasing_od_9.setRange(0, 500)
        self.phasing_od_9.setValue(50)
        
        
        self.phasing_zp_0 = QDoubleSpinBox()
        self.phasing_zp_0.setDecimals(3)
        self.phasing_zp_0.setRange(0, 0.999)
        self.phasing_zp_0.valueChanged.connect(self.phasing_changed)
        self.phasing_zp_0.setValue(0.5)
        self.phasing_zp_0.setSingleStep(0.001)
        self.phasing_od_0 = QSpinBox()
        self.phasing_od_0.valueChanged.connect(self.phasing_changed)
        self.phasing_od_0.setRange(0, 500)
        self.phasing_od_0.setValue(50)
        
        
        self.phasing_zp_label = QLabel('Zero/Pole:')
        self.phasing_od_label = QLabel('Order:')
        
        self.phasing_gain = QDial()
        self.phasing_gain.setRange(0,  100)
        self.phasing_gain_label = QLabel()
        self.phasing_gain.valueChanged.connect(self.phasing_gain_changed)
        self.phasing_gain.setValue(88)
        
        self.phasing_page.layout.addWidget(self.phasing_zp_label, 0, 0, 1, 1)
        self.phasing_page.layout.addWidget(self.phasing_od_label, 1, 0, 1, 1)
        
        self.phasing_page.layout.addWidget(self.phasing_zp_1, 0, 1, 1, 1)
        self.phasing_page.layout.addWidget(self.phasing_od_1, 1, 1, 1, 1)
        self.phasing_page.layout.addWidget(self.phasing_zp_2, 0, 2, 1, 1)
        self.phasing_page.layout.addWidget(self.phasing_od_2, 1, 2, 1, 1)
        self.phasing_page.layout.addWidget(self.phasing_zp_3, 0, 3, 1, 1)
        self.phasing_page.layout.addWidget(self.phasing_od_3, 1, 3, 1, 1)
        self.phasing_page.layout.addWidget(self.phasing_zp_4, 0, 4, 1, 1)
        self.phasing_page.layout.addWidget(self.phasing_od_4, 1, 4, 1, 1)
        self.phasing_page.layout.addWidget(self.phasing_zp_5, 0, 5, 1, 1)
        self.phasing_page.layout.addWidget(self.phasing_od_5, 1, 5, 1, 1)
        self.phasing_page.layout.addWidget(self.phasing_zp_6, 0, 6, 1, 1)
        self.phasing_page.layout.addWidget(self.phasing_od_6, 1, 6, 1, 1)
        self.phasing_page.layout.addWidget(self.phasing_zp_7, 0, 7, 1, 1)
        self.phasing_page.layout.addWidget(self.phasing_od_7, 1, 7, 1, 1)
        self.phasing_page.layout.addWidget(self.phasing_zp_8, 0, 8, 1, 1)
        self.phasing_page.layout.addWidget(self.phasing_od_8, 1, 8, 1, 1)
        self.phasing_page.layout.addWidget(self.phasing_zp_9, 0, 9, 1, 1)
        self.phasing_page.layout.addWidget(self.phasing_od_9, 1, 9, 1, 1)
        self.phasing_page.layout.addWidget(self.phasing_zp_0, 0, 10, 1, 1)
        self.phasing_page.layout.addWidget(self.phasing_od_0, 1, 10, 1, 1)
        
        self.phasing_page.layout.addWidget(self.phasing_gain, 0, 11, 2, 2)
        self.phasing_page.layout.addWidget(self.phasing_gain_label, 0, 13, 1,1)
        
        self.phasing_page.layout.addWidget(self.phasing_check, 2, 13, 1, 1)
        self.phasing_freq = np.arange(0, 5001)/10000.0
        
        ## Equalizer:
        ###TODO
        self.EQ_page = QWidget()
        self.EQ_page.layout = QGridLayout()
        self.EQ_page.setLayout(self.EQ_page.layout)
        self.processors_stack.addTab(self.EQ_page, 'Filter')
        
        
        ### 
        self.LCD = QLCDNumber()
        self.LCD.setSegmentStyle(2)
        self.LCD.setDigitCount(11)
        self.LCD.display('  :  :  .  ')

        #self.layout.addWidget(self.Listplaylist, 0, 0, -1, 1)
        #self.layout.addWidget(self.AudioFrame, 0, 1, 1, 2)
        #self.layout.addWidget(self.LCD, 0, 1, 1, 2)
        #self.layout.addWidget(self.audio_progress, 1, 1, 1, 2)
        #self.layout.addWidget(self.go_next_page_B, 2, 2, 1, 1)
        #self.layout.addWidget(self.go_prev_page_B, 2, 1, 1, 1)
        #self.layout.addWidget(self.ControlFrame, 3, 1, 1, 2)
        #self.layout.addWidget(self.processor_frame, 0, 3, -1, -1)
        
        self.mainFrame = QWidget()   ###TODO
        self.mainFrame.setMaximumWidth(162)  #TODO
        self.mainFrame.setMaximumHeight(480)  #TODO
        self.mainFrame.layout = QGridLayout()
        self.mainFrame.setLayout(self.mainFrame.layout)
        
        self.mainFrame.layout.addWidget(self.AudioFrame,0,0,1,-1)
        self.mainFrame.layout.addWidget(self.LCD,0,0,1,-1)
        self.mainFrame.layout.addWidget(self.audio_progress,1,0,1,-1)
        self.mainFrame.layout.addWidget(self.go_prev_page_B,2,0,1,1)
        self.mainFrame.layout.addWidget(self.go_next_page_B,2,1,1,1)
        self.mainFrame.layout.addWidget(self.ControlFrame,3,0,1,-1)
        
        
        self.layout.addWidget(self.Listplaylist, 0)
        self.layout.addWidget(self.mainFrame,1)
        self.layout.addWidget(self.processor_frame, 2)


        
        self.prefixdir = ''
        if audio is not None:
            self.load_file(audio)
            self.Play.setEnabled(True)
            #self.index = 0
            #self.pause = True
        else:
            self.pause = False
            self.Play.setEnabled(False)
            self.index = 0
            self.audio_length = -1
        
            
        self.search_currentdir(audio)
        
        self.spectrum = np.ones((50))
        self.playlistindex = 0

        
        
        self.resize(QSize(184, 280))
        self.setMaximumHeight(500)
        #self.show()
        #self.raise_()
        self.xticks = np.array([50*np.log10(i) for i in range(1, 51)])
        self.xticks = self.xticks / self.xticks.max() * 50
    
        
        
    def paintEvent(self, events):
        self.__draw__()
        
        
    
    def __draw__(self):
        size = self.AudioFrame.size()
        self.AudioFrame.setScene(self.scene)
        w = size.width()
        h = size.height()

        x_index, y_index = self.calc_spectrum_size(w, h)        
        a = self.spectrum
        
        
        
        Pen = QPen(QColor(177, 0, 0))
        self.scene.clear()
        self.scene.setSceneRect(QRectF(0, 0, w*0.95, h*0.95))

        
        polypoints = QPolygonF([QPointF(0, h)]+[QPointF(self.xticks[i]*x_index+x_index, int(h - a[i]*100*y_index)) for i in range(50)]+[QPointF(2*x_index+self.xticks[-1]*x_index,h)])
        

        grad = QLinearGradient(QPointF(0, h), QPointF(0, 0))
        grad.setColorAt(0, QColor(255, 255, 0))
        grad.setColorAt(0.2, QColor(255, 170, 0))
        grad.setColorAt(1, QColor(170, 0, 0))
        Brush = QBrush(grad)

        self.scene.addPolygon(polypoints, Pen, Brush)
        self.play_partial()
        
        
        
    def calc_spectrum_size(self, w, h):
        x_index = w / 52.0
        y_index = h / 102.0
        return x_index, y_index
        
        
        
        
    def load_file(self, name):
        try:
            self.fs, self.audio = wavfile.read(self.prefixdir + name)
            p = pyaudio.PyAudio()
            self.stream = p.open(format=pyaudio.paInt16, channels=2, rate=self.fs, frames_per_buffer=100, output=True)

            #self.timer.start(0.01/fs)
            self.index = 0
            
            self.audio_length = self.audio[:,0].shape[0]
            self.audio_progress.setMaximum(self.audio_length / 1000)
            
            self.audio = self.audio.astype(np.double)
            self.max_spec_value = self.audio.sum(1).max()
            self.max_spec_value = np.sum([self.max_spec_value*0.9**k for k in range(4)])

            self.pause = False
            self.Play.setEnabled(True)
            self.Play.setText(self.playSymbolChar)
            self.audio_progress.setValue(0)
            self.could_flanging_enabled = True
            self.fs_text.setText('Fs: %6d (Hz)'%self.fs)
            self.flanging_check.setEnabled(self.could_flanging_enabled)
            self.flanging_check.setChecked(False)
        except:
            self.pause = True
            self.could_flanging_enabled = False
            self.fs_text.setText('Fs: ------ (Hz)'%self.fs)
            self.flanging_check.setEnabled(self.could_flanging_enabled)
            self.flanging_check.setChecked(False)
            print('loading seen problem')
            self.next_audio()
        
        
    def play_partial(self):
        length = 1000
        if self.pause is False and self.index < self.audio_length*1.0/length:
            self.time_calculation()
            i = self.index
            play = self.audio[length*i:length*(i+1),:]
            play = play * self.vl / 100.0
            shape0 = play.shape[0]
            if shape0 < length:
                play = np.vstack((play, np.zeros((length-shape0,play.shape[1]))))
                print('finished')
                self.next_audio()
            
            play = self.DSPProcessor(play, length)
            #print(play.max())
            
            self.audio_progress.setValue(self.index)
            frame = play.sum(1)/2
            #self.spectrum = 0.1 * np.abs(np.fft.rfft(frame[0:-1:10]))[0:50]/self.max_spec_value * 100 / (1+self.Volume_Dial.value()) + self.spectrum * (0.9)
            self.spectrum = 0.1 * self.periodgram(frame)/(self.max_spec_value) * 100 / (1+self.Volume_Dial.value()) + self.spectrum * (0.9)
            self.spectrum[self.spectrum > 1] = 1
            self.index += 1
            
            
            self.stream.write(play.astype(np.int16).tostring())
        else:
            self.spectrum = self.spectrum * (0.999)
            self.Play.setText(self.pauseSymbolChar)
        
    
    def animate(self):
        self.__draw__()
        self.update()
        
        
    def jump_audio(self):
        self.index = self.audio_progress.value()
        
        
    def volumeChange(self):
        self.vl = self.Volume_Dial.value() + 1
        
        
    def toggleplaypause(self):
        self.pause = not self.pause
        if self.pause is False:
            self.Play.setText('►')
        else:
            self.Play.setText('║')
        
        
    def toggleplaylistview(self):
        self.isshowplaylist = not self.isshowplaylist
        self.Listplaylist.setVisible(self.isshowplaylist)
        
        #if self.isshowplaylist is False:
            #self.layout = QGridLayout()
            #self.setLayout(self.layout)
            ##self.layout.removeWidget(self.Listplaylist)
            ##self.layout.addWidget(self.Listplaylist, 0, 0, -1, 1)
            #self.layout.addWidget(self.mainFrame,0,0,-1,1)
            #self.layout.addWidget(self.processor_frame, 0, 1, -1, -1)
        
    def search_currentdir(self, name=None):
        supported_format = ['wav']
        self.Listplaylist.clear()
        self.itemIndex = -1
        print(name)
        if name is None:
            files = listdir('./')
            self.prefixdir = ''
        else:
            self.prefixdir = '/'.join(name.split('/')[0:-1]) + '/'
            name = name.split('/')[-1]
            files = listdir(self.prefixdir)
        playlist = []
        j = 0
        itemIndex = 0
        for f in files:
            for ff in supported_format:
                if f[-3::] == ff:
                    playlist.append(f)
                    if f == name:
                        itemIndex = j
                    j += 1
                        
                    
                    
        for l in playlist : self.Listplaylist.addItem(QListWidgetItem(l))
        self.Listplaylist.setCurrentRow(itemIndex)
        self.playlistindex = itemIndex
        if name is not None:
            self.load_file(name)

        
    def getNewFromPlayList(self, item):
        #if pitem is not None:
        self.load_file(item.text())
        self.index = 0
        self.playlistindex = self.Listplaylist.currentRow()
    
    
    def next_audio(self):
        i = (self.playlistindex + 1) % self.Listplaylist.count()
        self.Listplaylist.setCurrentRow(i)
        self.playlistindex = i
        self.getNewFromPlayList(self.Listplaylist.item(self.playlistindex))

    
    def previous_audio(self):
        i = (self.playlistindex - 1) % self.Listplaylist.count()
        self.playlistindex = i
        self.Listplaylist.setCurrentRow(i)
        self.getNewFromPlayList(self.Listplaylist.item(self.playlistindex))
            
            
    def go_next_page(self):
        i = self.ControlFrame.currentIndex()
        self.ControlFrame.setCurrentIndex((i+1)%self.ControlFrame.count())
    
    
    def go_prev_page(self):
        i = self.ControlFrame.currentIndex()
        self.ControlFrame.setCurrentIndex((i-1)%self.ControlFrame.count())
        
    def periodgram(self, f):
        L = 0
        #l = f.shape[0]
        #f = f*f.conj()
        for i in range(10):
            l = f[i*100:(i+1)*100]
            lenl = l.shape[0]
            if lenl < 100:
                l = np.hstack((l, np.zeros((100-lenl))))
            L = np.fft.rfft(l) + L
        #L = np.fft.rfft(f)
        return np.abs(L/5)[0:50]
        
        
    def Processors(self):
        self.isshowprocess = not self.isshowprocess
        self.processor_frame.setVisible(self.isshowprocess)
        w1 = self.Listplaylist.size().width()
        w2 = self.processor_frame.size().width()
        if self.isshowprocess is False:
            if self.isshowplaylist is False:
                self.resize(QSize(184,280))
            else:
                self.resize(QSize(184+w1, 280))
        else:
            if self.isshowplaylist is False:
                self.resize(QSize(184+w2,280))
            else:
                self.resize(QSize(184+w1+w2, 280))
        
        
    
    
    def Opennewfile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Wav Files (*.wav)", options=options)
        if fileName:
            self.search_currentdir(name=fileName)            
            
    
    def time_calculation(self):
        overal_time = self.audio_length 
        passed = self.index * 1000.0
        remained = (overal_time - passed)/self.fs
        h = remained / 3600.0
        hour = int(h)
        m = (h - hour)*60.0
        minute = int(m)
        second = (m - minute)*60.0
        hour = '0'+str(hour) if hour < 10 else str(hour)
        minute = '0'+str(minute) if minute < 10 else str(minute)
        second = "0%1.2f"%(second) if second < 10 else "%1.2f"%(second)
        self.text = hour+":"+minute+":"+second#"%2d:%2d:%2.2f"%(hour,minute,second)
        #text = str(hour)+':'+str(minute)+':'+'00.00'
        self.LCD.display(self.text)
        
        
        
        
    def phaseshift_slider_change(self):
        v = self.phaseshift_slider.value()
        self.phaseshift_label.setText('Scale: '+str(v/200))
        #self.phaseshift_slider_2.setValue(v)
        if v == 0:
            self.phaseshift_check.setChecked(False)
            self.timestretch_check.setChecked(False)
            self.phaseshift_check.setEnabled(False)
            self.timestretch_check.setEnabled(False)
        else:
            self.phaseshift_check.setEnabled(True)
            self.timestretch_check.setEnabled(True)

    
    def do_phaseshifting(self, state):
        pass
    
    
    def do_simple_reverbation(self, state):
        if state:
            self.reverb_check.setChecked(not state)
            self.flanging_check.setChecked(not state)
            self.reverbator, self.reverb_simple_zp, self.reverb_simple_length = coreprocessor.Reverb(reverb_zp=self.reverb_simple_zp, reverb_length=self.reverb_simple_length)
    
    
    def do_reverbation(self, state):
        if state:
            self.reverb_simple_check.setChecked(not state)
            #self.flanging_check.setChecked(not state)
            
            
    def get_zp_simple_reverb(self, zp):
        self.reverb_simple_zp = zp
        self.reverb_simple_check.setChecked(False)
    
    def get_len_simple_reverb(self, ln):
        self.reverb_simple_length = ln
        self.reverb_simple_check.setChecked(False)
        
        
    def reverb_repeatnum_changed(self, value):
        self.reverb_repeatnum_label.setText("Repeat number: %2d"%value)
        
        
    def reverb_repeatdalay_changed(self, value):
        self.reverb_repeatdalay_label.setText("delays: %1.3f (sec)"%(value/500.0))
    
    
    def reverb_atten_changed(self, value):
        self.reverb_atten_label.setText("attenuation per delay: %1.2f"%(value/100.0))
        
        
    def flange_max_delay_changed(self, value):
        self.flange_max_delay_label.setText('Max delay: %2.4f (sec)'%(value*12.0*1e-6))
        self.flanging_check.setChecked(False)
        
        
    def flanging_duration_change(self, value):
        self.flanging_duration_label.setText('Time duration: %2.3f (sec)'%(value/500.0))
        self.flanging_check.setChecked(False)
        
        
    def flanging_gain_changed(self, value):
        self.flanging_gain_label.setText('Gain: %1.2f'%(value/100.0))
        self.flanging_check.setChecked(False)
        
        
    def do_flanging_effect(self, state):
        if state:
            #self.reverb_check.setChecked(not state)
            self.reverb_simple_check.setChecked(not state)
            # init flangin parameter
            self.flange_delay, self.flanging_rem = coreprocessor.Flanging_params(fs=self.fs,flanging_time=self.flanging_duration.value()/500.0, flange_max_delay=self.flange_max_delay.value()*12.0*1e-6, flanging_gain=self.flanging_gain.value()/100.0)
            
            
    ##TODO
    def phasing_changed(self, value):
        self.phasing_check.setChecked(False)
        
    
    def phasing_gain_changed(self, value):
        self.phasing_gain_label.setText('gain:%1.2f'%(self.phasing_gain.value()/100.0))
        self.phasing_check.setChecked(False)

    
    def do_phasing_effect(self, state):
        if state:
            zp1 = self.phasing_zp_1.value()
            od1 = self.phasing_od_1.value()
            zp2 = self.phasing_zp_2.value()
            od2 = self.phasing_od_2.value()
            zp3 = self.phasing_zp_3.value()
            od3 = self.phasing_od_3.value()
            zp4 = self.phasing_zp_4.value()
            od4 = self.phasing_od_4.value()
            zp5 = self.phasing_zp_5.value()
            od5 = self.phasing_od_5.value()
            zp6 = self.phasing_zp_6.value()
            od6 = self.phasing_od_6.value()
            zp7 = self.phasing_zp_7.value()
            od7 = self.phasing_od_7.value()
            zp8 = self.phasing_zp_8.value()
            od8 = self.phasing_od_8.value()
            zp9 = self.phasing_zp_9.value()
            od9 = self.phasing_od_9.value()
            zp0 = self.phasing_zp_0.value()
            od0 = self.phasing_od_0.value()
            
            Z = [zp1, zp2, zp3, zp4, zp5, zp6, zp7, zp8, zp9, zp0]
            O = [od1, od2, od3, od4, od5, od6, od7, od8, od9, od1] 
            
            ##TODO
            self.phaser_TF = 1
            for i in range(10):
                z = Z[i]
                #for o in range(O[i]):
                self.phaser_TF = (self.phaser_TF * ((z + 1 * np.exp(-1j*2*np.pi*self.phasing_freq*1))/((1 + z * np.exp(-1j*2*np.pi*self.phasing_freq*1)))))**O[i]##TODO
            
            self.phaser_TF = np.vstack((self.phaser_TF, self.phaser_TF)).T #*self.phasing_gain.value()/100.0
    
    
    def DSPProcessor(self, frame, length=1000):
        
        anyone = False
        try:
            frame1 = 0
            frame2 = 0
            frame3 = 0
            if self.flanging_check.isChecked() and self.index>5:
                index = np.arange(1000*self.index, 1000 * (self.index+1)).astype(np.int)
                frame_delayed = self.audio[index - self.flange_delay[1000*(self.index%self.flanging_rem):1000*(self.index%self.flanging_rem+1)]]
                frame1 = coreprocessor.flanging_effect(frame, self.flanging_gain.value()/100.0, frame_delayed)
                anyone = True
                frame = frame1
            
            if self.reverb_simple_check.isChecked() and self.index > 5:
                frame = coreprocessor.SimpleReverb(self.audio[(self.index-4)*1000:(self.index+1)*1000], self.reverbator, leng=1000)
                anyone = True
                #print('reverb simple:', self.reverbator.shape)
                
            if self.reverb_check.isChecked():
                #frame = coreprocessor.reverb_repeat(self.audio, self.index, self.fs, 0.1, repeats= 10, attenuation=0.8, leng=1000)
                frame2 = coreprocessor.reverb_repeat(self.audio, self.index, self.fs, self.reverb_repeatdalay.value()/500.0, self.reverb_repeatnum.value(), attenuation=self.reverb_atten.value()/100.0)
                anyone = True
                frame = frame1 + frame2
                
            if self.phasing_check.isChecked() and self.index > 10:
                w = self.audio[(self.index-9)*1000:(self.index+1)*1000,:].copy()
                frame3 = coreprocessor.phasing_effect(w, self.phaser_TF)
                frame = frame1 + frame2 + frame3
                anyone = True
            
            if self.phaseshift_check.isChecked():
                frame = coreprocessor.Phaseshifting_Timestretching2(frame, self.phaseshift_slider.value(), self.timestretch_check.isChecked(), length)
                anyone = True
                
            if self.voiceremove_B.isChecked():
                frame = coreprocessor.remove_centered_voice(frame)
                
            if anyone:
                frame = coreprocessor.backtoint16(frame)
        except:
            print('something bad happend')
        return frame
