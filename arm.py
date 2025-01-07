from machine import Pin, PWM, UART
import time

# mg996
lower_pin = Pin(15)
pwm_lower = PWM(lower_pin)
pwm_lower.freq(50)

middle_pin = Pin(16)
pwm_middle = PWM(middle_pin)
pwm_middle.freq(50)
# 그리퍼(sg90)
grip_pin = Pin(14)
pwm_grip = PWM(grip_pin)
pwm_grip.freq(50)

grip2_pin = Pin(13)
pwm_grip2 = PWM(grip2_pin)
pwm_grip2.freq(50)

grip3_pin = Pin(12)
pwm_grip3 = PWM(grip3_pin)
pwm_grip3.freq(50)


# 블루투스 모듈 HC-06의 UART 설정
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))


# mg996 각도를 설정하는 함수
def set_lower_angle(angle):
    min_pulse = 1000  # 최소 펄스 폭 (1ms)
    max_pulse = 2000  # 최대 펄스 폭 (2ms)
    pulse = min_pulse + (angle / 180) * (max_pulse - min_pulse)
    duty = int((pulse / 20000) * 65535)
    pwm_lower.duty_u16(duty)
    
def set_middle_angle(angle):
    min_pulse = 1000  # 최소 펄스 폭 (1ms)
    max_pulse = 2000  # 최대 펄스 폭 (2ms)
    pulse = min_pulse + (angle / 180) * (max_pulse - min_pulse)
    duty = int((pulse / 20000) * 65535)
    pwm_middle.duty_u16(duty)
    
# sg90 각도를 설정하는 함수
def set_grip_angle(angle):
    min_pulse = 500  # SG90 최소 펄스 폭 (0.5ms)
    max_pulse = 2500  # SG90 최대 펄스 폭 (2.5ms)
    pulse = min_pulse + (angle / 180) * (max_pulse - min_pulse)
    duty = int((pulse / 20000) * 65535)
    pwm_grip.duty_u16(duty)
def set_grip2_angle(angle):
    min_pulse = 500  # SG90 최소 펄스 폭 (0.5ms)
    max_pulse = 2500  # SG90 최대 펄스 폭 (2.5ms)
    pulse = min_pulse + (angle / 180) * (max_pulse - min_pulse)
    duty = int((pulse / 20000) * 65535)
    pwm_grip2.duty_u16(duty)

def set_grip3_angle(angle):
    min_pulse = 500  # SG90 최소 펄스 폭 (0.5ms)
    max_pulse = 2500  # SG90 최대 펄스 폭 (2.5ms)
    pulse = min_pulse + (angle / 180) * (max_pulse - min_pulse)
    duty = int((pulse / 20000) * 65535)
    pwm_grip3.duty_u16(duty)
    
    
def move_grip_smooth(pre_angle, to_angle, steps=50, step_delay=0.01):
    if pre_angle is None or to_angle is None:
        raise ValueError("pre_angle and to_angle must be valid numbers")
    
    step_size = (to_angle - pre_angle) / steps
    for step in range(steps):
        pre_angle += step_size
        set_grip_angle(pre_angle)
        time.sleep(step_delay)
    set_grip_angle(to_angle)  # 최종 각도 설정
    return to_angle

def move_grip2_smooth(pre_angle, to_angle, steps=50, step_delay=0.01):
    if pre_angle is None or to_angle is None:
        raise ValueError("pre_angle and to_angle must be valid numbers")
    
    step_size = (to_angle - pre_angle) / steps
    for step in range(steps):
        pre_angle += step_size
        set_grip2_angle(pre_angle)
        time.sleep(step_delay)
    set_grip2_angle(to_angle)  # 최종 각도 설정
    return to_angle

def move_grip3_smooth(pre_angle, to_angle, steps=50, step_delay=0.01):
    if pre_angle is None or to_angle is None:
        raise ValueError("pre_angle and to_angle must be valid numbers")
    
    step_size = (to_angle - pre_angle) / steps
    for step in range(steps):
        pre_angle += step_size
        set_grip3_angle(pre_angle)
        time.sleep(step_delay)
    set_grip3_angle(to_angle)  # 최종 각도 설정
    return to_angle


# 각도를 점진적으로 변경하는 함수
def move_lower_smooth(pre_angle, to_angle, steps=50, step_delay=0.01):
    # 각도가 None이 아닌지 확인
    if pre_angle is None or to_angle is None:
        raise ValueError("pre_angle and to_angle must be valid numbers")
    
    step_size = (to_angle - pre_angle) / steps
    for step in range(steps):
        pre_angle += step_size
        set_lower_angle(pre_angle)
        time.sleep(step_delay)
    set_lower_angle(to_angle)  # 최종 각도 설정
    return to_angle

def move_middle_smooth(pre_angle, to_angle, steps=50, step_delay=0.01):
    # 각도가 None이 아닌지 확인
    if pre_angle is None or to_angle is None:
        raise ValueError("pre_angle and to_angle must be valid numbers")
    
    step_size = (to_angle - pre_angle) / steps
    for step in range(steps):
        pre_angle += step_size
        set_middle_angle(pre_angle)
        time.sleep(step_delay)
    set_middle_angle(to_angle)  # 최종 각도 설정
    return to_angle

#초기 상태 각도 설정
current_lower_angle = 120
current_middle_angle = 200
current_grip_angle = 90 #그리퍼 open:90 close: 20
current_grip2_angle = 100 
current_grip3_angle = 120 #앞: 120 왼쪽: 180 오른쪽 :60

set_lower_angle(120)
set_middle_angle(200)
set_grip_angle(90)
set_grip2_angle(100)
set_grip3_angle(120)

try:
    while True:
        if uart.any():
            # 블루투스 모듈로부터 데이터 수신
            data = uart.readline().decode('utf-8').strip()
            print("Received:", data)  # 디버깅용으로 수신된 데이터 출력
            if data == 'G':
                current_lower_angle = move_lower_smooth(current_lower_angle, 60)
                time.sleep(1)
                current_middle_angle = move_middle_smooth(current_middle_angle, 220)
                time.sleep(1)
                current_grip2_angle = move_grip2_smooth(current_grip2_angle, 80)
                time.sleep(1)
                current_grip_angle = move_grip_smooth(current_grip_angle, 20)
                time.sleep(1)
                current_lower_angle = move_lower_smooth(current_lower_angle, 120)
                time.sleep(1)
                current_middle_angle = move_middle_smooth(current_middle_angle, 200)
                time.sleep(1)
                current_grip2_angle = move_grip2_smooth(current_grip2_angle, 100)
                time.sleep(1)
                current_grip_angle = move_grip_smooth(current_grip_angle, 90)
                time.sleep(1)
                print("Lower angle moved to 60")
                
            elif data == 'E':
                current_lower_angle = move_lower_smooth(current_lower_angle, 120)
                time.sleep(0.5)
                current_middle_angle = move_middle_smooth(current_middle_angle, 200)
                time.sleep(0.5)
                current_grip2_angle = move_grip2_smooth(current_grip2_angle, 100)
                time.sleep(0.5)
                current_grip_angle = move_grip_smooth(current_grip_angle, 90)
                time.sleep(0.5)
                current_grip3_angle = move_grip3_smooth(current_grip3_angle, 120)
                
            #elif data == 'Y':
                
            #elif data == 'U':
                
    # 숙이고 집고 올라오고 벌리고 
#    current_lower_angle = move_lower_smooth(current_lower_angle, 60)
#    time.sleep(1)
#    current_middle_angle = move_middle_smooth(current_middle_angle, 220)
#    time.sleep(1)
#    current_grip2_angle = move_grip2_smooth(current_grip2_angle, 80)
#    time.sleep(1)
#    current_grip_angle = move_grip_smooth(current_grip_angle, 20)
#    time.sleep(1)
#    current_lower_angle = move_lower_smooth(current_lower_angle, 120)
#    time.sleep(1)
#    current_middle_angle = move_middle_smooth(current_middle_angle, 200)
#    time.sleep(1)
#    current_grip2_angle = move_grip2_smooth(current_grip2_angle, 100)
#    time.sleep(1)
#    current_grip_angle = move_grip_smooth(current_grip_angle, 90)
#    time.sleep(1)

    
    
    
    #current_grip_angle = move_grip_smooth(current_grip_angle, 20)
    
    #current_grip2_angle = move_grip2_smooth(current_grip2_angle, 100)
    
    
except KeyboardInterrupt:
    pwm_lower.deinit()  # 프로그램 종료 시 PWM 비활성화
    pwm_middle.deinit()  # 프로그램 종료 시 PWM 비활성화
    pwm_grip.deinit()
    pwm_grip2.deinit()
    pwm_grip3.deinit()
except ValueError as e:
    print(e)
    pwm_lower.deinit()  # 프로그램 종료 시 PWM 비활성화
    pwm_middle.deinit()  # 프로그램 종료 시 PWM 비활성화
    pwm_grip.deinit()
    pwm_grip2.deinit()
    pwm_grip3.deinit()


