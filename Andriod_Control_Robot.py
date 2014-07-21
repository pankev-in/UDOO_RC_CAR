#!/usr/bin/python

import serial
import socket
import sys
from time import sleep
from sys import argv

HOST=''
PORT=0

S1=0;#Slider - Prime Arm Position;
S2=0;#Slider - Secondary Arm Position;
S3=0;#Slider - Defence Arm Position;
S4=0;#Slider - Grab Base Position;
S5=0;#Slider - Grab Position;
B1=0;#Button - 'Forward'
B2=0;#Button - 'Backward'
B3=0;#Button - 'TurnLeft'
B4=0;#Button - 'TurnRight'
SAVE_B=0;
savePressed=False

NUM_POTENTIOMETER_1_MAX_ANGLE=108
NUM_POTENTIOMETER_1_MIN_ANGLE=-98
NUM_POTENTIOMETER_2_MAX_ANGLE=115
NUM_POTENTIOMETER_2_MIN_ANGLE=-93
NUM_SERVO_GRAB_CLOSE=0
NUM_SERVO_GRAB_OPEN=100
NUM_PRIME_MAX_ANGLE=45
NUM_PRIME_MIN_ANGLE=-45
NUM_DEFENCE_MAX_ANGLE=180
NUM_DEFENCE_MIN_ANGLE=0

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
arduino = serial.Serial("/dev/ttyACM0",9600)
print ("\nSerial Connection with Arduino Created")


#Socket Connection
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((HOST,PORT))
print '\nSocket Connected:'
print "Connected to Host Address:",HOST
print "Connected to Port Number:",PORT,"\n\n"
target = open("robotPosition.txt", 'w');
target.write("\n\n\n")



while True:
	#Buffering Data income:
	InputString=sock.recv(BufferSize)

	#End program by sending '<stop>' string:
	if InputString[1:5] == 'STOP':
		print("Disconnected form Client")
		sys.exit()


	#Editing Values:
	Values=InputString.split(";")
	try:
		B1=int(Values[1]);
		B2=int(Values[2]);
		B3=int(Values[3]);
		B4=int(Values[4]);
		S1=int(Values[5].lstrip("{S").rstrip("}"))
		S2=int(Values[6].lstrip("{S").rstrip("}"))
		S3=int(Values[7].lstrip("{S").rstrip("}"))
		S4=int(Values[8].lstrip("{S").rstrip("}"))
		S5=int(Values[9].lstrip("{S").rstrip("}"))
		B5=Values[10]
		SAVE_B=int(B5[0:1])
		breakout=0;

	except (ValueError,IndexError) as e:
		B1=0;B2=0;B3=0;B4=0;
		breakout=breakout+1
		if breakout>=5:
			sys.exit("\nConnection breaks\n");
		pass


	S1=-int(S1/float(SliderMax)*45)

	if S2>0:
		S2=int(S2/float(SliderMax)*NUM_POTENTIOMETER_1_MIN_ANGLE)
	elif S2<0:
		S2=-int(S2/float(SliderMax)*NUM_POTENTIOMETER_1_MAX_ANGLE)
	
	if S4>0:
		S4=int(S4/float(SliderMax)*NUM_POTENTIOMETER_2_MIN_ANGLE)
	elif S4<0:
		S4=-int(S4/float(SliderMax)*NUM_POTENTIOMETER_2_MAX_ANGLE)
	
	S3=-int((S3-SliderMax)/float(SliderMax)*NUM_DEFENCE_MAX_ANGLE)/2
	S5=-int((S5-SliderMax)/float(SliderMax)*NUM_SERVO_GRAB_OPEN)/2



	#Printing Values on to the screen:
	print "Forward:",B1,"Backward:",B2,"Left:",B3,"Right:",B4
	print "S1: ",S1," S2: ",S2," S3: ",S3," S4: ",S4," S5: ",S5
	OutputString=str(S1)+";"+str(S2)+";"+str(S3)+";"+str(S4)+";"+str(S5)

	if SAVE_B==1:
		print "Save Pressed";
		savePressed=True;
	else:
		if savePressed==True:
			target.write(OutputString)
			target.write("\n")
			savePressed=False;
		print "Save not Pressed"
	
	OutputString=str(B1)+";"+str(B2)+";"+str(B3)+";"+str(B4)+";"+str(S1)+";"+str(S2)+";"+str(S3)+";"+str(S4)+";"+str(S5)+"|"

	arduino.write(OutputString);

	#Reset Variables:
	B1=0;#Button - 'Forward'
	B2=0;#Button - 'Backward'
	B3=0;#Button - 'TurnLeft'
	B4=0;#Button - 'TurnRight'
	InputString=''
	OutputString=''
	Values=''

arduino.close()
target.close()
sock.close()
del sock
print('Programm ended.\n\n')

