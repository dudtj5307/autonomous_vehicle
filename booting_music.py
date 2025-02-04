import RPi.GPIO as GPIO
import time

from controls import gpios

# GPIO VALUES
BUZZER = 12
BUZZER_ON, BUZZER_OFF = True, False
TIME_INTERVAL = 0.05

OCT1, OCT2, OCT3 = 1, 2, 4
BUZZER_freq = {"C": 130.8128, "C#": 138.5913, "D": 146.8324, "D#": 155.5635, "E": 164.8138, "F": 174.6141, "F#": 184.9972,
             "G": 195.9977, "G#": 207.6523, "A": 220.0000, "A#": 233.0819, "B": 246.9417}



# GPIO SETUPS
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)
buzzer = GPIO.PWM(BUZZER, BUZZER_freq["E"])

# DEFAULT PLAY LIST
DEFAULT_PLAY_LIST = [["E", OCT1, 1], ["A", OCT1, 1], ["A", OCT1, 3], ["B", OCT1, 1], ["C", OCT2, 1], ["A", OCT1, 1], ["A", OCT1, 0.5], ["A", OCT1, 0.2], ["C", OCT2, 1],
                     ["B", OCT1, 1], ["G", OCT1, 1], ["G", OCT1, 3], ["B", OCT1, 1], ["C", OCT2, 1], ["A", OCT1, 1], ["A", OCT1, 4]]

def BUZ_CONTROL(freq, octv, duration=TIME_INTERVAL):
    buzzer.start(1)
    buzzer.ChangeFrequency(BUZZER_freq[freq] * octv)
    time.sleep(duration)
    buzzer.stop()
    
def play_music(play_list = DEFAULT_PLAY_LIST):
    for freq, octv, ticks in play_list:
        if gpios.SWT_PUSHED():
            break
        BUZ_CONTROL(freq, octv, duration=TIME_INTERVAL * ticks)
        time.sleep(0.2)

if __name__ == "__main__":
    play_music()
    GPIO.cleanup()
