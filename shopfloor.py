#%%
import datetime
import time
import logging
import threading

from blower import blower
from filler import filler
from conveyor import conveyor
from labeller import labeller
from packer import packer
from palletizer import palletizer
from opcua import Server




#Instanciating Logger - 
logger = logging.getLogger('machine_logs')
f_handler = logging.FileHandler('machine_logs.log')
logger.addHandler(f_handler)
logger.setLevel(logging.DEBUG)
logger.info(f'Creating ShopFloor')




# Creating Production Machines - 
blower = blower(36000)
filler = filler(36000)
outfeed_conveyor = conveyor()
labeller = labeller(36000)
labeller_outfeed = conveyor()
packer = packer(3000)
packer_outfeed = conveyor()
palletizer = palletizer(30)



#Creating list for each counter
blower_infeed_count = [0]
filler_infeed_count = [0]
outfeed_conveyor_count = [0]
labeller_infeed_count = [0]




#Starting Blower & Filler in Production Mode - 
logger.info(f'Preform loading started!!')
blower.startstop_blower()
time.sleep(5)
logger.info(f'Filling Started!!')
filler.start_filling(bottle_loading=True)



#Starting OPC Server - 
def StartServer():
    print('server just get called')
    

    #Setting up OPC-UA Server 
    server=Server()

    print('Attempting to establish server')
    url = "opc.tcp://127.0.0.1:63362"
    server.set_endpoint(url)


    name= "OPC UA Simulation Server"
    addspace = server.register_namespace(name)
    node=server.get_objects_node()
    Param = node.add_object(addspace, "Parameters")



    Blower = Param.add_variable(addspace, "Blower_Counter",0)
    Filler = Param.add_variable(addspace, "Filler_Counter",0)
    Buffer_Conveyor = Param.add_variable(addspace, "Conveyor_Counter",0)
    Labeller = Param.add_variable(addspace, "Labler_Counter",0)

    Blower.set_writable()
    Filler.set_writable()
    Buffer_Conveyor.set_writable()
    Labeller.set_writable()

    try:
        server.start()
        print("Server started at {}".format(url))
    except:
        print("Failed to start server")

        
    while True:
        Machine1 = blower_infeed_count[-1]
        Machine2 = filler_infeed_count[-1]
        Machine3 = outfeed_conveyor_count[-1]
        Machine4 = labeller_infeed_count[-1]

        print(Machine1, Machine2, Machine3, Machine4)

        Blower.set_value(Machine1)
        Filler.set_value(Machine2)
        Buffer_Conveyor.set_value(Machine3)
        Labeller.set_value(Machine4)

        
        time.sleep(1)

thread5 = threading.Thread(target=StartServer, args=())
thread5.daemon = True





#Starting Buffer Conveyor
def buffer_conveyor():
    logger.info(f'Buffer Conveyor Started')
    while(blower.counter>filler.counter):
        time.sleep(1)
        now = datetime.datetime.now()
        outfeed_conveyor.buffer = filler_infeed_count[-1] - labeller_infeed_count[-1]
        outfeed_conveyor_count.append(outfeed_conveyor.buffer)
        logger.info(f'Buffer Table: {outfeed_conveyor_count[-1], now.time()}')


thread3 = threading.Thread(target=buffer_conveyor, args=())
thread3.daemon = True






#Starting Labeller in Production Mode -
def labeler_infeed(): 
    logger.info(f'Labelling started!!')
    labeller.start_labelling(bottle_labelling= True)
    d=0
    while(d==0):
        time.sleep(1)
        now = datetime.datetime.now()
        labeller_infeed_count.append(labeller.counter)
        logger.info(f'Lebeller Counter: {labeller_infeed_count[-1], now.time()}')
    

thread4 = threading.Thread(target=labeler_infeed, args=())
thread4.daemon = True







#Appending Blower & Filler counter into the list & running conditions
a=0
b=0
c=0
i=0

while(a==0):
    time.sleep(1)

    #Appending Blower & Filler counter value to the list
    blower_infeed_count.append(blower.counter)
    filler_infeed_count.append(filler.counter)
    now = datetime.datetime.now()
    logger.info(f'Blower: {blower_infeed_count[-1], now.time()}')
    logger.info(f'Filler: {filler_infeed_count[-1], now.time()}')


    #Restricting the size of the list to 5 for blower - 
    if(len(blower_infeed_count)>5):
        blower_infeed_count.pop(0)
    else:
        continue
    #Restricting the size of the list to 5 for filler- 
    if(len(filler_infeed_count)>5):
        filler_infeed_count.pop(0)
    else:
        continue


    #Calling conveyor function to start
    for i in range(len(blower_infeed_count)):
        if(filler_infeed_count[i]>70 and b==0 ):
           thread3.start()
           b= b+1
        else: 
            continue 
    #Calling labeller function to start
    if(len(outfeed_conveyor_count)>10 and c==0):
        thread4.start()
        print('Now calling Thread 5')
        thread5.start()
        
        
        c = c+1
    else:
        continue



















































    



#%%
#Starting Buffer Table in Production Mode
def buffer_conveyor():
    logger.info(f'Buffer Conveyor Running!!')
    outfeed_conveyor.buffer = filler.counter - labeller.counter
    i=0
    while(blower.counter>filler.counter):
        time.sleep(2)
        outfeed_conveyor.buffer = filler.counter - labeller.counter
        logger.info(f'Blower: {blower.counter}')
        logger.info(f'Filler: {filler.counter}')
        logger.info(f'Buffer Table: {outfeed_conveyor.buffer}')

        #starting labeller
        if(outfeed_conveyor.buffer>150 and i==0):
            logger.info(f'Calling Labeller')
            start_labelling()
            i=i+1

        #Blower will stop if buffer table is full - 
        elif(outfeed_conveyor.buffer > 1000 ):
            blower.startstop_blower(signal_loading=False)
        else:
            blower.startstop_blower(signal_loading=True)

        #Filler will stop if blower will stop
        if(blower.startstop_blower(signal_loading=False)):
            filler.start_filling(bottle_loading=False)
        else:
            filler.start_filling(bottle_loading=True)

        #filler will stop if filler counter becomes equal to blower counter
        time.sleep(1)
        if(filler.counter >= blower.counter):
            filler.start_filling(bottle_loading=False)
            blower.startstop_blower(signal_loading=False)
            logger.info(f'Blower Counter{blower.counter}')
            logger.info(f'Filler Counter{filler.counter}')
            logger.info(f'Combi counter runout at filler')
            while(filler.counter >= blower.counter):
                time.sleep(1)
                outfeed_conveyor.buffer = filler.counter - labeller.counter
                time.sleep(10)
                logger.info(f'Buffer Table: {outfeed_conveyor.buffer}')

        
        
#buffer_conveyor()

thread3 = threading.Thread(target=buffer_conveyor, args=())
thread3.daemon = True
thread3.start()

#%%

#Starting Labeller in Production Mode - 
def start_labelling():
    thread4 = threading.Thread(target=labeler_infeed, args=())
    thread4.daemon = True
    thread4.start()
    

def labeler_infeed(): 
    logger.info(f'Labelling started!!')
    while(outfeed_conveyor.buffer>150):
        if(outfeed_conveyor.buffer> 250):
            time.sleep(1)
            labeller.start_labelling(bottle_labelling= True)
            logger.info(f'Lebeller Counter: {labeller.counter}')
        if(labeller.counter >= outfeed_conveyor.buffer):
            labeller.buffer_table(empty=True)
            time.sleep(2)
            logger.info(f'Waiting for bottles')
            





#%%
#Starting Packer in Production
while(labeller_outfeed>100):
    if(labeller.outfeed>200):
        packer.start_packer(packing=True)
    elif():
        packer.start_packer(packing=False)

    logger.info(f'Packer Counter: {packer.counter}')



#%%
#Packer Outfeed Conveyor Accumulation Counter
packer_outfeed = packer.counter - palletizer.counter




#%%
#Start Palletiser in production - 
while(packer_outfeed > 100):
    palletizer.start_pallet(palletizing=True)

    logger.info(f'Palletiser: {palletizer.counter}')















































# # %%

# #%%
# #creating machines - 
# m1_blower = blower(36000)
# # filler = filler(36000)
# # outfeed_conveyor = conveyor()
# # labeller = labeller(48000)
# # labeller_outfeed = conveyor()
# # packer = packer(3000)
# # packer_outfeed = conveyor()
# # palletiser = palletiser(30)
# # %%
# m1_blower.startstop_blower()
# print(f'Blower: {m1_blower.counter}')
# # %%
# while(m1_blower.counter>0):

#     print(f'Blower: {m1_blower.counter}')
# %%
