from RPIO import PWM
import time

servo1 = PWM.Servo()
servo2 = PWM.Servo()

## FIRST MOTOR
servo1.set_servo(17, 1500)


## SECOND MOTOR
servo2.set_servo(18, 1500)

class RobotController:
    # Clockwise is positive

    # Servo1 = LEFT MOTOR
    # Servo2 = RIGHT MOTOR

    def __init__(self):
        self.velocity = 0
        self.angular_velocity = 0

    def to_pwm(self):
        right, left = self.velocity, self.velocity
        left += self.angular_velocity
        right -= self.angular_velocity
        m = max(left, right)
        if m > 1:
            left /= m
            right /= m
        left *= 700
        right *= 700
        left += 1500
        right += 1500
        return left, right

    def toMotor(self):
        left, right = self.to_pwm()
        servo1.set_servo(17, left)
        servo2.set_servo(18, right)

    def stopMoving(self):
        self.velocity = 0
        self.angular_velocity = 0
        self.toMotor()

    def move(self, direction, duration, velocity=1):
        dir = -1 if direction.lower() == "backwards" else 1
        self.velocity *= dir
        self.toMotor()
        time.sleep(duration)
        self.stopMoving()

    def turn(self, direction, duration, velocity=1):
        dir = -1 if direction.lower() == "clockwise" else 1
        self.angular_velocity *= dir
        self.toMotor()
        time.sleep(duration)
        self.stopMoving()


controller = RobotController()
