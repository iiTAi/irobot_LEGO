from spike import PrimeHub, ColorSensor, Motor
from spike.control import wait_for_seconds, Timer
from math import *

class MotorAndSensor:
    def __init__(self, sensor, motor=''):
        self.sensor = ColorSensor(sensor)
        if motor != '':
            self.motor = Motor(motor)
        self.ref = 0
        self.ref_center = 0
        self.error_prev = 0
        self.speed = 0.0
        self.BASE_SPEED = 22

    def calc_speed(self, option='+'):
        Kp = 0.24
        Kd = 0.10
        T = 0.050
        target = 50

        error = self.ref - target
        error_diff = (error - self.error_prev) / T

        weight = 1 + self.ref_center / 20
        proportional = Kp * error * weight
        derivative = Kd * error_diff
        self.speed = int(proportional + derivative + self.BASE_SPEED)
        if option == '-':
            self.speed = -self.speed

        self.error_prev = error

    def get_color(self):
        if self.ref < 50:
            return 'black'
        else:
            return 'white'
        
    def update_speed(self):
        self.motor.start(self.speed)

    def update_sensor(self):
        self.ref = self.sensor.get_reflected_light()

    def update_ref_center(self, ref_c):
        self.ref_center = ref_c

class TimeChecker:
    def __init__(self):
        self.timer = Timer()
        self.prev = 0
        self.now = 0
        self.stop_counter = 0
        self.STOP_LIMIT = 7

    def update(self):
        self.prev = self.now
        self.now = self.timer.now()

    def check_progress(self):
        return self.now > self.prev
    
    def check_stop(self, color1, color2):
        if self.check_progress():
            if color1 == 'black' and color2 == 'black':
                self.stop_counter += 1
            else:
                self.stop_counter = 0

        return self.stop_counter > self.STOP_LIMIT



#========================================
# setup
hub = PrimeHub()

left = MotorAndSensor('A', 'C')
right = MotorAndSensor('B', 'D')
center = MotorAndSensor('F')

hub.speaker.beep(note=60, seconds=1.0)

tc = TimeChecker()

#========================================
# main loop
while True:
    tc.update() # タイマの更新

    # センサの値の更新
    left.update_sensor()
    right.update_sensor()
    center.update_sensor()

    # 中央センサの値の更新
    left.update_ref_center(center.ref)
    right.update_ref_center(center.ref)

    # 停止確認
    if tc.check_stop(left.get_color(), right.get_color()):
        break

    # モータの速度の計算
    left.calc_speed('-')
    right.calc_speed('+')

    # モータの速度の更新
    left.update_speed()
    right.update_speed()

#========================================
# 停止処理
left.motor.stop()
right.motor.stop()

# メロディの再生
hub.speaker.beep(65, 0.2)#ファ
hub.speaker.beep(67, 0.2)#ソ
hub.speaker.beep(69, 0.2)#ラ
hub.speaker.beep(70, 0.2)#シ♭
hub.speaker.beep(72, 0.2)#ド^
wait_for_seconds(0.2)
hub.speaker.beep(69, 0.2)#ラ
hub.speaker.beep(65, 0.2)#ファ
wait_for_seconds(0.2)#200ms待つ
hub.speaker.beep(72, 0.2)#ド^
wait_for_seconds(0.2)#200ms待つ
hub.speaker.beep(70, 0.4)#シ♭
hub.speaker.beep(67, 0.6)#ソ
wait_for_seconds(0.8)#1200ms待つ
hub.speaker.beep(70, 0.2)#シ♭
wait_for_seconds(0.2)
hub.speaker.beep(67, 0.2)#ソ
hub.speaker.beep(64, 0.2)#ミ
wait_for_seconds(0.2)#200ms待つ
hub.speaker.beep(70, 0.2)#シ♭
wait_for_seconds(0.2)#200ms待つ
hub.speaker.beep(69, 0.4)#ラ
hub.speaker.beep(65, 0.6)#ファ
wait_for_seconds(0.8)#1200ms待つ
hub.speaker.beep(62, 0.4)#レ
hub.speaker.beep(74, 0.4)#レ^
hub.speaker.beep(72, 0.2)#ド
hub.speaker.beep(70, 0.2)#シ♭
hub.speaker.beep(69, 0.2)#ラ
hub.speaker.beep(70, 0.2)#シ♭
hub.speaker.beep(72, 0.6)#ド^
hub.speaker.beep(65, 0.2)#ファ
hub.speaker.beep(65, 0.4)#ファ
wait_for_seconds(0.2)#200ms待つ
hub.speaker.beep(69, 0.2)#ラ
hub.speaker.beep(70, 0.2)#シ♭
hub.speaker.beep(69, 0.2)#ラ
hub.speaker.beep(65, 0.2)#ファ
hub.speaker.beep(70, 0.2)#シ♭
hub.speaker.beep(69, 0.2)#ラ
hub.speaker.beep(65, 0.2)#ファ
hub.speaker.beep(74, 0.2)#レ^
hub.speaker.beep(72, 1.8)#ド^
wait_for_seconds(0.4)#400ms待つ
hub.speaker.beep(60, 0.2)#ド
hub.speaker.beep(60, 0.2)#ド
hub.speaker.beep(70, 0.2)#シ♭
hub.speaker.beep(69, 0.2)#ラ
hub.speaker.beep(67, 0.2)#ソ
hub.speaker.beep(69, 0.2)#ラ
hub.speaker.beep(65, 1.2)#ファ