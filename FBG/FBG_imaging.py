# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FBG_imaging.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.



'''
given parameters from advanced or basic start 
    inscrition length/height TRY ME WILL BE HARD 

'''

from PyQt5.QtSerialPort import QSerialPort
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QIODevice
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
import time
from pylablib.devices import Thorlabs


import serial.tools.list_ports
from pylablib.devices import Thorlabs
import sys
import os
os.environ['OPENCV_VIDEOIO_PRIORITY'] = '0'
import cv2

stageX = Thorlabs.KinesisMotor("27601391")
stageY = Thorlabs.KinesisMotor("27264708")

stageX.home(force=True, sync=False)
stageY.home(force=True, sync=False)
stageX.wait_for_home()
stageY.wait_for_home()


#from spec sheet
pos_scaling = 34550
vel_scaling = 767367.49
accel_scaling = 261.93

#from device
device_scaleX = stageX.get_scale()
device_scaleY = stageY.get_scale()

#scaling uses spec sheet and device
pos_scalingX = pos_scaling / device_scaleX[0]
vel_scalingX = vel_scaling / device_scaleX[1]
accel_scalingX = accel_scaling / device_scaleX[2]

pos_scalingY = pos_scaling / device_scaleY[0]
vel_scalingY = vel_scaling / device_scaleY[1]
accel_scalingY = accel_scaling / device_scaleY[2]

stageX.setup_velocity(min_velocity=0,acceleration=(1*accel_scalingX),max_velocity=(1*vel_scalingX)) #1mm/s velocity and 1mm/s^2 accel
stageY.setup_velocity(min_velocity=0,acceleration=(1*accel_scalingY),max_velocity=(1*vel_scalingY))

#go to initial position
stageY.move_by(11.8*pos_scalingX) #11.8mm
stageY.wait_move()

class Ui_Form(object):
    def __init__(self, n, minH, maxH, bs, period, height, power, order):
        self.n = n
        self.minH = minH
        self.maxH = maxH
        self.bs =bs 
        self.period=period
        self.height = height
        self.power = power
        self.order = order
        print(self.n)
        print(self.minH)
        print(self.maxH)
        print(self.bs)
        print(self.period)
        print(self.height)
        print(self.power)
        print(self.order)

    def upButton(self):
        print("up")
        #stageY.move_by(0.025*pos_scalingY)  #25 um
        stageY.move_by(.015*pos_scalingY) #larger for testing


    def downButton(self):
        print("down")
        #stageY.move_by(-0.025*pos_scalingY) #25 um
        stageY.move_by(-.015*pos_scalingY) #larger for testing
        return

    def leftButton(self):
        print("left")
        stageX.move_by(-1*pos_scalingX) #1 mm
        return

    def rightButton(self):
        print("right")
        stageX.move_by(1*pos_scalingX) #1 mm
        return

    def clicked(self, FBG_imaging_info, MainWindow_info, FBG_etching_info, FBG_end_info):
        #stageX.close()
        #stageY.close()
        self.window = QtWidgets.QWidget() #type
        self.ui = FBG_etching_info(self.n, self.minH, self.maxH, self.bs, self.period, self.height, self.power, self.order, stageX, stageY) #class name
        self.ui.setupUi(self.window, MainWindow_info, FBG_end_info)
        self.window.show() # opens this new window 
        FBG_imaging_info.hide() # hides this window

    def setupUi(self, Form, MainWindow, FBG_etching, FBG_end):
        Form.setObjectName("Form")
        Form.resize(1078, 873)
        Form.setStyleSheet("QWidget{\n"
"\n"
"background-color:rgb(23, 17, 57)\n"
"}")
        self.pushButton = QtWidgets.QPushButton(Form, clicked = lambda: self.clicked(Form, MainWindow, FBG_etching, FBG_end))
        self.pushButton.setGeometry(QtCore.QRect(820, 450, 201, 71))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton {\n"
"    background-color: #3498db; /* Blue background color */\n"
"    color: #ffffff; /* White text color */\n"
"    border-radius: 15px; /* Rounded corners */\n"
"    padding: 10px; /* Padding around the content */\n"
"    width: 100px; /* Set a specific width */\n"
"    height: 40px; /* Set a specific height */\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(40, 10, 1021, 71))
        font = QtGui.QFont()
        font.setFamily("STCaiyun")
        font.setPointSize(28)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("QLabel{\n"
"color:rgb(255, 0, 127)\n"
"}")
        self.label_2.setObjectName("label_2")




        self.graphicsView = VideoWidget(Form)  # Use the custom VideoWidget
        self.graphicsView.setGeometry(QtCore.QRect(40, 180, 751, 461))



        self.up_button = QtWidgets.QPushButton(Form, clicked = lambda: self.downButton())
        self.up_button.setGeometry(QtCore.QRect(880, 270, 91, 51))
        self.up_button.setStyleSheet("QPushButton {\n"
"    background-color: #3498db; /* Blue background color */\n"
"    color: #ffffff; /* White text color */\n"
"    border-radius: 15px; /* Rounded corners */\n"
"    padding: 10px; /* Padding around the content */\n"
"    width: 100px; /* Set a specific width */\n"
"    height: 40px; /* Set a specific height */\n"
"}")
        self.up_button.setObjectName("up_button")
        self.down_button = QtWidgets.QPushButton(Form, clicked = lambda: self.upButton())
        self.down_button.setGeometry(QtCore.QRect(880, 370, 91, 51))
        self.down_button.setStyleSheet("QPushButton {\n"
"    background-color: #3498db; /* Blue background color */\n"
"    color: #ffffff; /* White text color */\n"
"    border-radius: 15px; /* Rounded corners */\n"
"    padding: 10px; /* Padding around the content */\n"
"    width: 100px; /* Set a specific width */\n"
"    height: 40px; /* Set a specific height */\n"
"}")
        self.down_button.setObjectName("down_button")
        self.left_button = QtWidgets.QPushButton(Form, clicked = lambda: self.leftButton())
        self.left_button.setGeometry(QtCore.QRect(960, 320, 91, 51))
        self.left_button.setStyleSheet("QPushButton {\n"
"    background-color: #3498db; /* Blue background color */\n"
"    color: #ffffff; /* White text color */\n"
"    border-radius: 15px; /* Rounded corners */\n"
"    padding: 10px; /* Padding around the content */\n"
"    width: 100px; /* Set a specific width */\n"
"    height: 40px; /* Set a specific height */\n"
"}")
        self.left_button.setObjectName("left_button")
        self.right_button = QtWidgets.QPushButton(Form, clicked = lambda: self.rightButton())
        self.right_button.setGeometry(QtCore.QRect(800, 320, 91, 51))
        self.right_button.setStyleSheet("QPushButton {\n"
"    background-color: #3498db; /* Blue background color */\n"
"    color: #ffffff; /* White text color */\n"
"    border-radius: 15px; /* Rounded corners */\n"
"    padding: 10px; /* Padding around the content */\n"
"    width: 100px; /* Set a specific width */\n"
"    height: 40px; /* Set a specific height */\n"
"}")
        self.right_button.setObjectName("right_button")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(0, 650, 1081, 291))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.textEdit.setFont(font)
        self.textEdit.setStyleSheet("QTextEdit{\n"
"color:white;\n"
"}")
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Aligned!"))
        self.label_2.setText(_translate("Form", "Use the camera to line up your fiber to the laser!"))
        self.up_button.setText(_translate("Form", "Up"))
        self.down_button.setText(_translate("Form", "Down"))
        self.left_button.setText(_translate("Form", "Right"))
        self.right_button.setText(_translate("Form", "Left"))
        self.textEdit.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Use the buttons below to align your laser!</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Step one: Z alignment</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">    Please use the nobs to manually adjust the height of the stages. Move the height until the beam is as small as possible as seen on the video.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Step two: X/Y alignment</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">    Please use the buttons above to set the center of the beam to the center of the fiber. Please give enough room for the full length of the grating.</span></p></body></html>"))





class VideoWidget(QWidget):
    def __init__(self, parent=None):
        super(VideoWidget, self).__init__(parent)
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 751, 461)

        self.capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Add vertical and horizontal lines with small millimeter lines
        center_x = frame.shape[1] // 2
        center_y = frame.shape[0] // 2
        line_length = min(frame.shape[1], frame.shape[0]) // 2
        mm_spacing = 10  # Adjust as needed

        # Vertical line
        cv2.line(frame, (center_x, 0), (center_x, frame.shape[0]), (255, 255, 255), 1)

        # Small millimeter horizontal lines
        for j in range(0, frame.shape[0], mm_spacing):
            cv2.line(frame, (center_x - 5, j), (center_x + 5, j), (255, 255, 255), 1)

        # Horizontal line
        cv2.line(frame, (0, center_y), (frame.shape[1], center_y), (255, 255, 255), 1)

        # Small millimeter vertical lines
        for i in range(0, frame.shape[1], mm_spacing):
            cv2.line(frame, (i, center_y - 5), (i, center_y + 5), (255, 255, 255), 1)



            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.label.setPixmap(pixmap)
    
        return

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())