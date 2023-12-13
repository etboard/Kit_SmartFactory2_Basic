/******************************************************************************************************
 * FileName     : SmartFactory_Basic
 * Description  : 스마트 팩토리 코딩 키트 (기본)
 * Author       : 위대원
 * CopyRight    : (주)한국공학기술연구원(www.ketri.re.kr)
 * Warning      : Arduino IDE에서 u8g2 라이브러리를 추가해서 컴파일 해야함
 * Created Date : 2021.09.14 : WDW : 최초 작성
 * Modified     : 2022.01.12 : SCS : 소스 크린징
 * Modified     : 2022.10.03 : SCS : support arduino uno with ET-Upboard
 * Modified     : 2022.11.23 : YSY : 소스 크린징, distance값 수정, distance 범위 지정, delay 수정
 * Modified     : 2022.12.19 : YSY : reset_pin_PIN -> reset_pin, 주석
 * Modified     : 2022.12.21 : YSY : 변수 명명법 통일
 * Modified     : 2022.12.21 : YSY : 2<distance<8
 ******************************************************************************************************/

// OLED 제어를 위한 라이브러리 불러오기
#include "oled_u8g2.h"
OLED_U8G2 oled;

//-------------------------------------------------------------------------------------------------------
// ETBoard 핀번호 설정
//-------------------------------------------------------------------------------------------------------
#include "pins_arduino.h"                       // support arduino uno with ET-Upboard

int reset_pin = D6;                             // 카운트 리셋핀 (D6 = 빨강 버튼)

int echo_pin  = D8;                             // 초음파 센서 수신부
int trig_pin  = D9;                             // 초음파 센서 송신부

int count = 0;                                  // 카운터용 변수
int pre_time = 0;                               // 이전에 물건이 지나간 시간


//=======================================================================================================
void setup()
//=======================================================================================================
{
    Serial.begin(115200);                       // 시리얼 통신 준비
    oled.setup();                               // OLED 셋업

    pinMode(reset_pin, INPUT);                  // 리셋버튼 입력 모드 설정

    pinMode(trig_pin, OUTPUT);                  // 초음파 센서 송신부 출력 모드 설정
    pinMode(echo_pin, INPUT);                   // 초음파 센서 수신부 입력 모드 설정
}


//=======================================================================================================
void loop()
//=======================================================================================================
{
    //---------------------------------------------------------------------------------------------------
    // 물체가 초음파 센서를 지나면 카운트 하기
    //---------------------------------------------------------------------------------------------------
    long duration, distance;
    digitalWrite(trig_pin, LOW);                // 초음파 센서 거리 센싱 시작
    delayMicroseconds(2);
    digitalWrite(trig_pin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trig_pin, LOW);                // 초음파 센서 거리 센싱 종료

    duration = pulseIn (echo_pin, HIGH);        // 물체에 반사되어 돌아온 초음파의 시간을 저장
    distance = ((34 * duration) / 1000) / 2;    // 측정된 값을 cm로 변환하는 공식
    //Serial.print("distance : ");
    Serial.print(distance);
    Serial.print("->");
    //Serial.println("cm");

    if(distance > 1 && distance < 8)            // 물체와의 거리가 2cm 초과 10cm 미만이면 
    {
        int now_time = millis();
        if(now_time - pre_time > 500)           // 중복 카운트를 방지하기 위해 0.5초 초과인 경우만 
        {
            count += 1;                         // 한번 카운트
            pre_time = now_time;                // 이전 시각에 현재 시각 저장
            delay(500);
        }
    }

    //---------------------------------------------------------------------------------------------------  
    // 리셋 버튼을 누르면 카운트 초기화 하기
    //---------------------------------------------------------------------------------------------------         
    if(digitalRead(reset_pin) == LOW)           // 리셋 버튼을 누르면
    {
        Serial.println("count reset");                
        count = 0;                              // 카운트 초기화
    }
  
    //Serial.print("count : ");             
    Serial.println(count);
    //Serial.println("---------------------");

    //---------------------------------------------------------------------------------------------------
    // OLED 텍스트 표시
    //---------------------------------------------------------------------------------------------------
    char text1[32] = "count : ";                // text1 count 값 표시
    char value1[32];
    String str1 = String(count, DEC);
    str1.toCharArray(value1, 6);
    strcat(text1, value1);
  
    oled.setLine(1, "*Smart Factory");          // OLED 첫 번째 줄 : 시스템 이름
    oled.setLine(2, text1);                     // OLED 두 번째 줄 : count 값
    oled.setLine(3, "---------------------");   // OLED 세 번째 줄 
    oled.display();
    
    delay(100);  
}

//=======================================================================================================
//
// (주)한국공학기술연구원 http://et.ketri.re.kr
//
//=======================================================================================================