from time import sleep
import RPi.GPIO as GPIO

def TurnServoMotor(open):
    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        pin = 33
        GPIO.setup(pin, GPIO.OUT)
        #pulse width moderation, set the frequency
        pwm = GPIO.PWM(pin, 50)
        if (open):
            #Servo motor angle will always be initialise at 90 degree
            pwm.start(11.5)
            sleep(0.2)
            #Turn from 90 degree to 0 degree
            pwm.ChangeDutyCycle(2.0)
            sleep(4)
            #To prevent any jaggering
            pwm.ChangeDutyCycle(0)
            sleep(0.5)
            #Stop sending any pulse width
            pwm.stop()
            #Clean up used pin back to input pin (protection)
            GPIO.cleanup()
            return True
        else:
            pwm.start(11.5)
            sleep(1)
            pwm.stop()
            GPIO.cleanup()
            return True
        return False
    except:
        return False
