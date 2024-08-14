# ******************************************************************************************
# FileName     : servo_lego_rack_pinion_three_button.py
# Description  : 파랑, 초록 버튼을 눌러 서보모터 움직여 보기
# Author       : 이승찬
# Created Date : 2021.08.20
# Reference    :
# Modified     : 2022.02.08 : SJI   : 헤더 수정, 주석 수정, 소스 크린징
# Modified     : 2024.08.14 : 손철수 : 노랑 버튼 추가
# ******************************************************************************************


# import
import time
from machine import Pin
from ETboard.lib.pin_define import *
from ETboard.lib.servo import Servo


# global variable
servo = Servo(Pin(D6))                         # 서보모터 핀 지정
Up = Pin(D7)                                   # 파랑 버튼 핀 지정
Down = Pin(D8)                                 # 초록 버튼 핀 지정
Mid = Pin(D9)                                  # 노랑 버튼 핀 지정


# setup
def setup():
    Up.init(Pin.IN)                            # 파랑 버튼 입력모드 설정
    Down.init(Pin.IN)                          # 초록 버튼 입력모드 설정
     Mid.init(Pin.IN)                          # 노랑 버튼 입력모드 설정


# mainloop
def loop():
    Up_state = Up.value()                      # 파랑 버튼값 가져오기
    Down_state = Down.value()                  # 초록 버튼값 가져오기
    Mid_state = Mid.value()                    # 노랑 버튼값 가져오기
    
    if Up_state == LOW:                        # 파랑 버튼이 눌리면 서보모터 150도 까지 회전
        servo.write_angle(150)
        time.sleep(0.3)

    if Mid_state == LOW:                       # 노랑 버튼이 눌리면 서보모터 105도 까지 회전
        servo.write_angle(105)
        time.sleep(0.3)
        
    if Down_state == LOW:                      # 초록 버튼이 눌리면 서보모터 60도 까지 회전
        servo.write_angle(60)
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
