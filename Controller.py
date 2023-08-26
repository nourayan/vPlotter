
import serial
import time


class Controller:
    
    def __init__(self):
        
        self.ser = serial.Serial('COM6')


        self.ser.baudrate = 9600
        self.ser.bytesize = 8
        self.ser.parity = 'N'
        self.ser.stopbits = 1


    time.sleep(3)                      

    def close(self):
        
        self.ser.close()

    def pen_up(self):
       
        self.ser.write('pu\n'.encode())
        self.ser.read(1)  # block until command complete byte is received

    def pen_down(self):
        
        self.ser.write('pd\n'.encode())
        self.ser.read(1)  # block until command complete byte is received

    def move(self, l, r):
        
        self.ser.write('m {} {}\n'.format(l, r).encode())
        self.ser.read(1)  # block until command complete byte is received

    def turn_off(self):
       
        self.ser.write('o\n'.encode())
        self.ser.read(1)  # block until command complete byte is received
