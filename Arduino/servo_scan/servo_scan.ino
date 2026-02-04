#include <Servo.h>

Servo scanServo;

#define SERVO_PIN 13
#define START_ANGLE 0
#define END_ANGLE 160
#define STEP_ANGLE 20
#define HOLD_TIME 2000

void setup() {
  Serial.begin(115200);
  scanServo.attach(SERVO_PIN);
}

void loop() {
  for (int angle = START_ANGLE; angle <= END_ANGLE; angle += STEP_ANGLE) {
    scanServo.write(angle);
    delay(HOLD_TIME);
  }
  while(true);
}
