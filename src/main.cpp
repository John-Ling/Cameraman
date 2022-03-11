#include <Arduino.h>
#include <Servo.h>

const int PIN_X = 10;
const int PIN_Y = 9;
const float SCALING_X = 0.1099;
const float SCALING_Y = 0.1428;

Servo motorX;
Servo motorY; 

int indexOfSeparator = 0;
String serialData;
float dataX;
float dataY;

void setup() {
  motorX.attach(PIN_X);
  motorY.attach(PIN_Y);
  motorX.write(30);
  motorY.write(30);
  Serial.begin(9600);
  Serial.setTimeout(50);
}

void loop() {
  if (Serial.available())
  {
    serialData = Serial.readStringUntil('\0');  
    indexOfSeparator = serialData.indexOf(':');
    dataX = (serialData.substring(0, indexOfSeparator)).toFloat();
    dataY = (serialData.substring(indexOfSeparator + 1)).toFloat();
    dataX = round(dataX * SCALING_X);
    dataY = round(dataY * SCALING_Y);
    motorX.write(dataX);
    motorY.write(dataY);
  }
}