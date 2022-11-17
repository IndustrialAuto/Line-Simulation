
# logger = logging.getLogger('machine_logs')

# f_handler = logging.FileHandler('machine_logs.log')
# logger.addHandler(f_handler)

# logger.setLevel(logging.DEBUG)

# logger.info(f'Playing with machine')


class conveyor:
    def __init__(self, accumulation=False, buffer=0):
        self.accumulation = accumulation
        self.buffer = buffer

