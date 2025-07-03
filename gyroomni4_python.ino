#include <Wire.h>
#include <MPU6050.h>
#include "BluetoothSerial.h"
#include <ESP32PWM.h>

// Motor Pins
#define MOTOR1_DIR 16 
#define MOTOR1_PWM 4
#define MOTOR2_DIR 2
#define MOTOR2_PWM 15
#define MOTOR3_DIR 27
#define MOTOR3_PWM 14
#define MOTOR4_DIR 12
#define MOTOR4_PWM 13
#define RELAY_PIN 23   // Relay control pin (active-high)
// Motor A pins
#define IN1 17
#define IN2 5
#define ENA 18  // PWM for Motor A

// Motor B pins
#define IN3 32
#define IN4 33
#define ENB 25  // PWM for Motor B

#define PWM_FREQ 1000
#define PWM_RESOLUTION 8

// Command Definitions (add new servo commands)
#define STOP_COMMAND 1
#define FORWARD_COMMAND 2
#define LEFT_COMMAND 3
#define RIGHT_COMMAND 4
#define ROTATE_LEFT_COMMAND 5
#define ROTATE_RIGHT_COMMAND 6
#define ROTATE_TO_COMMAND 7
#define RETURN_TO_0DEGREE 8
#define RELAY_ON_COMMAND 9
#define RELAY_OFF_COMMAND 10
#define RELAY_TOGGLE_COMMAND 11
#define FRONT_LEFT_COMMAND 14
#define FRONT_RIGHT_COMMAND 15
#define AUTO_CORRECT_YAW_COMMAND 16
#define FORWARD_M2 17  // Move Forward
#define STOP_M2 18     // Stop Movement


MPU6050 mpu;
BluetoothSerial SerialBT;

// IMU Variables
int16_t gyroX, gyroY, gyroZ;
float yaw = 0;
float gyroZ_offset = 0;
unsigned long lastTime = 0;
float elapsedTime;

// Movement Control
int motorSpeed = 50;
bool moveForwardFlag = false;
bool moveBackwardFlag = false;
bool moveLeftFlag = false;
bool moveRightFlag = false;
bool rotationleftFlag = false;
bool rotationrightFlag = false;
bool returnToZeroFlag = false;
bool isStopped = false;
bool moveFrontLeftFlag = false;
bool moveFrontRightFlag = false;

int speedA = 255;
int speedB = 255;

// Relay Control
unsigned long relayTimer = 0;
bool relayAutoOffEnabled = false;
unsigned long RELAY_PULSE_DURATION = 100; // 1 second auto-off

// Rotation Parameters
float targetYaw = 0;
const float yawTolerance = 3.0;
const int rotationSpeed = 50;

// Motor Offsets
typedef struct {
  float m1Offset;
  float m2Offset;
  float m3Offset;
  float m4Offset;
} MotorOffsets;

MotorOffsets forwardOffsets = {-10.0, 0, -10.0, 0};
MotorOffsets backwardOffsets = {-0.2, -2, -0.2, -2.3};
MotorOffsets leftOffsets = {-1.4, -0.6, -1.5, -1.5};
MotorOffsets rightOffsets = {-1.2, -1.2, -1.2, -1};

void setup() {
  Serial.begin(115200);
  while(!Serial); // Wait for serial port to connect
  SerialBT.begin("ESP32_Robot");
  Wire.begin();

  // Initialize motor pins
  pinMode(MOTOR1_DIR, OUTPUT);
  pinMode(MOTOR1_PWM, OUTPUT);
  pinMode(MOTOR2_DIR, OUTPUT);
  pinMode(MOTOR2_PWM, OUTPUT);
  pinMode(MOTOR3_DIR, OUTPUT);
  pinMode(MOTOR3_PWM, OUTPUT);
  pinMode(MOTOR4_DIR, OUTPUT);
  pinMode(MOTOR4_PWM, OUTPUT);
  
  // Initialize relay pin
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);

  // Set motor pins as outputs
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // Setup PWM channels
  analogWrite(ENA, 255); // 50% duty cycle on ENA
  analogWrite(ENB, 255); // 100% duty cycle on ENB

  // Initialize MPU6050
  mpu.initialize();
  if (!mpu.testConnection()) {
    Serial.println("MPU6050 connection failed");
    while(1);
  }
  
  // Then calibrate gyro
  calibrateGyro();
  
  lastTime = millis();
  Serial.println("READY"); // Handshake message
}

void loop() {
  // Check if relay needs auto-off
  if (relayAutoOffEnabled && (millis() - relayTimer >= RELAY_PULSE_DURATION)) {
    digitalWrite(RELAY_PIN, LOW);
    relayAutoOffEnabled = false;
    Serial.println("Relay auto-off");
  }

  checkSerial();
  updateYaw();
  checkBluetooth();
  
  // Movement state machine
  if (returnToZeroFlag) {
    returnToZero();
  } 
  else if (moveForwardFlag) {
    moveForward();
  } 
  else if (moveLeftFlag) {
    turnLeft();
  } 
  else if (moveRightFlag) {
    turnRight();
  } 
  else if (moveBackwardFlag) {
    moveBackward();
  } 
  else if (rotationleftFlag || rotationrightFlag) {
    executeRotation();
  }
  else if (moveFrontLeftFlag) {
    moveFrontLeft();
  } 
  else if (moveFrontRightFlag) {
    moveFrontRight();
  }
  else {
    stopMovement();
  }

  delay(10);
}

void calibrateGyro() {
  for (int i = 0; i < 1000; i++) {
    mpu.getRotation(&gyroX, &gyroY, &gyroZ);
    gyroZ_offset += gyroZ;
    delay(2);
  }
  gyroZ_offset /= 1000;
}

void checkSerial() {
  if (Serial.available() >= 6) {
    byte header = Serial.read();
    byte identifier = Serial.read();
    byte lowbyte = Serial.read();
    byte lowbyte_checksum = Serial.read();
    byte highbyte = Serial.read();
    byte highbyte_checksum = Serial.read();

    // Verify packet structure and checksums
    if (header == 0xFF && identifier == 0x55 && 
        (lowbyte + lowbyte_checksum == 255) && 
        (highbyte + highbyte_checksum == 255)) {
      
      int command = highbyte;
      int speed = lowbyte;
      
      // Send acknowledgment
      Serial.print("ACK:");
      Serial.print(command);
      Serial.print(",");
      Serial.println(speed);
      
      executeCommand(command, speed);
    }
  }
}

void executeCommand(int command, int speed) {
  isStopped = false;  // Clear stop flag
  resetMovementFlags();
  motorSpeed = constrain(speed, 0, 255);

  switch (command) {
    case STOP_COMMAND:
      stopMovement();
      break;
    case FORWARD_COMMAND:
      moveForwardFlag = true;
      targetYaw = yaw;
      break;
    case LEFT_COMMAND:
      moveLeftFlag = true;
      break;
    case RIGHT_COMMAND:
      moveRightFlag = true;
      break;
    case ROTATE_LEFT_COMMAND:
      rotationleftFlag = true;
      break;
    case ROTATE_RIGHT_COMMAND:
      rotationrightFlag = true;
      break;
    case ROTATE_TO_COMMAND:
      targetYaw = speed;
      returnToZeroFlag = true;
      break;
    case RETURN_TO_0DEGREE:
      targetYaw = 0;
      returnToZeroFlag = true;
      break;
    case RELAY_ON_COMMAND:
      digitalWrite(RELAY_PIN, HIGH);
      relayTimer = millis();
      relayAutoOffEnabled = true;
      Serial.println("Relay ON (auto-off in 1s)");
      break;
    case RELAY_OFF_COMMAND:
      digitalWrite(RELAY_PIN, LOW);
      relayAutoOffEnabled = false;
      Serial.println("Relay FORCED OFF");
      break;
    case RELAY_TOGGLE_COMMAND:
      digitalWrite(RELAY_PIN, !digitalRead(RELAY_PIN));
      Serial.print("Relay TOGGLED to ");
      Serial.println(digitalRead(RELAY_PIN) ? "ON" : "OFF");
      break;
    case FRONT_LEFT_COMMAND:
      moveFrontLeftFlag = true;
      break;
    case FRONT_RIGHT_COMMAND:
      moveFrontRightFlag = true;
      break;
    case AUTO_CORRECT_YAW_COMMAND:
      autoCorrectYaw();
      break;
    case FORWARD_M2: // Move Forward
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
      break;
      
    case STOP_M2: // Stop Movement
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, LOW);
      break;
  }
  // Apply speeds
  ledcWrite(0, speedA); // Motor A
  ledcWrite(1, speedB); // Motor B
}

float smoothYaw = 0;
const float alpha = 0.9;

void updateYaw() {
  unsigned long currentTime = millis();
  elapsedTime = (currentTime - lastTime) / 1000.0;
  lastTime = currentTime;

  mpu.getRotation(&gyroX, &gyroY, &gyroZ);
  float rateGyroZ = -(gyroZ - gyroZ_offset) / 131.0;
  yaw += rateGyroZ * elapsedTime;

  yaw = fmod(yaw, 360);
  if (yaw < 0) yaw += 360;

  // Smoothing to reduce pulses
  smoothYaw = alpha * smoothYaw + (1 - alpha) * yaw;

  static unsigned long lastYawPrint = 0;
  if (millis() - lastYawPrint > 100) {
    Serial.print("Yaw: ");
    Serial.println(smoothYaw, 2);
    lastYawPrint = millis();
  }
}

void resetMovementFlags() {
  moveForwardFlag = false;
  moveBackwardFlag = false;
  moveLeftFlag = false;
  moveRightFlag = false;
  rotationleftFlag = false;
  rotationrightFlag = false;
  returnToZeroFlag = false;
  moveFrontLeftFlag = false;
  moveFrontRightFlag = false;
}

void moveForward() {
  // Simple forward movement without PID correction
  int leftSpeed = motorSpeed;
  int rightSpeed = motorSpeed;

  // Add small constant compensation for right drift
  rightSpeed -= 3;

  // Safety clamp
  leftSpeed = constrain(leftSpeed, 30, 255);
  rightSpeed = constrain(rightSpeed, 30, 255);

  digitalWrite(MOTOR1_DIR, LOW);
  digitalWrite(MOTOR2_DIR, LOW);
  digitalWrite(MOTOR3_DIR, LOW);
  digitalWrite(MOTOR4_DIR, LOW);

  moveMotors(&forwardOffsets, leftSpeed, rightSpeed);
}

void moveBackward() {
  // Simple backward movement without PID correction
  int leftSpeed = motorSpeed + 6;
  int rightSpeed = motorSpeed;

  // Clamp speeds safely
  leftSpeed = constrain(leftSpeed, 30, 255);
  rightSpeed = constrain(rightSpeed, 30, 255);

  digitalWrite(MOTOR1_DIR, HIGH);
  digitalWrite(MOTOR2_DIR, HIGH);
  digitalWrite(MOTOR3_DIR, HIGH);
  digitalWrite(MOTOR4_DIR, HIGH);

  moveMotors(&backwardOffsets, leftSpeed, rightSpeed);
}

void executeRotation() {
  if (rotationleftFlag) {
    digitalWrite(MOTOR1_DIR, HIGH);
    digitalWrite(MOTOR2_DIR, LOW);
    digitalWrite(MOTOR3_DIR, HIGH);
    digitalWrite(MOTOR4_DIR, LOW);
  } else {
    digitalWrite(MOTOR1_DIR, LOW);
    digitalWrite(MOTOR2_DIR, HIGH);
    digitalWrite(MOTOR3_DIR, LOW);
    digitalWrite(MOTOR4_DIR, HIGH);
  }
  moveMotors(&backwardOffsets, motorSpeed, motorSpeed);
}

void turnLeft() {
  digitalWrite(MOTOR1_DIR, HIGH);  // Left motors backward
  digitalWrite(MOTOR3_DIR, LOW);   // Right motors forward
  digitalWrite(MOTOR2_DIR, LOW);
  digitalWrite(MOTOR4_DIR, HIGH);
  
  // Apply speeds with offsets
  analogWrite(MOTOR1_PWM, motorSpeed + leftOffsets.m1Offset);
  analogWrite(MOTOR3_PWM, motorSpeed + leftOffsets.m3Offset);
  analogWrite(MOTOR2_PWM, motorSpeed + leftOffsets.m2Offset);
  analogWrite(MOTOR4_PWM, motorSpeed + leftOffsets.m4Offset);
}

void turnRight() {
  digitalWrite(MOTOR1_DIR, LOW);    // Left motors forward
  digitalWrite(MOTOR3_DIR, HIGH);   // Right motors backward
  digitalWrite(MOTOR2_DIR, HIGH);
  digitalWrite(MOTOR4_DIR, LOW);
  
  analogWrite(MOTOR1_PWM, motorSpeed + rightOffsets.m1Offset);
  analogWrite(MOTOR3_PWM, motorSpeed + rightOffsets.m3Offset);
  analogWrite(MOTOR2_PWM, motorSpeed + rightOffsets.m2Offset);
  analogWrite(MOTOR4_PWM, motorSpeed + rightOffsets.m4Offset);
}

void moveFrontLeft() {
  digitalWrite(MOTOR1_DIR, LOW);  // Motor1 Off
  digitalWrite(MOTOR2_DIR, LOW);  // Motor2 Forward
  digitalWrite(MOTOR3_DIR, LOW);  // Motor3 Forward
  digitalWrite(MOTOR4_DIR, LOW);  // Motor4 Off

  analogWrite(MOTOR1_PWM, 0);
  analogWrite(MOTOR2_PWM, motorSpeed);
  analogWrite(MOTOR3_PWM, motorSpeed);
  analogWrite(MOTOR4_PWM, 0);
}

void moveFrontRight() {
  digitalWrite(MOTOR1_DIR, LOW);  // Motor1 Forward
  digitalWrite(MOTOR2_DIR, LOW);  // Motor2 Off
  digitalWrite(MOTOR3_DIR, LOW);  // Motor3 Off
  digitalWrite(MOTOR4_DIR, LOW);  // Motor4 Forward

  analogWrite(MOTOR1_PWM, motorSpeed);
  analogWrite(MOTOR2_PWM, 0);
  analogWrite(MOTOR3_PWM, 0);
  analogWrite(MOTOR4_PWM, motorSpeed);
}

float calculateShortestPath(float currentAngle, float targetAngle) {
  float diff = targetAngle - currentAngle;
  if (diff > 180) {
    diff -= 360;
  } else if (diff < -180) {
    diff += 360;
  }
  return diff;
}

void returnToZero() {
  unsigned long startTime = millis();
  const unsigned long timeout = 5000; // 5-second timeout
  
  while (abs(calculateShortestPath(yaw, targetYaw)) > yawTolerance) {
    // Check for timeout
    if (millis() - startTime > timeout) {
      Serial.println("ReturnToZero timeout!");
      stopMovement();
      returnToZeroFlag = false;
      return;
    }
    
    // Update yaw FIRST
    updateYaw();
    
    float angleError = calculateShortestPath(yaw, targetYaw);
    int currentSpeed = rotationSpeed;

    // Set motor directions
    if (angleError > 0) { // Rotate right
      digitalWrite(MOTOR1_DIR, LOW);
      digitalWrite(MOTOR2_DIR, HIGH);
      digitalWrite(MOTOR3_DIR, LOW);
      digitalWrite(MOTOR4_DIR, HIGH);
    } else { // Rotate left
      digitalWrite(MOTOR1_DIR, HIGH);
      digitalWrite(MOTOR2_DIR, LOW);
      digitalWrite(MOTOR3_DIR, HIGH);
      digitalWrite(MOTOR4_DIR, LOW);
    }
    
    moveMotors(&backwardOffsets, currentSpeed, currentSpeed);
    
    // Small delay to allow IMU updates
    delay(10);
    
    // Optional: Add early exit if stopped by user
    if (Serial.available() || SerialBT.available()) {
      char c = Serial.read() || SerialBT.read();
      if (c == 'X') { // Stop command
        stopMovement();
        returnToZeroFlag = false;
        return;
      }
    }
  }
  
  // Reached target
  stopMovement();
  returnToZeroFlag = false;
  Serial.print("Reached target yaw: ");
  Serial.println(yaw, 2);
}

void autoCorrectYaw() {
  float angleError = calculateShortestPath(yaw, 0);

  if (abs(angleError) > 1.0) {
    int correctionSpeed = 50; // Fixed correction speed

    if (angleError > 0) {  // Rotate right
      digitalWrite(MOTOR1_DIR, LOW);
      digitalWrite(MOTOR2_DIR, HIGH);
      digitalWrite(MOTOR3_DIR, LOW);
      digitalWrite(MOTOR4_DIR, HIGH);
    } else {  // Rotate left
      digitalWrite(MOTOR1_DIR, HIGH);
      digitalWrite(MOTOR2_DIR, LOW);
      digitalWrite(MOTOR3_DIR, HIGH);
      digitalWrite(MOTOR4_DIR, LOW);
    }

    moveMotors(&backwardOffsets, correctionSpeed, correctionSpeed);
  } else {
    stopMovement();
  }
}

void moveMotors(MotorOffsets *offsets, int leftSpeed, int rightSpeed) {
  analogWrite(MOTOR1_PWM, constrain(leftSpeed + offsets->m1Offset, 0, 255));
  analogWrite(MOTOR3_PWM, constrain(leftSpeed + offsets->m3Offset, 0, 255));
  analogWrite(MOTOR2_PWM, constrain(rightSpeed + offsets->m2Offset, 0, 255));
  analogWrite(MOTOR4_PWM, constrain(rightSpeed + offsets->m4Offset, 0, 255));
}

void stopMovement() {
  analogWrite(MOTOR1_PWM, 0);
  analogWrite(MOTOR2_PWM, 0);
  analogWrite(MOTOR3_PWM, 0);
  analogWrite(MOTOR4_PWM, 0);
}

void checkBluetooth() {
  if (SerialBT.available()) {
    char command = SerialBT.read();
    resetMovementFlags();
    switch (command) {
      case 'W':
        moveForwardFlag = true;
        targetYaw = yaw;
        break;
      case 'S':
        moveBackwardFlag = true;
        break;
      case 'A':
        moveLeftFlag = true;
        break;
      case 'D':
        moveRightFlag = true;
        break;
      case 'Q':
        rotationleftFlag = true;
        break;
      case 'E':
        rotationrightFlag = true;
        break;
      case 'R':
        targetYaw = 0;
        returnToZeroFlag = true;
        break;
      case 'X':
        stopMovement();
        resetMovementFlags();
        break;
      case '+':
        motorSpeed = min(255, motorSpeed + 10);
        break;
      case '-':
        motorSpeed = max(0, motorSpeed - 10);
        break;
      case 'O':
        digitalWrite(RELAY_PIN, HIGH);
        relayTimer = millis();
        relayAutoOffEnabled = true;
        SerialBT.println("Relay ON (auto-off in 1s)");
        break;
      case 'F':
        digitalWrite(RELAY_PIN, LOW);
        relayAutoOffEnabled = false;
        SerialBT.println("Relay FORCED OFF");
        break;
      case 'T':
        digitalWrite(RELAY_PIN, !digitalRead(RELAY_PIN));
        SerialBT.print("Relay TOGGLED to ");
        SerialBT.println(digitalRead(RELAY_PIN) ? "ON" : "OFF");
        break;
      case 'Z':  // Use Z key to trigger yaw correction
        autoCorrectYaw();
        break;
      case 'K': // Forward
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
        break;
      case 'L': // Stop
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
        break;
    }
    // Apply speeds
    ledcWrite(0, speedA); // Motor A
    ledcWrite(1, speedB); // Motor B
  }
}