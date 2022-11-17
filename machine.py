#%%
import time
import logging
import threading

#%%
logger = logging.getLogger('machine_logs')

f_handler = logging.FileHandler('machine_logs.log')
logger.addHandler(f_handler)

logger.setLevel(logging.DEBUG)

logger.info(f'Playing with machine')

#%%
class machine:
    def __init__(self, speed):
        self.speed = speed
        self.counter = 0

    def set_speed(self, speed):
        self.speed = speed

    def set_signals(self, signal_critical=False, signal_alert=False):
        self.signal_critical = signal_critical
        self.signal_alert = signal_alert

        if ((self.signal_critical) or (self.signal_alert)):
            machine.startstop_machine(signal_loading=False)

        else:
            self.startstop_machine(signal_loading=True)

    def startstop_machine(self, signal_loading=True):
        self.signal_loading = signal_loading

        if self.signal_loading:
            self.signal_critical = False
            self.signal_alert = False

        thread = threading.Thread(target=self.counter_loop, args=())
        thread.daemon = True
        thread.start()

    def counter_loop(self):
        while (self.signal_loading):
            time.sleep(1)
            self.counter += (self.speed/(60*60))
            logger.info(f'Blower: {self.counter}')

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

        thread = threading.Thread(target=self.filling_counter, args=())
        thread.daemon = True
        thread.start()

    def filling_counter(self):
        while(self.bottle_loading):
            time.sleep(1)
            self.counter +=(self.speed/(60*60))
            logger.info(f'Filler: {filler.counter}')
    

class conveyor:
    def __init__(self, accumulation=False, buffer=0):
        self.accumulation = accumulation
        self.buffer = buffer

class labeller:
    def __init__(self, speed, counter = 0):
        self.speed = speed
        self.counter = counter

    def set_speed(self, speed):
        self.speed = speed


    def start_labelling(self, bottle_labelling = True):
        self.bottle_labelling = bottle_labelling

        thread = threading.Thread(target=self.labelling_counter, args=())
        thread.daemon = True
        thread.start()

    def labelling_counter(self):
        while(self.bottle_labelling):
            time.sleep(1)
            self.counter +=(self.speed/(60*60))

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
    

class palletiser:
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
    

#%%
#creating machines - 
blower = machine(36000)
filler = filler(36000)
outfeed_conveyor = conveyor()
labeller = labeller(48000)
labeller_outfeed = conveyor()
packer = packer(3000)
packer_outfeed = conveyor()
palletiser = palletiser(30)


#%%
#Blower in production mode
blower.startstop_machine()


#filler in production mode
time.sleep(4)
filler.start_filling(bottle_loading=True)


#%%
#Buffer Table Conveyor accumulation counter
i = 0
while(blower.counter>filler.counter):
    time.sleep(1)
    outfeed_conveyor.buffer = filler.counter - labeller.counter
    logger.info(f'Buffer Table: {outfeed_conveyor.buffer}')

    #Blower will stop if buffer table is full - 
    if(outfeed_conveyor.buffer > 300 ):
        blower.startstop_machine(signal_loading=False)
    else:
        blower.startstop_machine(signal_loading=True)

    #Filler will stop if blower will stop
    if(blower.startstop_machine(signal_loading=False)):
        filler.start_filling(bottle_loading=False)

    #filler will stop if filler counter becomes equal to blower counter
    if(filler.counter >= blower.counter):
        filler.start_filling(bottle_loading=False)
        blower.startstop_machine(signal_loading=False)

#%%
#Labeller in production mode
while(outfeed_conveyor.buffer>150):
    if(outfeed_conveyor.buffer> 250):
        time.sleep(1)
        labeller.start_labelling(bottle_labelling= True)

    elif(outfeed_conveyor.buffer == 0):
        labeller.start_labelling(bottle_labelling=False)

    logger.info(f'Lebeller Counter: {labeller.counter}')


#%%
#Labeller Outfeed Conveyor Accumulation Counter 
labeller_outfeed = labeller.counter - packer.counter


#%%
#Start Packer in production 
while(labeller_outfeed>100):
    if(labeller.outfeed>200):
        packer.start_packer(packing=True)
    elif(labeller.outfeed == 0):
        packer.start_packer(packing=False)

    logger.info(f'Packer Counter: {packer.counter}')


#Packer Outfeed Conveyor Accumulation Counter
packer_outfeed = packer.counter - palletiser.counter


#Start Palletiser in production - 
while(packer_outfeed > 100):
    palletiser.start_pallet(palletizing=True)

    logger.info(f'Palletiser: {palletiser.counter}')












# %%
