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
Buffer=20


#Serial connection to Arduino
arduino = serial.Serial("/dev/tty.usbmodemfd121",9600)
print ("\n\nSerial Connection Created")

#Socket Connection
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    sock.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

sock.listen(10)
print 'Socket now listening'

conn, addr = sock.accept()
print 'Connected with ' + addr[0] + ':' + str(addr[1])


while True:
    #Buffering Data income:
    InputString=conn.recv(Buffer)

    #End program by sending 'end' string:
    if InputString == "end":
	print("Disconnected form Client")
	sys.exit()

    #print recived comman on to the Screen:
    print(InputString)

    arduino.write(InputString)
    InputString=''


arduino.close()
sock.close()
del sock
print('Programm ended.\n\n')

