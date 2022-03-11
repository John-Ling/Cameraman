#include <Arduino.h>
#include <Servo.h>

Servo motorX;
Servo motorY; 


void setup() {
  motorX.attach(10);
  motorY.attach(9);
  motorX.write(30);
  motorY.write(30);

}

void loop() {
    motorX.write(60);
    delay(1000);
    motorX.write(0);
    delay(1000);
    motorY.write(60);
    delay(1000);
    motorY.write(0);
    delay(1000);
}   