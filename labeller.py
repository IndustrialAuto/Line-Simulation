import time
import threading


# logger = logging.getLogger('machine_logs')

# f_handler = logging.FileHandler('machine_logs.log')
# logger.addHandler(f_handler)

# logger.setLevel(logging.DEBUG)

# logger.info(f'Playing with machine')


class labeller:
    def __init__(self, speed, counter = 0):
        self.speed = speed
        self.counter = counter

    def set_speed(self, speed):
        self.speed = speed

    def buffer_table(self, empty= False):
        self.empty = empty

        if(self.empty):
            self.start_labelling(bottle_labelling = False)

        
    def start_labelling(self, bottle_labelling = True):
        self.bottle_labelling = bottle_labelling

        thread = threading.Thread(target=self.labelling_counter, args=())
        thread.daemon = True
        thread.start()

    def labelling_counter(self):
        while(self.bottle_labelling==True):
            time.sleep(1)
            self.counter +=(self.speed/(60*60))

