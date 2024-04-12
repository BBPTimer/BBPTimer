########## Variables (see README)

# reedPin (required)
reedPin = 26

# warmup (optional)
warmup = 0.0

# preInfuse (optional)
preInfuse = 5.0

# cooldown (required, change this value after timing your first shot)
cooldown = 0.0

########## NO NEED TO EDIT ANYTHING BELOW HERE ##########

import RPi.GPIO as GPIO
import time
import os

########## Stopwatch.py Copyright (c) 2018-2024 Ravener
########## https://github.com/ravener/stopwatch.py

class Stopwatch:
    digits: int

    def __init__(self, digits: int = 2):
        self.digits = digits

        self._start = time.perf_counter()
        self._end = None

    @property
    def duration(self) -> float:
        return (
            self._end - self._start if self._end else time.perf_counter() - self._start
        )

    @property
    def running(self) -> bool:
        return not self._end

    def restart(self) -> None:
        self._start = time.perf_counter()
        self._end = None

    def reset(self) -> None:
        self._start = time.perf_counter()
        self._end = self._start

    def start(self) -> None:
        if not self.running:
            self._start = time.perf_counter() - self.duration
            self._end = None

    def stop(self) -> None:
        if self.running:
            self._end = time.perf_counter()
            return 1
        else:
            return 0

    def __str__(self) -> str:
        time = self.duration

        if time >= 1:
            return "{:.{}f}s".format(time, self.digits)

        if time >= 0.01:
            return "{:.{}f}ms".format(time * 1000, self.digits)

        return "{:.{}f}μs".format(time * 1000 * 1000, self.digits)

########## End of Stopwatch.py

# Initialize stopwatch
shot = Stopwatch(2)
shot.reset()

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Setup the GPIO pin as an input
GPIO.setup(reedPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

offMS = 0

try:
    while True:

        if GPIO.input(reedPin) == 0:
            if shot.running == False:
                shot.restart()
            offMS = 0
        if GPIO.input(reedPin) == 1:
            if offMS == 15:
                done = shot.stop()
                if done == 1:
                    os.system('clear')
                    print (round((shot.duration-warmup-cooldown), 1), 's\nTurn your volume back down.\nEnjoy your coffee!')
                    GPIO.cleanup()
                    break
            offMS+=1

        if round((shot.duration-warmup), 1) == preInfuse: # Bell at end of pre-infuse
            print('\a')
        os.system('clear')
        print(round((shot.duration-warmup), 1), 's')
        if GPIO.input(reedPin) == 1 and shot.running == False:
            print('Turn up your volume to make sure you hear the pre-infuse bell.')
        
        time.sleep(0.1)  # Add a small delay to avoid excessive reads

except KeyboardInterrupt:
    print("Enjoy your coffee?")
    GPIO.cleanup()
