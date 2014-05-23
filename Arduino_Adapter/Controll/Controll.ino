/*
  The Control programm for the UDOO RC Car

The programm waits for the serial data and use the values to control the robot.

INPUT FORM:
    
    String = "SPEED+DIRECTION."
    
    SPEED => Is the value for the speed, From -10 to 10;
    DIRECTION => Is the value for servo direction, From -10 to 10;
    
    
Created 19 May 2014
by Kevin Pan

*/

// include the servo library
#include <Servo.h>
#define SpeedPin 9
#define DirectionPin 10

//<90Degree=>forward;>90=>backward;=90=>stop
#define forward 75
#define backward 105
#define left 60
#define right 120

//Device Definition
Servo Dir_Servo;
Servo Drive_Motor;

String inputString = "";   // Holding incomming data
boolean stringComplete = false;  // whether the string is complete
int motorspeed_raw=0;   //Motor speed -10 to 10
int motorspeed=0;   //Motor speed
int servodirection_raw=0; // Servo Direction -10 to 10
int servodirection=0; // Servo Direction

void setup(){
  //initialize serial:
  Serial.begin(9600);
  Serial.println("Programm Started\n\nPlease wait.....");
  
  //Pin Mode setups:
  pinMode(SpeedPin,OUTPUT);
  pinMode(DirectionPin,OUTPUT);
  
  //attaching Motor Controller:
  Drive_Motor.attach(SpeedPin);
  Drive_Motor.write(90);
  delay(3000);
  
  //attaching Direction Servo:
  Dir_Servo.attach(DirectionPin);
  Dir_Servo.write(90);
  delay(1000);
  Serial.println("Already for drive....");
}

void loop(){
  
  
  //wait until the data completly comes:
  if (stringComplete) {
    
    //split string:
    int plus=inputString.indexOf("+");
    int dot=inputString.indexOf(".");
    String ms_raw=inputString.substring(0,plus);
    String sd_raw=inputString.substring(plus+1,dot);
    
    //convert the raw string data into int
    motorspeed_raw=ms_raw.toInt();
    servodirection_raw=sd_raw.toInt();
    
    //map the raw value
    motorspeed=map(motorspeed_raw,-10,10,70,110);
    servodirection=map(servodirection_raw,-10,10,60,120);
    
    
    Serial.print(motorspeed);Serial.print("   ");Serial.println(servodirection);
    
    //RUN
    Drive_Motor.write(motorspeed);
    Dir_Servo.write(servodirection);  
    
    // clear the string:
    inputString = "";
    stringComplete = false;
  }
}

void serialEvent(){
  while(Serial.available()){
    //get new byte and transform it in to char -> ascii
    char inChar = (char)Serial.read();
    //add it in to incomming inputString
    inputString += inChar;
    //Check if the incomming Data array ends;
    if(inChar == '.'){
      stringComplete = true;
      Serial.print("SENT!!!");
    }
  }
}

