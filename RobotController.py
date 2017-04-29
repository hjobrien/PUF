from RPIO import PWM

servo1 = PWM.Servo()
servo2 = PWM.Servo()

## FIRST MOTOR
# Set servo on GPIO17 to 800µs
servo1.set_servo(17, 800)
# Set servo on GPIO17 to 2200µs
servo1.set_servo(17, 2200)

## SECOND MOTOR
servo2.set_servo(18, 800)
servo2.set_servo(18, 2000)

# Clear servo on GPIO17 and GPIO18
servo1.stop_servo(17)
servo2.stop_servo(18)


class Servo:

   def __init__(self, dma_channel=0, subcycle_time_us=20000, pulse_incr_us=10):
       """Makes sure PWM is setup with the correct increment granularity and
       subcycle time.
       """
       self.dma_channel = dma_channel
       self.subcycle_time_us = subcycle_time_us
       self.pulse_incr_us = pulse_incr_us

   def set_servo(self, gpio, pulse_width_us):
       """Sets a pulse-width on a gpio to repeat every subcycle
       (by default every 20ms).
       """


   def stop_servo(self, gpio):
      "Stops servo activity for this gpio"
