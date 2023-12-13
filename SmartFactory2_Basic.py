# ******************************************************************************************************
# FileName     : SmartFactory2_Basic
# Description  : 스마트 팩토리2 코딩 키트 (기본)
# Author       : 손철수
# CopyRight    : (주)한국공학기술연구원(www.ketri.re.kr)
# Created Date : 2023.11.02
# Reference    :
# Modified     : ????.??.?? : ??? : ????
# ******************************************************************************************************

# import
import time                                        # 시간 관련 모듈
from machine import Pin, time_pulse_us             # 핀 및 시간 관련 모듈
from ETboard.lib.pin_define import *               # ETboard 핀 관련 모듈
from ETboard.lib.OLED_U8G2 import *                # ETboard OLED 관련 모듈
from ETboard.lib.servo import Servo

#-------------------------------------------------------------------------------------------------------
# ETBoard 핀번호 설정
#-------------------------------------------------------------------------------------------------------
# global variable
oled = oled_u8g2()                                 

echo_pin = Pin(D8)                                 # 초음파 센서 수신부
trig_pin = Pin(D9)                                 # 초음파 센서 송신부

count = 0                                          # 카운터용 변수
pre_time = 0                                       # 이전에 물건이 지나간 시간

servo = Servo(Pin(D6))                             # 서보모터 핀 지정
PUSH = Pin(D7)                                     # 밀기 버튼 : 파랑 버튼 핀 지정

pos = 0                                            # 컨베이어 막대 위치


#=======================================================================================================
# setup
#=======================================================================================================
def setup():   
    trig_pin.init(Pin.OUT)                         # 초음파 센서 송신부 출력 모드 설정
    echo_pin.init(Pin.IN)                          # 초음파 센서 수신부 입력 모드 설정
    PUSH.init(Pin.IN)                              # 밀기 버튼 입력모드 설정


#=======================================================================================================
# main loop
#=======================================================================================================
def loop():
    #---------------------------------------------------------------------------------------------------
    # 물체가 초음파 센서를 지나면 카운트 하기
    #---------------------------------------------------------------------------------------------------
    global pre_time, count
    global pos
    
    trig_pin.value(LOW)                            # 초음파 센서 거리 센싱 시작
    echo_pin.value(LOW)
    time.sleep_ms(2)
    trig_pin.value(HIGH)
    time.sleep_ms(10)
    trig_pin.value(LOW)                            # 초음파 센서 거리 센싱 종료

    duration = time_pulse_us(echo_pin, HIGH)       # 물체에 반사되어 돌아온 초음파의 시간을 저장
    distance  = ((34 * duration) / 1000) / 2       # 측정된 값을 cm로 변환하는 공식 
    print("distance : ", distance, "cm")
    
    time.sleep(0.07)

    if( distance >= 1 and distance <= 8 ) :        # 물체와의 거리가 1이상 8cm 이하이면
        now_time = int(round(time.time() * 1000))  #   필요시 거리를 수정하세요
        if(now_time - pre_time > 500) :            # 중복 카운트를 방지하기 위해 0.5초 초과인 경우만
            count += 1                             # 한 번 카운트
            pre_time = now_time;                   # 이전 시각에 현재 시각 저장
            time.sleep(0.5)
    print("count    : ", count)               

    PUSH_state = PUSH.value()
    if PUSH_state == LOW:   
        pos = pos + 1
        if (pos > 3):
            pos = 0
        servo.write_angle(180-(49*pos))
        time.sleep(0.05)
    print("pos      : ", pos)
    print("---------------------")
    
    #---------------------------------------------------------------------------------------------------
    # OLED 텍스트 표시
    #---------------------------------------------------------------------------------------------------
    text1 = "count: %d" %(count)                   # count 표시글
    text2 = "pos  : %d" %(pos)                     # position 표시글
    
    oled.clear()
    oled.setLine(1, "* Smart Factory *")           # OLED 첫 번째 줄 : 시스템 이름
    oled.setLine(2, text1)                         # OLED 두 번째 줄 : count
    oled.setLine(3, text2)                         # OLED 세 번째 줄 : position
    oled.display()    


if __name__ == "__main__":
    setup()
    while True:
        loop()

#=======================================================================================================
#
#  (주)한국공학기술연구원 http://et.ketri.re.kr
#
#======================================================================================================= 