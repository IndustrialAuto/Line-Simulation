import time
import threading


# logger = logging.getLogger('machine_logs')

# f_handler = logging.FileHandler('machine_logs.log')
# logger.addHandler(f_handler)

# logger.setLevel(logging.DEBUG)

# logger.info(f'Playing with machine')


class packer:
    def __init__(self, speed, counter = 0):
        self.speed = speed
        self.counter = counter

    def set_speed(self, speed):
        self.speed = speed


    def start_packer(self, packing = False):
        self.packing = packing

        thread = threading.Thread(target=self.packer_counter, args=())
        thread.daemon = True
        thread.start()

    def packer_counter(self):
        while(self.packing):
            time.sleep(1)
            self.counter +=(self.speed/(60*60))
    
