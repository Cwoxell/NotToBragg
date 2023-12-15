from FBG_start import Ui_MainWindow as Ui_start

from FBG_fiber import Ui_Form as Ui_fiber
from FBG_who import Ui_Form as Ui_who
from FBG_basic_start import Ui_Form as Ui_basic
from FBG_advanced_start import Ui_Form as Ui_advanced
from FBG_imaging import Ui_Form as Ui_imaging
from FBG_etching import Ui_Form as Ui_etching
from FBG_end import Ui_Form as Ui_end

from PyQt5.QtSerialPort import QSerialPort
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QIODevice
import serial.tools.list_ports
from pylablib.devices import Thorlabs