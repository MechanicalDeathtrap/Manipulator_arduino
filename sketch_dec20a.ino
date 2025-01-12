#include <ServoEasing.hpp>


ServoEasing servo1;
ServoEasing servo2;
ServoEasing servo3;

const int SERVO1_PIN = 2;
const int SERVO2_PIN = 3;
const int SERVO3_PIN = 4;

int currentAngle1 = 180;
int currentAngle2 = 90;
int currentAngle3 = 90;
const int stepSize = 1;
const int stepDelay = 20;
int servoSpeed = 50;

void setup() {
  Serial.begin(9600);  
  servo1.attach(SERVO1_PIN, 500, 2500, 0, 180);
  servo2.attach(SERVO2_PIN, 500, 2500, 0, 180);
  servo3.attach(SERVO3_PIN, 500, 2500, 0, 180);

  servo1.setEasingType(EASE_LINEAR);
  servo2.setEasingType(EASE_LINEAR);
  servo3.setEasingType(EASE_LINEAR);

  servo1.write(160);
  servo2.write(90);
  servo3.write(90);

  
  setSpeedForAllServos(servoSpeed);
}

void moveServoSmoothly(ServoEasing &servo, int &currentAngle, int targetAngle) {
  while (currentAngle != targetAngle) {
    if (currentAngle < targetAngle) {
      currentAngle += stepSize; 
    } else {
      currentAngle -= stepSize;
    }
    servo.setEaseTo(currentAngle);
    delay(stepDelay); 
  }
}


void loop() {

  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');  
    data.trim();  

    // Разбиваем строку на углы
    int separator1 = data.indexOf(',');
    int separator2 = data.lastIndexOf(',');

    if (separator1 != -1 && separator2 != -1) {
      int angle1 = data.substring(0, separator1).toInt();
      int angle2 = data.substring(separator1 + 1, separator2).toInt();
      int angle3 = data.substring(separator2 + 1).toInt();

      if (angle2 < 5) {
        angle2 = 5;
    }

      moveServoSmoothly(servo1, currentAngle1, angle1);
      moveServoSmoothly(servo2, currentAngle2, angle2);
      moveServoSmoothly(servo3, currentAngle3, angle3);

      synchronizeAllServosStartAndWaitForAllServosToStop();
      delay(500);
      


      Serial.println("OK");
    }
  }
}