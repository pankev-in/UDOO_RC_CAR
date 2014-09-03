#!/usr/bin/python

#	UDOO Server Socket
#This programm listens to the port number: 45643
#Output FORM:
#    
#    String = "SPEED+DIRECTION."
#    
#    SPEED => Is the value for the speed, From -10 to 10;
#    DIRECTION => Is the value for servo direction, From -10 to 10;
#    
#    
#Created 20 May 2014
#by Kevin Pan

import serial
import socket
import sys

HOST=''
PORT=8888
TF=False
InputString=''
Buffer=16


#Serial connection to Arduino
arduino = serial.Serial("/dev/tty.usbmodemfd121",9600)
print ("\nSerial Connection Created\n")

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
sock.bind((HOST,PORT))
print("\nUDP Server Connection Created\n")

while True:
   data, addr = sock.recvfrom(Buffer) # buffer size is 16 bytes
   print data
   if data=="end":
	print "Disconnected from Client:",addr
   arduino.write(data);


arduino.close()
sock.close()
del sock
print('Programm ended.\n\n')

