#include <SoftwareSerial.h>

SoftwareSerial bluetooth(0,1); // RX, TX (핀 0, 1 사용)

int motorA = 10;
int motorB = 11;

int motorA_PWM = 12;
int motorB_PWM = 13;

int speed = 0;

void setup() {
  pinMode(motorA_PWM, OUTPUT);      // 출력핀 설정
  pinMode(motorB_PWM, OUTPUT);

  bluetooth.begin(9600); // 블루투스 통신 속도
  Serial.begin(9600); // 시리얼 모니터 통신 속도
}

void loop() {
  if (bluetooth.available()) {
    Serial.write(bluetooth.read());
  }
  if (Serial.available()) {
    bluetooth.write(Serial.read());
  }

  if (bluetooth.available()) {
    char data = bluetooth.read();
    Serial.println(data);
    if (data == 'H'){
      speed = 250;
      Serial.println("speed: HIGH");
    }
    else if(data == 'N'){
      speed = 150;
      Serial.println("speed: NORMAL");
    }
    else if(data == 'L'){
      speed = 100;
      Serial.println("speed: LOW");
    }
    else if (data == 'B') {  // 후진
      digitalWrite(motorA_PWM, HIGH);
      digitalWrite(motorB_PWM, HIGH);
      analogWrite(motorA,speed);
      analogWrite(motorB,speed);
      Serial.println("BackWard");
    } 
    else if (data == 'F') {   // 전진
      digitalWrite(motorA_PWM, LOW);
      digitalWrite(motorB_PWM, LOW);
      analogWrite(motorA,speed);
      analogWrite(motorB,speed);
      Serial.println("Forward");
    } 
    else if (data == 'S') {   //정지
      digitalWrite(motorA_PWM, HIGH);
      digitalWrite(motorB_PWM, HIGH);
      analogWrite(motorA,0);
      analogWrite(motorB,0);
      Serial.println("Stop");
    }
    else if (data == 'R') {   //시계방향 회전
      digitalWrite(motorA_PWM, HIGH);
      digitalWrite(motorB_PWM, LOW);
      analogWrite(motorA,speed);
      analogWrite(motorB,speed);
      Serial.println("Clock wise");
    }
    else if (data == 'C') {   //반시계방향 회전
      digitalWrite(motorA_PWM, LOW);
      digitalWrite(motorB_PWM, HIGH);
      analogWrite(motorA,speed);
      analogWrite(motorB,speed);
      Serial.println("Counter Clock wise");
    }

  }
  
  

}
