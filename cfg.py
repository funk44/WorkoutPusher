#import queue
import multiprocessing

# q = queue.Queue()
q = multiprocessing.Queue()

print("cfg.py is running in process {}".format(multiprocessing.current_process()))

