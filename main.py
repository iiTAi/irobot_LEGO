from spike import PrimeHub, ColorSensor, Motor
from spike.control import wait_for_seconds, Timer
from math import *

class MotorAndSensor:
    """ モータとセンサを制御するクラス """

    def __init__(self, sensor, motor=''):
        """ インスタンスの初期化

        Members:
            sensor (ColorSensor): カラーセンサのインスタンス
            motor (str, optional): モータのインスタンス Defaults to ''.
            ref (int): センサの反射率
            ref_center (int): 中央センサの反射率
            error_prev (int): 反射率の目標値との差分の前回値
            speed (int): モータの速度
            BASE_SPEED (int): モータの基本速度
        """
        self.sensor = ColorSensor(sensor)
        if motor != '':
            self.motor = Motor(motor)
        self.ref = 0
        self.ref_center = 0
        self.error_prev = 0
        self.speed = 0
        self.BASE_SPEED = 25

    def calc_speed(self, option='+'):
        """ モータの速度計算

        比例利得Kp, 微分利得Kdを用いてモータの速度を計算する
        Kp, Kd, サンプリング周期T, 目標値targetは試行を重ねて調整済
        重みweightは中央センサの値による重み付けで, 比例利得に掛けられる

        Args:
            option (str, optional): 回転方向 Defaults to '+'.
        """
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
        """ 反射率に応じた白黒判定

        Returns:
            string: 反射率が50未満なら'black', それ以外は'white'を返す
        """
        if self.ref < 50:
            return 'black'
        else:
            return 'white'
        
    def update_speed(self):
        """ モータの速度更新 """
        self.motor.start(self.speed)

    def update_sensor(self):
        """ センサの値の更新 """
        self.ref = self.sensor.get_reflected_light()

    def update_ref_center(self, ref_c):
        """ 中央センサの値の更新

        Args:
            ref_c (int): 中央センサの反射率
        """
        self.ref_center = ref_c

class TimeChecker:
    """ タイマを制御するクラス """
    def __init__(self):
        """_summary_

        Members:
            timer (Timer): タイマのインスタンス
            prev (int): 前回のタイマの値(秒)
            now (int): 現在のタイマの値(秒)
            stop_counter (int): 停止用カウンタ
            STOP_LIMIT (int): 停止判定の閾値
        """
        self.timer = Timer()
        self.prev = 0
        self.now = 0
        self.stop_counter = 0
        self.STOP_LIMIT = 7

    def update(self):
        """ タイマの更新 """
        self.prev = self.now
        self.now = self.timer.now()

    def check_progress(self):
        """ タイマの進行確認

        Returns:
            bool: タイマが進んでいればTrue, それ以外はFalseを返す
        """
        return self.now > self.prev
    
    def check_stop(self, color1, color2):
        """ 停止判定

        Args:
            color1 (string): ひとつ目のセンサの色
            color2 (string): ふたつ目のセンサの色

        Returns:
            bool: 停止用カウンタがSTOP_LIMITを超えたらTrue, それ以外はFalseを返す
        """
        if self.check_progress():
            if color1 == 'black' and color2 == 'black':
                self.stop_counter += 1
            else:
                self.stop_counter = 0

        return self.stop_counter > self.STOP_LIMIT



#========================================
## setup
hub = PrimeHub() # ハブのインスタンスの作成

# モータとセンサのインスタンスの作成
left = MotorAndSensor('A', 'C')
right = MotorAndSensor('B', 'D')
center = MotorAndSensor('F')

# 開始音の再生
hub.speaker.set_volume(100)
hub.speaker.beep(note=60, seconds=1.0)

# タイマの初期化
tc = TimeChecker()

#========================================
## main loop
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
## 停止処理
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