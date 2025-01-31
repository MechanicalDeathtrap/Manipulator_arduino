#include <ServoEasing.hpp>
#include <math.h>

ServoEasing servo1;
ServoEasing servo2;
ServoEasing servo3;

const int SERVO1_PIN = 2;
const int SERVO2_PIN = 3;
const int SERVO3_PIN = 4;

int currentAngle1 = 160; 
int currentAngle2 = 90;
int currentAngle3 = 90;
const int stepSize = 1;
const int stepDelay = 20;
int servoSpeed = 50;

const float L1 = 75; 
const float L2 = 65; 

float digit1[][2] = {
  {5.0, 5.0}, {8.0, 5.0} 
};

float digit2[][2] = {
  {5.0, 5.0}, {5.0, 8.0}, 
  {3.5, 5.0}, {3.5, 8.0}  
};

float digit3[][2] = {
  {2.5, 5.0}, 
  {5.0, 2.0}, {5.0, 7.0}, 
  {7.5, 2.0}, {7.5, 7.0}  
};


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
    currentAngle += (currentAngle < targetAngle) ? stepSize : -stepSize;
    servo.setEaseTo(currentAngle);
    delay(stepDelay);
  }
}

void moveToPoint(float x, float y) {
  x *= 10; 
  y *= 10;

  float theta2 = acos((x * x + y * y - L1 * L1 - L2 * L2) / (2 * L1 * L2));
  float theta1 = atan2(y, x) - atan2(L2 * sin(theta2), L1 + L2 * cos(theta2));

  int angle1 = 180;
  int angle2 = degrees(theta1);
  int angle3 = degrees(theta2); 
  
  moveServoSmoothly(servo1, currentAngle1, angle1);
  moveServoSmoothly(servo2, currentAngle2, angle2);
  moveServoSmoothly(servo3, currentAngle3, angle3);

  synchronizeAllServosStartAndWaitForAllServosToStop();
  delay(500);
}

void drawDigit(float digit[][2], int pointsCount) {
  servo1.setEaseTo(150);
  moveToPoint(digit[0][0], digit[0][1]);
  delay(1000);
  servo1.setEaseTo(180);
  synchronizeAllServosStartAndWaitForAllServosToStop();

  for (int i = 1; i < pointsCount; i++) {
    moveToPoint(digit[i][0], digit[i][1]);
  }

  servo1.setEaseTo(160);
  synchronizeAllServosStartAndWaitForAllServosToStop();
  delay(500);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    data.trim();
    int digit = data.toInt();

    switch (digit) {
      case 1:
        drawDigit(digit1, sizeof(digit1) / sizeof(digit1[0]));
        break;
      case 2:
        drawDigit(digit2, sizeof(digit2) / sizeof(digit2[0]));
        break;
      case 3:
        drawDigit(digit3, sizeof(digit3) / sizeof(digit3[0]));
        break;
      default:
        Serial.println("Некорректная цифра!");
        break;
    }
    Serial.println("OK");
  }
}
