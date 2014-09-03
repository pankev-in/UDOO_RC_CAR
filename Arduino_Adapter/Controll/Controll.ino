/*
 	Program: GCER 2014 OPEN GAME: Andriod Control Mode
 	Member: Kalus Ableitinger , Kevin Pan
 	Date: 07.2014
*/

//External libraries:
#include <Roomba.h>
#include <Servo.h>
#include <Motor.h>

//Pin connections:
#define M1_EN_PIN 2
#define M1_INA_PIN 22
#define M1_INB_PIN 23
#define M2_EN_PIN 3
#define M2_INA_PIN 24
#define M2_INB_PIN  25
#define SERVO_FRONT_PIN  4
#define SERVO_BACK_PIN  5
#define SERVO_GRAB_PIN  6
#define SERVO_DEFENSE_PIN 7
#define POTENTIOMETER_1_PIN  1
#define POTENTIOMETER_2_PIN  2

//Constants:
#define NUM_SERVO_FRONT_ZERO_DEGREE 90
#define NUM_SERVO_BACK_ZERO_DEGREE 95
#define NUM_SERVO_GRAB_CLOSE 0
#define NUM_SERVO_GRAB_OPEN 100
#define NUM_POTENTIOMETER_1_ZERO_DEGREE 330
#define NUM_POTENTIOMETER_1_MAX_ANGLE 108
#define NUM_POTENTIOMETER_1_MIN_ANGLE -98
#define NUM_POTENTIOMETER_2_ZERO_DEGREE 310
#define NUM_POTENTIOMETER_2_MAX_ANGLE 115
#define NUM_POTENTIOMETER_2_MIN_ANGLE -93
#define NUM_ROOMBA_TURN_SPEED 213
#define NUM_LIGHT_SENSOR_VALUE 40
#define NUM_CLIFF_BLACKTAPE_VALUE 200

//Objects define:
Roomba roomba (&Serial1);
Servo SERVO_FRONT;
Servo SERVO_BACK;
Servo SERVO_GRAB;
Servo SERVO_DEFENCE;
Motor m1;
Motor m2;

int go;
int back;
int left;
int right;
int primary_arm_angle;
int secondary_arm_angle;
int defence_arm_angle;
int grab_base_angle;
int grab_angle;
int index[9];


unsigned int u;
String inputString = "";   // Holding incomming data
boolean stringComplete = false;  // whether the string is complete

void setup() {
    
    Serial.begin(9600);
    Serial.println("Serial communication established");
    SERVO_FRONT.attach(SERVO_FRONT_PIN);
    SERVO_BACK.attach(SERVO_BACK_PIN);
    SERVO_GRAB.attach(SERVO_GRAB_PIN);
	SERVO_DEFENCE.attach(SERVO_DEFENSE_PIN);
	m1.attach(M1_EN_PIN, M1_INA_PIN, M1_INB_PIN);
	m2.attach(M2_EN_PIN, M2_INA_PIN, M2_INB_PIN);
    roomba.start();
    roomba.safeMode();
}

void loop() {
    
    //wait until the data completly comes:
    if (stringComplete) {
        
            index[0]=inputString.indexOf(";");
        for(int i=1;i<=8;i++){
            index[i]=inputString.indexOf(";",index[i-1]+1);
        }
        
        go=inputString.substring(0,index[0]).toInt();
        back=inputString.substring(index[0]+1,index[1]).toInt();
        left=inputString.substring(index[1]+1,index[2]).toInt();
        right=inputString.substring(index[2]+1,index[3]).toInt();
        primary_arm_angle=inputString.substring(index[3]+1,index[4]).toInt();
        secondary_arm_angle=inputString.substring(index[4]+1,index[5]).toInt();
        defence_arm_angle=inputString.substring(index[5]+1,index[6]).toInt();
        grab_base_angle=inputString.substring(index[6]+1,index[7]).toInt();
        grab_angle=inputString.substring(index[7]+1,index[8]).toInt();
        
        
        
        if(back==0&&go==1&&left==0&right==0){
            roomba.driveDirect(200,200);
        }
        else if(back==1&&go==0&&left==0&right==0){
            roomba.driveDirect(-200,-200);
        }
        else if(back==0&&go==0&&left==1&right==0){
            roomba.drive(NUM_ROOMBA_TURN_SPEED, roomba.DriveInPlaceCounterClockwise);
        }
        else if(back==0&&go==0&&left==0&right==1){
            roomba.drive(NUM_ROOMBA_TURN_SPEED, roomba.DriveInPlaceClockwise);
        }
        else{
            roomba.driveDirect(0,0);
        }
        moveAll(primary_arm_angle,secondary_arm_angle,grab_base_angle,grab_angle,defence_arm_angle);
        
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
        if(inChar == '｜'){
            stringComplete = true;
        }
    }
}
           
String getValue(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = {0, -1};
    int maxIndex = data.length()-1;
            
    for(int i=0; i<=maxIndex && found<=index; i++){
        if(data.charAt(i)==separator || i==maxIndex){
            found++;
            strIndex[0] = strIndex[1]+1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
            }
    }
            
    return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void moveAll(int primaryArmPos, int secondaryArmPos, int grabBasePos, int grabPos, int defensePos) {

    if(primaryArmPos > 45|| primaryArmPos < -45) return;
    if(secondaryArmPos > NUM_POTENTIOMETER_1_MAX_ANGLE || secondaryArmPos < NUM_POTENTIOMETER_1_MIN_ANGLE) return;
    if(grabBasePos > NUM_POTENTIOMETER_2_MAX_ANGLE || grabBasePos < NUM_POTENTIOMETER_2_MIN_ANGLE) return;
    if(grabPos > 100 || grabPos < 0) return;
    if(defensePos > 180 || defensePos < 0) return;

    SERVO_FRONT.write(NUM_SERVO_FRONT_ZERO_DEGREE - primaryArmPos);
    SERVO_BACK.write(NUM_SERVO_BACK_ZERO_DEGREE + primaryArmPos);
    SERVO_DEFENCE.write(defensePos);
    SERVO_GRAB.write(grabPos);
  
    int secondaryDiff = secondaryArmPos - checkSecondaryArmAngle();
	if(secondaryDiff < 5 && secondaryDiff > -5){
        
		Serial.println("Secondary Arm is not going to turn.");
		Serial.print("Diff:");Serial.println(secondaryDiff);
	} else if(secondaryDiff > 0){
        
		m1.forward(255);
	} else if(secondaryDiff < 0){
		m1.backward(255);
	}
    
    int grabDiff = secondaryArmPos - checkGrabAngle();
	if(grabDiff < 5 && grabDiff > -5){
        
		Serial.println("Grab is not going to turn.");
		Serial.print("Diff:");Serial.println(grabDiff);
	} else if(grabDiff < 0){
		
        m2.backward(200);
	} else if(grabDiff > 0){
        
		m2.forward(200);
	}
    
	while((grabDiff > 5 || grabDiff < -5) || (secondaryDiff > 5 || secondaryDiff < -5)){
        
        grabDiff = grabBasePos - checkGrabAngle();
        secondaryDiff = secondaryArmPos - checkSecondaryArmAngle();
        
        if(secondaryDiff < 5 || secondaryDiff > -5){m1.brake();}
        if(grabDiff < 5 || grabDiff > -5)  
        m2.brake();
	}
}

// Turn Secondary arm in to an specific angle between -110 to 110 degree:
// Status: Untested
void secondaryArmPosition(int angle){
	if(angle > NUM_POTENTIOMETER_1_MAX_ANGLE || angle < NUM_POTENTIOMETER_1_MIN_ANGLE){		//Check if the input angle is posible
		return;
	}
	int diff =angle - checkSecondaryArmAngle();		//calculate the difference
	if(diff<5&&diff>-5){
		Serial.println("Secondary Arm is not going to turn.");
		Serial.print("Diff:");Serial.println(diff);
	}
	else if(diff>0){
		m1.forward(255);
	}
	else if(diff<0){
		m1.backward(255);
	}
	while(diff>5||diff<-5){
        diff =angle - checkSecondaryArmAngle();
	}
    m1.brake();
}

// Turn the Grabber in to an specific angle between -110 to 110 degree:
// Status: Untested
void grabBasePosition(int angle) {
	if(angle > NUM_POTENTIOMETER_2_MAX_ANGLE || angle < NUM_POTENTIOMETER_2_MIN_ANGLE){		//Check if the input angle is posible
		return;
	}
	int diff =angle - checkGrabAngle();		//calculate the difference
	if(diff<5&&diff>-5){
		Serial.println("Grab is not going to turn.");
		Serial.print("Diff:");Serial.println(diff);
	}
	else if(diff<0){
		m2.backward(200);       //Here is Backward!!!!
	}
	else if(diff>0){
		m2.forward(200);
	}
	while(diff>5||diff<-5){
        diff =angle - checkGrabAngle();
	}
    m2.brake();
}

// Returns the Angle of the grabbler:
// Status: TESTED
int checkGrabAngle() {
   	int value=analogRead(POTENTIOMETER_2_PIN);
	value=map(value,0,697,NUM_POTENTIOMETER_2_MIN_ANGLE,NUM_POTENTIOMETER_2_MAX_ANGLE);
  	return value;
}

// Returns the Angle of the secondary Arm:
// Status: TESTED
int checkSecondaryArmAngle(){
   	int value=analogRead(POTENTIOMETER_1_PIN);
   	value=map(value,0,697,NUM_POTENTIOMETER_1_MIN_ANGLE,NUM_POTENTIOMETER_1_MAX_ANGLE);
   	return value;
}




