
#Global import
import sys
import time
import serial
import struct
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLineEdit,
    QPlainTextEdit,
    QMainWindow,
    QLabel,
    QComboBox
    )
from PyQt5.QtGui import QFont
from threading import Thread
from threading import Event
from PyCRC.CRCCCITT import CRCCCITT
#Local import
from strFit import *
from UI_flag import *

   


class Window (QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.test_string = [
            "EEEEEEEEEEEEEEEEEEEE\nEEEEEEEEEEEEEEEEEEEE\nEEEEEEEEEEEEEEEEEEEE\nEEEEEEEEEEEEEEEEEEEE",
            "MMMMMMMMMMMMMMMMMMMM\nMMMMMMMMMMMMMMMMMMMM\nMMMMMMMMMMMMMMMMMMMM\nMMMMMMMMMMMMMMMMMMMM",
            "WWWWWWWWWWWWWWWWWWWW\nWWWWWWWWWWWWWWWWWWWW\nWWWWWWWWWWWWWWWWWWWW\nWWWWWWWWWWWWWWWWWWWW",
            ]
        
        self.setFixedSize (550,260) 
        self.move (300,300)
        self.setWindowTitle ('Remote Display Test v.1.1')

        input_font=QFont("Courier",10)
        
        self.input_box=QPlainTextEdit(self)
        self.input_box.move (370,10)
        self.input_box.resize (170, 190)
        self.input_box.setPlainText(self.test_string[0])
        self.input_box.setFont(input_font)
        self.textpage = 1

        help1_label=QLabel(self)
        help1_label.move (10,0)
        help1_label.resize (170,30)
        help1_label.setText("Instructions:")

        help2_label=QLabel(self)
        help2_label.move (10,20)
        help2_label.resize (350,30)
        help2_label.setText("1) Connect to the display via RS-485. Switch the power on.") 

        help3_label=QLabel(self)
        help3_label.move (10,40)
        help3_label.resize (350,30)
        help3_label.setText("2) Open Device Manager and determine the COM port.")

        help4_label=QLabel(self)
        help4_label.move (10,60)
        help4_label.resize (350,30)
        help4_label.setText('3) Select the appropriate COM port below. Click "Connect".')

        help5_label=QLabel(self)
        help5_label.move (10,80)
        help5_label.resize (350,30)
        help5_label.setText('4) The PC will start sending ping (empty messages) to the display.')
        
        help6_label=QLabel(self)
        help6_label.move (10,100)
        help6_label.resize (350,30)
        help6_label.setText('5) Click "Send". The message on the right should appear on the display.')

        help7_label=QLabel(self)
        help7_label.move (10,120)
        help7_label.resize (350,30)
        help7_label.setText('6) You can click "Auto fill and Send" to check pixel integrity.')

        pulse_label=QLabel(self)
        pulse_label.move (10,160)
        pulse_label.setText("Request interval, ms")

        self.pulse_box=QLineEdit(self)
        self.pulse_box.move (120,165)
        self.pulse_box.resize (60,20)
        self.pulse_box.setText("200")

        port_label=QLabel(self)
        port_label.move (10,180)
        port_label.setText("Port")

        self.port_box=QComboBox(self)
        self.port_box.addItems(["COM1","COM2","COM3","COM4","COM5","COM6","COM7","COM8"])
        self.port_box.move (120,185)
        self.port_box.resize (60,20)

        btn_stop = QPushButton('Reset',self)
        btn_stop.resize(170,25)
        btn_stop.move (190,210)
        btn_stop.clicked.connect(self.btn_stop_clicked)        

        btn_send = QPushButton('Send',self)
        btn_send.resize(170,25)
        btn_send.move (370,210)
        btn_send.clicked.connect(self.btn_send_clicked)
        
        btn_auto = QPushButton('Auto fill and Send',self)
        btn_auto.resize(170,25)
        btn_auto.move (370,175)
        btn_auto.clicked.connect(self.btn_auto_clicked)
        
        btn_conn = QPushButton('Connect',self)
        btn_conn.resize(170,25)
        btn_conn.move (10,210)
        btn_conn.clicked.connect(self.btn_conn_clicked)

        self.flag_tx = Flag(self)
        self.flag_tx.move(190,170)

        TX_label=QLabel(self)
        TX_label.move (205,165)
        TX_label.resize (40,20)
        TX_label.setText("TX")

        self.flag_rx = Flag(self)
        self.flag_rx.move(220,170)

        RX_label=QLabel(self)
        RX_label.move (235,165)
        RX_label.resize (40,20)
        RX_label.setText("RX")

        self.show()

    def btn_auto_clicked (self):
        self.input_box.setPlainText(self.test_string[self.textpage])
        self.textpage += 1
        if self.textpage == 3:
            self.textpage = 0
        self.btn_send_clicked()

    def btn_stop_clicked (self):
        allow_exchange.clear()
        ser.close()
        self.statusBar().showMessage ("Connection closed.")

    def btn_send_clicked (self):
        input_string = self.input_box.toPlainText()
        input_string = strFit_4x20(input_string)
        buffer_string = input_string.encode('1251','ignore')
        ser.write_buffer = p_init + p_src + p_dst + p_0_cmd + buffer_string
        crc = CRCCCITT().calculate(ser.write_buffer)
        ser.write_buffer += struct.pack('<H', crc)
        ser.write_buffer += p_end + p_stop
          

    def btn_conn_clicked (self):
        allow_exchange.clear()
        ser.close()
        ser.pulse=int(self.pulse_box.text())
        if (self.port_box.currentIndex()==0):
            ser.port="COM1"
        if (self.port_box.currentIndex()==1):
            ser.port="COM2"
        if (self.port_box.currentIndex()==2):
            ser.port="COM3"
        if (self.port_box.currentIndex()==3):
            ser.port="COM4"
        if (self.port_box.currentIndex()==4):
            ser.port="COM5"
        if (self.port_box.currentIndex()==5):
            ser.port="COM6"
        if (self.port_box.currentIndex()==6):
            ser.port="COM7"
        if (self.port_box.currentIndex()==7):
            ser.port="COM8"
        try:
            ser.open()
            self.statusBar().showMessage ("Connection opened.")
            allow_exchange.set()
        except Exception:
            self.statusBar().showMessage ("Port inaccessible.")
        

def RS_exchange():
    while(True):
        allow_exchange.wait()
        ser.write(ser.write_buffer)
        TX.set()
        read_buffer = b''
        try:
            for i in range(4):
                read_buffer = ser.read()
        except Exception:
            pass
        if read_buffer == p_good:
            ser.write_buffer = pulse_data 
            RX.set()
        elif read_buffer == p_bad:
            RX_bad.set()
        try:
            for i in range(4):
                read_buffer = ser.read()           
        except Exception:
            pass
        time.sleep(ser.pulse/1000)

def TX_blink():
    while(True):
        TX.wait()
        w.flag_tx.set1()
        w.flag_tx.update()
        time.sleep(0.1)
        w.flag_tx.set0()
        w.flag_tx.update()
        TX.clear()

def RX_blink():
    while(True):
        RX.wait()
        w.flag_rx.set1()
        w.flag_rx.update()
        time.sleep(0.1)
        w.flag_rx.set0()
        w.flag_rx.update()
        RX.clear()

def RX_bad_blink():
    while(True):
        RX_bad.wait()
        w.flag_rx.set2()
        w.flag_rx.update()
        time.sleep(0.1)
        w.flag_rx.set0()
        w.flag_rx.update()
        RX_bad.clear()

class Flag (QWidget): 

    col=QColor(255,255,255)
 
    def paintEvent(self, event):
        f=QPainter(self)
        f.setBrush(self.col)
        f.setPen(QPen(QColor(0,0,0),1))
        f.drawRect(0,0,10,10)

    def set1(self):
        self.col=QColor(0,255,0)

    def set0(self):
        self.col=QColor(255,255,255)

    def set2(self):
        self.col=QColor(255,0,0)

if __name__ == '__main__':
    ser = serial.Serial()
    allow_exchange = Event()
    TX = Event()
    RX = Event()
    RX_bad = Event()
    thread2 = Thread(target=RS_exchange)
    threadTX = Thread(target=TX_blink)
    threadRX = Thread(target=RX_blink)
    threadRX_bad = Thread(target=RX_bad_blink)
    
    ser.baudrate = 100000
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.pulse = 200

    p_init = b'\x1F'
    p_src = b'\x33'
    p_dst = b'\x44'
    p_pulse_cmd = b'\xFF'
    p_0_cmd = b'\x51'
    p_end = b'\x2F'
    p_stop = b'\x55'

    p_good = b'\x11'
    p_bad = b'\x22'

   
    ser.write_buffer = p_init + p_src + p_dst + p_pulse_cmd
    crc = CRCCCITT().calculate(ser.write_buffer)
    ser.write_buffer += struct.pack('<H', crc)
    ser.write_buffer += p_end + p_stop
    pulse_data=ser.write_buffer

    thread2.start()
    threadTX.start()
    threadRX.start()
    threadRX_bad.start()
    
    app = QApplication(sys.argv)
    w = Window()
    cleanup = app.exec() 
    allow_exchange.clear()
    ser.close() 
    sys.exit(cleanup)
