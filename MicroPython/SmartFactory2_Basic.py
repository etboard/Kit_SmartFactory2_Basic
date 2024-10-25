# ******************************************************************************************
# FileName     : SmartFactory2_Basic
# Description  : 스마트 팩토리 2 코딩 키트 (기본)
# Author       : 손철수
# CopyRight    : (주)한국공학기술연구원(www.ketri.re.kr)
# Created Date : 2023.11.02
# Reference    :
# Modified     : 2024.10.24 : PEJ : 구조 변경, 최신화
# ******************************************************************************************


#===========================================================================================
# 기본 모듈 사용하기
#===========================================================================================
import time
import math
from machine import Pin, time_pulse_us
from ETboard.lib.pin_define import *
from ETboard.lib.servo import Servo


#===========================================================================================
# OLED 표시 장치 사용하기
#===========================================================================================
from ETboard.lib.OLED_U8G2 import *
oled = oled_u8g2()


#===========================================================================================
# 전역 변수 선언
#===========================================================================================
button_push = Pin(D7)                                    # 톱니바퀴 작동 버튼 핀 : D7

echo_pin = Pin(D8)                                       # 초음파 수신 핀: D8
trig_pin = Pin(D9)                                       # 초음파 송신 핀: D9

pump_state = 0                                           # 워터 펌프 상태: 멈춤

servo_block = Servo(Pin(D4))                             # 서보모터(차단대) 핀 : D4
servo_geer = Servo(Pin(D5))                              # 서보모터(차단대) 핀 : D5

count = 0                                                # 지나간 드럼통 개수
pre_time = 0                                             # 드럼통이 지나간 시간

distance = 0                                             # 거리
pos = 0                                                  # 컨베이어 위치 상태
block_state = 'close'                                    # 차단대 상태

short_previous_time = 0
long_previous_time = 0


#===========================================================================================
def setup():                                             #  사용자 맞춤형 설정
#===========================================================================================
    button_push.init(Pin.IN)                             # 밀기 버튼 : 입력 모드

    echo_pin.init(Pin.IN)                                # 초음파 수신부: 입력 모드
    trig_pin.init(Pin.OUT)                               # 초음파 송신부: 출력 모드

    initializing_process()                               # 초기화


#===========================================================================================
def loop():                                              # 사용자 반복 처리
#===========================================================================================
    do_sensing_process()                                 # 센싱 처리
    do_automatic_process()                               # 자동화 처리
    et_short_periodic_process()                          # 짧은 주기 처리
    et_long_periodic_process()                           # 긴 주기 처리


#===========================================================================================
def initializing_process():                              # 초기화
#===========================================================================================
    global count, pos, block_state

    count = 0
    pos = 0
    block_state = 'close'

    do_geer_process()
    servo_block.write_angle(0)

    display_information()


#===========================================================================================
def do_geer_process():                                   # 톱니바퀴 작동 처리
#===========================================================================================
    global pos

    if pos > 3:                                          # 각도 값이 3보다 크다면
        pos = 0                                          # 0으로 설정

    p = [180, 138, 102, 64]                              # 톱니바퀴 각도
    servo_geer.write_angle(p[pos])                       # 톱니바퀴 각도 설정


#===========================================================================================
def do_sensing_process():                                # 센싱 처리
#===========================================================================================
    global pos, distance

    if button_push.value() == LOW:                       # 드럼통 출고 버튼이 눌렸다면
        while True:
            if button_push.value() == HIGH:
                break
        pos += 1                                         # 각도 증가
        do_geer_process()                                # 톱니바퀴 작동

    # 초음파 송신
    trig_pin.value(LOW)
    echo_pin.value(LOW)
    time.sleep_ms(2)
    trig_pin.value(HIGH)
    time.sleep_ms(10)
    trig_pin.value(LOW)

    duration = time_pulse_us(echo_pin, HIGH)             # 초음파 수신까지의 시간 계산
    distance = 17 * duration / 1000                      # 거리 계산

    time.sleep(0.1)


#===========================================================================================
def do_automatic_process():                              # 자동화 처리
#===========================================================================================
    global distance, count, block_state, pre_time

    if distance > 2 and distance < 8:                    # 측정된 거리가 2 초과 8 미만이라면
        now = int(round(time.time() * 1000))             # 현재 시간 저장
        if now - pre_time > 500:                         # 중복 카운트 방지
            pre_time = now
            count += 1                                   # 드럼통 출고 개수 증가
            time.sleep(0.5)

            servo_block.write_angle(75)                  # 차단대 열기
            block_state = 'open'
            time.sleep(1)

            servo_block.write_angle(0)                   # 차단대 닫기
            block_state = 'close'


#===========================================================================================
def et_short_periodic_process():                         # 사용자 주기적 처리 (예 : 1초마다)
#===========================================================================================
    global short_previous_time

    interval = 1                                         # 1초마다 정보 표시
    now = int(round(time.time()))

    if now - short_previous_time < interval:             # 1초가 지나지 않았다면
        return

    short_previous_time = now
    display_information()                                # 표시 처리


#===========================================================================================
def display_information():                               # OLED 표시
#===========================================================================================
    global count, pos

    string_count = "%d" % count                          # 드럼통 개수 값을 문자열로 변환
    string_pos = "%d" % pos                              # 각도 값을 문자열로 변환

    oled.clear()
    oled.setLine(1, '* SmartFactory2 *')                 # 1번째 줄에 키트명
    oled.setLine(2, 'count: ' + string_count)            # 2번재 줄에 개수
    oled.setLine(3, 'pos: ' + string_pos)                # 3번재 줄에 각도
    oled.display()                                       # OLED에 표시


#===========================================================================================
def et_long_periodic_process():                          # 사용자 주기적 처리 (예 : 5초마다)
#===========================================================================================
    global now, long_previous_time

    interval = 5                                         # 5초마다 정보 표시
    now = int(round(time.time()))

    if now - long_previous_time < interval:              # 5초가 지나지 않았다면
        return

    long_previous_time = now
    display_shell()                                      # 쉘에 정보 표시


#===========================================================================================
def display_shell():                                     # 쉘 표시
#===========================================================================================
    global count, pos

    string_count = "%d" % count                          # 드럼통 개수 값을 문자열로 변환
    string_pos = "%d" % pos                              # 각도 값을 문자열로 변환

    print('count: ' + string_count)
    print('pos: ' + string_pos)
    print('----------------------')


#===========================================================================================
# 시작 지점                     
#===========================================================================================
if __name__ == "__main__":
    setup()
    while True:
        loop()


#===========================================================================================
#                                                    
# (주)한국공학기술연구원 http://et.ketri.re.kr       
#
#===========================================================================================
