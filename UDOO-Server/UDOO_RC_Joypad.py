#!/usr/bin/python
#	UDOO Server Socket: working with Driodpad - Andriod
#Created 11 June 2014
#by Kevin Pan

import serial
import socket
import sys
from time import sleep

HOST=''
PORT=0

Gyro='';
X=0.000000;#Gyroscope X-axis
Y=0.000000;#Gyroscope Y-axis
Z=0.000000;#Gyroscope Z-axis
S1=0;#Slider 1;
S2=0;#Slider 2;
S3=0;#Slider 3;
S4=0;#Slider 4;
T1=0;#Trigger servo;
T2=0;#Trigger power;
B1=0;#Button - 'GO'
Speed=0;
Direction=0;


breakout=0;
BufferSize=128
SliderMax=16384
OutputString=''
InputString=''



#Programstart
print "\n	Programm Started"


#Checking system input values
if len(sys.argv)<2:
	print "\n####################################"
	print "ERROR: Need more input information!!! \n"+"Format:   python XYZ.py [HOST] [Port] "
	print "####################################"
	sys.exit("\n	Programm Ended.\n")

HOST=sys.argv[1]
PORT=int(sys.argv[2])


#Serial connection to Arduino
#arduino = serial.Serial("/dev/ttymxc3",9600)
print ("\nSerial Connection with Arduino Created")


#Socket Connection
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((HOST,PORT))
print '\nSocket Connected:'
print "Connected to Host Address:",HOST
print "Connected to Port Number:",PORT,"\n\n"


while True:
	#Buffering Data income:
	InputString=sock.recv(BufferSize)

	#End program by sending '<stop>' string:
	if InputString[1:5] == 'STOP':
		print("Disconnected form Client")
		sys.exit()


	#Editing Values:
	Values=InputString.split(";")
	Gyro=Values[0].split(",")
	try:
		X=float(Gyro[0].lstrip("[{"))
		Y=float(Gyro[1])
		Z=float(Gyro[2].rstrip("}"))
		S1=int(Values[1].lstrip("{S").rstrip("}"))
		S2=int(Values[2].lstrip("{S").rstrip("}"))
		S3=int(Values[3].lstrip("{S").rstrip("}"))
		S4=int(Values[4].lstrip("{S").rstrip("}"))
		T1=int(Values[5])
		T2=int(Values[6])
		B1=int(Values[7][0:1])
		breakout=0;
	except (ValueError,IndexError) as e:
		X=0;Y=0;Z=0;S1=0;S2=0;S3=0;S4=0;T1=0;T2=0;B1=0;
		breakout=breakout+1
		if breakout>=5:
			sys.exit("\nConnection breaks\n");
		pass


	#SPEED CALCULATION
	if B1==1:
		if T2==1:
			if Z>=0:
				if int(X)==9:Speed=0
				elif int(X)==8:Speed=4
				elif  int(X)==7:Speed=4
				elif  int(X)==6:Speed=5
				elif int(X)==5:Speed=5
				elif  int(X)==4:Speed=6
				elif  int(X)==3:Speed=6
				elif  int(X)<=2:Speed=7
			elif  Z<=0:
				if int(X)==9:Speed=0
				elif int(X)==8:Speed=-4
				elif  int(X)==7:Speed=-4
				elif  int(X)==6:Speed=-5
				elif int(X)==5:Speed=-5
				elif  int(X)==4:Speed=-6
				elif  int(X)==3:Speed=-6
				elif  int(X)<=2:Speed=-7
		elif  T2==0:
			if Z>=0:
				if int(X)==9:Speed=0
				elif  int(X)==8:Speed=3
				elif  int(X)==7:Speed=4
				elif  int(X)==6:Speed=5
				elif  int(X)<=5:Speed=5
			elif  Z<=0:
				if int(X)==9:Speed=0
				elif  int(X)==8:Speed=-3
				elif  int(X)==7:Speed=-4
				elif  int(X)==6:Speed=-5
				elif  int(X)<=5:Speed=-5


	#DIRECTION CALCULATION
	if int(Y)>=5:
		Direction=10
	elif int(Y)<=-5:
		Direction=-10
	else:
		Direction=int(Y)*2

	
	OutputString=str(Speed)+"+"+str(Direction)+"."


	#Printing Values on to the screen:
	print "GYRO: X: ",X," Y: ",Y," Z: ",Z
	print "SLIDER: S1: ",S1," S2: ",S2," S3: ",S3," S4: ",S4
	print "T1: ",T1," T2: ",T2," B1: ",B1
	print "Speed: ",Speed," Direction: ",Direction
	print "Raw: ",InputString

	
	#Reset Variables:
	X=0;Y=0;Z=0;S1=0;S2=0;S3=0;S4=0;T1=0;T2=0;B1=0;
	Speed=0;Direction=0;
	InputString=''
	OutputString=''
	Values=''
	Gyro=''


#arduino.close()
sock.close()
del sock
print('Programm ended.\n\n')

