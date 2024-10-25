/*******************************************************************************************
 * FileName     : SmartFactory2_Basic.ino
 * Description  : 스마트 팩토리 2 코딩 키트 (기본)
 * Author       : 박은정
 * CopyRight    : (주)한국공학기술연구원(www.ketri.re.kr)
 * Warning      : 
 * Created Date : 2024.10.24 : PEJ : 최초 작성
 ******************************************************************************************/


//==========================================================================================
// 서보 모터 사용하기
//==========================================================================================
#include <Servo.h>
Servo servo_block;
Servo servo_geer;

const int servo_block_pin = D4;                          // 서보 모터(차단대) 핀 : D4
const int servo_geer_pin = D5;                           // 서보 모터(톱니 바퀴) 핀 : D5


//==========================================================================================
// OLED 사용하기
//==========================================================================================.
#include "oled_u8g2.h"
OLED_U8G2 oled;


//==========================================================================================
// 전역 변수 선언
//==========================================================================================
const int button_push = D7;                              // 톱니바퀴 작동 버튼 핀 : D7

const int echo_pin = D8;                                 // 초음파 수신 핀: D8
const int trig_pin = D9;                                 // 초음파 송신 핀: D9

int count = 0;                                           // 지나간 드럼통 개수
int pos = 0;                                             // 컨베이어 위치 상태
String block_state = "close";                            // 차단대 상태

float distance;                                          // 거리
int pre_time = 0;                                        // 드럼통이 지나간 시간

unsigned short_previous_time = 0;
unsigned long_previous_time = 0;


//==========================================================================================
void setup()                                             // 사용자 맞춤형 설정
//==========================================================================================
{
  Serial.begin(115200);                                  // 시리얼 통신 준비

  oled.setup();                                          // OLED 셋업

  pinMode(trig_pin, OUTPUT);                             // 초음파 송신부: 출력 모드
  pinMode(echo_pin, INPUT);                              // 초음파 수신부: 입력 모드

  servo_block.attach(servo_block_pin);                   // 차단대 서보 모터 핀 설정
  servo_geer.attach(servo_geer_pin);                     // 톱니바퀴 서보 모터 핀 설정

  initializing_process();                                // 초기화
}


//==========================================================================================
void loop()                                              // 사용자 반복 처리
//==========================================================================================
{
  do_sensing_process();                                  // 센싱 처리
  do_automatic_process();                                // 자동화 처리
  et_short_periodic_process();                           // 짧은 주기 처리
  et_long_periodic_process();                            // 긴 주기 처리
}


//==========================================================================================
void initializing_process()                              // 초기화
//==========================================================================================
{
  pos = 0;
  count = 0;
  block_state = "close";

  do_geer_process();
  servo_block.write(0);

  display_information();
}


//==========================================================================================
void do_geer_process()                                   // 톱니바퀴 작동 처리
//==========================================================================================
{
  if (pos > 3) {                                         // 각도 값이 3보다 크다면
    pos = 0;                                             // 0으로 설정
  }

  int p[] = {180, 138, 102, 64};                         // 톱니바퀴 각도
  servo_geer.write(p[pos]);                              // 톱니바퀴 각도 설정
}


//==========================================================================================
void do_sensing_process()                                // 센싱 처리
//==========================================================================================
{
  if (digitalRead(button_push) == LOW) {                 // 드럼통 출고 버튼이 눌렸다면
    while (true) {
      if (digitalRead(button_push) == HIGH) break;
    }
    pos++;                                               // 각도 증가
    do_geer_process();                                   // 톱니바퀴 작동
  }

  // 초음파 송신
  digitalWrite(trig_pin, LOW);
  digitalWrite(echo_pin, LOW);
  delayMicroseconds(2);
  digitalWrite(trig_pin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig_pin, LOW);

  unsigned long duration  = pulseIn(echo_pin, HIGH);     // 초음파 수신까지의 시간 계산
  distance = duration * 17 / 1000;                       // 거리 계산

  delay(100);
}


//==========================================================================================
void do_automatic_process()                              // 자동화 처리
//==========================================================================================
{
  if(distance > 2 && distance < 8) {                     // 거리가 2cm 초과 8cm 미만일 때
    int now = millis();                                  // 현재 시간 저장
    if (now - pre_time > 500) {                          // 현재 시간과 이전 시간 비교
      pre_time = now;                                    // 드럼통이 지나간 시간 업데이트
      count++;                                           // 지나간 드럼통 개수 증가
      delay(500);

      servo_block.write(75);                             // 차단대 1초간 열기
      block_state = "open";
      delay(1000);

      servo_block.write(0);                              // 차단대 닫기
      block_state = "close";
    }
  }
}

//==========================================================================================
void et_short_periodic_process()                         // 사용자 주기적 처리 (예 : 1초마다)
//==========================================================================================
{
  unsigned long interval = 1 * 1000UL;                   // 1초마다 정보 표시
  unsigned long now = millis();

  if (now - short_previous_time < interval) {            // 1초가 지나지 않았다면
    return;
  }
  short_previous_time = now;

  display_information();                                 // 표시 처리
}


//==========================================================================================
void display_information()                               // OLED 표시
//==========================================================================================
{
  String string_count = String(count);                   // 드럼통 개수 값을 문자열로 변환
  String string_pos = String(pos);                       // 각도 값을 문자열로 변환

  oled.setLine(1, "* SmartFactory 2 *");                 // 1번째 줄에 키트명
  oled.setLine(2, "count : " + string_count);            // 2번재 줄에 개수
  oled.setLine(3, "pos : " + string_pos);                // 3번재 줄에 각도
  oled.display(3);                                       // OLED에 표시
}


//==========================================================================================
void et_long_periodic_process()                          // 사용자 주기적 처리 (예 : 5초마다)
//==========================================================================================
{
  unsigned long interval = 5 * 1000UL;                   // 5초마다 정보 표시
  unsigned long now = millis();

  if (now - long_previous_time < interval) {             // 5초가 지나지 않았다면
    return;
  }
  long_previous_time = now;

  display_serial();                                      // 시리얼 모니터 정보 표시
}


//==========================================================================================
void display_serial()                                     // 시리얼 표시
//==========================================================================================
{
  String string_count = String(count);                   // 드럼통 개수 값을 문자열로 변환
  String string_pos = String(pos);                       // 각도 값을 문자열로 변환

  Serial.println("count: " + string_count);
  Serial.println("pos: " + string_pos);
  Serial.println("----------------------");
}


//==========================================================================================
//                                                    
// (주)한국공학기술연구원 http://et.ketri.re.kr       
//                                                    
//==========================================================================================