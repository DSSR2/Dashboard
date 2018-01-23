/*
 * ARDUINO 2 MEGA
 * RPM 2x
 * Suspension Travel 2x
 * Engine RPM
 * Geaar Pos
 * Thermocouple
 */
#include <max6675.h>
//ThermoCouples
float temp1, temp2, temp3;
int t1SO=22;
int t1CS=23;
int t1SCK=24;

int t2SO=25;
int t2CS=26;
int t2SCK=27;

int t3SO=28;
int t3CS=29;
int t3SCK=30;

MAX6675 tc1(t1SCK, t1CS, t1SO);
MAX6675 tc2(t2SCK, t2CS, t2SO);
MAX6675 tc3(t3SCK, t3CS, t3SO);

//Engine RPM
int engRPM=3;
 
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
int sus1,sus2;
const int susPin1 = 0; 
const int susPin2 = 1;// Analog input pin that the potentiometer is attached to

void setup() {
  Serial.begin(9600);
  attachInterrupt(iPin,k,RISING);
  attachInterrupt(iPin2,j,RISING);
  flag=0;
  flag2=0;
}

void loop() {
  //Thermocouples
    temp1=tc1.readCelsius();
    temp2=tc2.readCelsius();
    temp3=tc3.readCelsius();
  //Engine RPM
    int eng=analogRead(engRPM);
  //Suspension travel
    sus1=sus(susPin1);
    delay(10);
    sus2=sus(susPin2);
    delay(10);
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
  
      float tSec2=float(t2)/1000;
      rpm2=(1/tSec2)*60;
      //Serial.print(t2);
      //Serial.print(", ");
      if(!isfinite(rpm2))
        rpm2=0;
      
      loopTime=millis();
      t=0;
      t2=0;
      attachInterrupt(iPin,k,RISING);
      attachInterrupt(iPin2,j,RISING); 

      String finalOP=""+String(temp1) + ", " + temp2 + ", " + temp3+", "+sus1+", "+sus2+", "+eng+", "+rpm+", "+rpm2;
      Serial.println(rpm);
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

int sus(int pin){
    int sensorValue=analogRead(pin);
    int outputValue = map(sensorValue, 0, 1023, 0, 100);
    return(outputValue);
}
