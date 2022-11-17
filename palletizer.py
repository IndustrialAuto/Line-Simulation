import time
import threading




# logger = logging.getLogger('machine_logs')

# f_handler = logging.FileHandler('machine_logs.log')
# logger.addHandler(f_handler)

# logger.setLevel(logging.DEBUG)

# logger.info(f'Playing with machine')

class palletizer:
    def __init__(self, speed, counter = 0):
        self.speed = speed
        self.counter = counter

    def set_speed(self, speed):
        self.speed = speed


    def start_pallet(self, palletizing = False):
        self.palletizing = palletizing

        thread = threading.Thread(target=self.pallet_counter, args=())
        thread.daemon = True
        thread.start()

    def pallet_counter(self):
        while(self.palletizing):
            time.sleep(1)
            self.counter +=(self.speed/(60*60))
