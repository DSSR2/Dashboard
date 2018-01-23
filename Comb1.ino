/*
 * ARDUINO 1. UNO
 * RPM 2x
 * Suspension Travel 2x
 * GPS
 * Steering angle
 */
 
 //GPS
#include "TinyGPS++.h"
#include "SoftwareSerial.h"
SoftwareSerial serial_connection(10, 11); //RX=pin 10, TX=pin 11
TinyGPSPlus gps;

//RPM 1
int iPin=0;
float rpm;
int flag;
volatile int t;
unsigned int lastInterrupt=0;
unsigned int prevInterrupt=0;
unsigned int currInterrupt=0;
unsigned int loopTime=0;

//RPM 2
int iPin2=1;
float rpm2;
int flag2;
volatile int t2;
unsigned int lastInterrupt2=0;
unsigned int prevInterrupt2=0;
unsigned int currInterrupt2=0;

//Suspension travel
const int susPin1 = 0; 
const int susPin2 = 1;// Analog input pin that the potentiometer is attached to
int sensorValue = 0;        // value read from the pot
int outputValue = 0;        // value output to the PWM (analog out)

//Steering angle
int steering =2;

void setup(){
  Serial.begin(9600);
  serial_connection.begin(9600);
  attachInterrupt(iPin,k,RISING);
  attachInterrupt(iPin2,j,RISING);
  flag=0;
  flag2=0;
}


void loop(){
  //Suspension travel
    sus(susPin1);
    delay(10);
    Serial.print(", ");
    sus(susPin2);
    Serial.println();
    delay(10);
    
  //Steering angle
    ster(steering);
    
  //GPS
    if(serial_connection.available())//While there are characters to come from the GPS
    {
      gps.encode(serial_connection.read());//This feeds the serial NMEA data into the library one char at a time
    }
    if(gps.location.isUpdated())//This will pretty much be fired all the time anyway but will at least reduce it to only after a package of NMEA data comes in
    {
      //Get the latest info from the gps object which it derived from the data sent by the GPS unit
      //Serial.println("Satellite Count:");
      //Serial.println(gps.satellites.value());
      //Serial.println("Latitude:");
      Serial.print(gps.location.lat(), 6);
      Serial.print(", ");
      //Serial.println("Longitude:");
      Serial.print(gps.location.lng(), 6);
      Serial.print(", ");
      //Serial.println("Speed MPH:");
      Serial.println(gps.speed.kmph());
      //Serial.println("Altitude Feet:");
      //Serial.println(gps.altitude.feet());
      //Serial.println("");
    }

  //RPM
  if(millis()-loopTime>1000){    
    detachInterrupt(iPin);
    detachInterrupt(iPin2);
    float tSec=float(t)/1000;
    rpm=(1/tSec)*60;
    //Serial.print(t);
    //Serial.print(", ");
    if(!isfinite(rpm))
      rpm=0;
    Serial.print(rpm);
    Serial.print(", ");

    float tSec2=float(t2)/1000;
    rpm2=(1/tSec2)*60;
    //Serial.print(t2);
    //Serial.print(", ");
    if(!isfinite(rpm2))
      rpm2=0;
    Serial.println(rpm2);

    
    loopTime=millis();
    t=0;
    t2=0;
    attachInterrupt(iPin,k,RISING);
    attachInterrupt(iPin2,j,RISING);    
  }  
}

void k(){  
  if(millis() - lastInterrupt > 10 ){    
      if(flag==1){
        currInterrupt=millis();
        flag=0;
        t=currInterrupt-prevInterrupt;
      }
      else{
        prevInterrupt=millis();
        flag=1;
        t=0;
      }
    lastInterrupt = millis();
  }  
}

void j(){  
  if(millis() - lastInterrupt2 > 10 ){    
      if(flag2==1){
        currInterrupt2=millis();
        flag2=0;
        t2=currInterrupt2-prevInterrupt2;
      }
      else{
        prevInterrupt2=millis();
        flag2=1;
        t2=0;
      }
    lastInterrupt2 = millis();
  }  
}

void steering(int pin){
    val=analogRead(pin);
    ang=map(val, 0,1023, 0,360);
    Serial.println(ang); 
}

void sus(int pin){
    sensorValue=analogRead(pin);
    outputValue = map(sensorValue, 0, 1023, 0, 100);
    Serial.print(outputValue);
}
