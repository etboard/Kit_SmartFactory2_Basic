# ******************************************************************************************
# FileName     : 03._servo_motor_up_down
# Description  : 파랑, 초록 버튼을 눌러 서보모터 움직여 보기
# Author       : 이승찬
# Created Date : 2021.08.20
# Reference    :
# Modified     : 2022.02.08 : SJI : 헤더 수정, 주석 수정, 소스 크린징 
# ******************************************************************************************


import time
from machine import Pin
from ETboard.lib.pin_define import *
from ETboard.lib.servo import Servo


# global variable
servo = Servo(Pin(D6))                         # 서보모터 핀 지정
PUSH = Pin(D7)                                 # 밀기 버튼 : 파랑 버튼 핀 지정
pos = 0


# setup
def setup():    
    PUSH.init(Pin.IN)                          # 밀기 버튼 입력모드 설정


# mainloop
def loop():
    global pos
    
    PUSH_state = PUSH.value()
    if PUSH_state == LOW:                      #
        pos = pos + 1
        if (pos > 3):
            pos = 0
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
