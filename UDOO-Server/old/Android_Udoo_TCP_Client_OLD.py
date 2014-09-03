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

HOST='192.168.11.7'
PORT=8888
TF=False
InputString=''
Buffer=64
MAX=16384


#Serial connection to Arduino
arduino = serial.Serial("/dev/ttymxc3",9600)
print ("\n\nSerial Connection Created")

#Socket Connection
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sock.connect((HOST,PORT))

print 'Socket Connected'

InputString=sock.recv(Buffer)

while InputString[0:1]=="<":
	InputString=''

while True:
    #Buffering Data income:
    InputString=sock.recv(Buffer)

    #End program by sending 'end' string:
    if InputString == "<STOP>":
	print("Disconnected form Client")
	sys.exit()

    INPUT=InputString.split(";");

    speedString=INPUT[1].lstrip("{S").rstrip('}')
    directionString=INPUT[2].lstrip("{S").rstrip('}')

    speed=int(-float(speedString)/MAX*10)
    direction=int(float(directionString)/MAX*10)

    print speed,"+",direction,"."


    arduino.write(speed,)
    InputString=''


arduino.close()
sock.close()
del sock
print('Programm ended.\n\n')

