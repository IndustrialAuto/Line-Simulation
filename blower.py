import time
import threading
import logging
import datetime

logger = logging.getLogger('Blower_logs')
f_handler = logging.FileHandler('Blower_logs.log')
logger.addHandler(f_handler)
logger.setLevel(logging.DEBUG)
logger.info(f'Blower')

class blower:
    def __init__(self, speed):
        self.speed = speed
        self.counter = 0

    def set_speed(self, speed):
        self.speed = speed

    def set_signals(self, signal_critical=False, signal_alert=False):
        self.signal_critical = signal_critical
        self.signal_alert = signal_alert

        if ((self.signal_critical) or (self.signal_alert)):
            self.startstop_blower(signal_loading=False)

        else:
            self.startstop_blower(signal_loading=True)

    def startstop_blower(self, signal_loading=True):
        self.signal_loading = signal_loading

        if self.signal_loading:
            self.signal_critical = False
            self.signal_alert = False

        thread1 = threading.Thread(target=self.counter_loop, args=())
        thread1.daemon = True
        thread1.start()

    def counter_loop(self):
        while (self.signal_loading):
            time.sleep(1)
            now = datetime.datetime.now()
            self.counter += int(self.speed/(60*60))
            #logger.info(f'Blower: {self.counter,        now.time()}')
            #print(f'Blower: {self.counter}')
