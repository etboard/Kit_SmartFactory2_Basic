# ******************************************************************************************
# FileName     : servo_sawtooth_three_button
# Description  : 3개의 버튼으로 톱니 바퀴 제억하기
# Author       : 손철수
# Created Date : 2023.11.02
# Reference    :
# Modified     : 
# ******************************************************************************************


import time
from machine import Pin
from ETboard.lib.pin_define import *
from ETboard.lib.servo import Servo


# global variable
servo = Servo(Pin(D6))                         # 서보모터 핀 지정
HOME = Pin(D7)                                 # 홈   : 파랑 버튼 핀 지정
PUSH = Pin(D9)                                 # 밀기 : 노랑 버튼 핀 지정
FRONT = Pin(D8)                                # 맨앞 : 초록 버튼 핀 지정
pos = 0


# setup
def setup():
    HOME.init(Pin.IN)                          # 홈 버튼 입력모드 설정
    PUSH.init(Pin.IN)                          # 밀기 버튼 입력모드 설정
    FRONT.init(Pin.IN)                         # 맨앞 버튼 입력모드 설정


# mainloop
def loop():
    global pos
    
    HOME_state = HOME.value()                  # 
    PUSH_state = PUSH.value()
    FRONT_state = FRONT.value()                # 
    
    if HOME_state == LOW:                      #
        pos = 0
        servo.write_angle(180)
        time.sleep(0.3)    
            
    if FRONT_state == LOW:                     #
        pos = 3
        servo.write_angle(36)
        time.sleep(0.3)
        
    if PUSH_state == LOW:                      #
        pos = pos + 1
        if (pos > 3):
            return
        servo.write_angle(180-(48*pos))
        time.sleep(0.3)        


if __name__ == "__main__":
    setup()
    while True:
        loop()


# ==========================================================================================
#
#  (주)한국공학기술연구원 http://et.ketri.re.kr
#
# ==========================================================================================
 