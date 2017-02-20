import time
import sys
import threading
import serial

performed_tilts = 0
detected_tilts = 0

ard = serial.Serial(
    port='/dev/tty.wchusbserial1410',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS,
    rtscts=False
)
raw_input()
ard.write('A')
raw_input();

ard.write("S")
while(1):
    a=1


