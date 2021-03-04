import pigpio
import RPi.GPIO as GPIO

_pi = pigpio.pi()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
