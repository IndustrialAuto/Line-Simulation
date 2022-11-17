import time
import threading
import logging
import datetime


logger = logging.getLogger('Filler_logs')
f_handler = logging.FileHandler('Filler_logs.log')
logger.addHandler(f_handler)
logger.setLevel(logging.DEBUG)
logger.info(f'Filler')


class filler:
    def __init__(self, speed):
        self.speed = speed
        self.counter = 0

    def set_speed(self, speed):
        self.speed = speed

    def fault(self, critical = False):
        self.critical = critical


    def start_filling(self, bottle_loading = True):
        self.bottle_loading = bottle_loading

        thread2 = threading.Thread(target=self.filling_counter, args=())
        thread2.daemon = True
        thread2.start()

    def filling_counter(self):
        while(self.bottle_loading):
            time.sleep(1)
            now = datetime.datetime.now()
            self.counter += int(self.speed/(60*60))
            #print(f'Filler: {self.counter}')
            #logger.info(f'Filler: {self.counter,        now.time()}')
