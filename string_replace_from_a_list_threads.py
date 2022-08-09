import multiprocessing as mp
import threading
from threading import Thread
import time
from time import sleep

multiplier = 16
num_workers = mp.cpu_count() * multiplier

def adjust_index(index, st, tg=','):
    """ adjust the index from the given index to the nearest one that is the target character """
    while st[index] != tg:
        index+=1
    return index

def worker(tid, subs, st):
    print('Thread {} starts ...'.format(tid))
    for f_jpg in subs:
        f_png = f_jpg.replace('.jpg','.png')
        st = st.replace(f_jpg, f_png)

class worker_thread(threading.Thread):
    def __init__(self, tid, subs, st):
        Thread.__init__(self)
        self.tid = tid
        self.st = st
        self.subs = subs

    def run(self):
        sleep(1)

        print('Thread {} starts ...'.format(self.tid))
        for f_jpg in self.subs:
            f_png = f_jpg.replace('.jpg','.png')
            self.st = self.st.replace(f_jpg, f_png)

''' The huge text file (~1.3GB) to be read as one string
'''
string_file = "docs/trainval.json"

''' List contains all the sub-string to be found in the huge string_file
'''
list_file = "docs/png_renamed_images.txt"
with open(list_file, 'r') as f:
    lines = f.readlines()
    lines = [l.strip() for l in lines]

with open(string_file, 'r') as f:
    data = f.read()

chunk_size = len(data) // num_workers
ts = []
t0 = time.time()
for tid in range(num_workers):
    start = adjust_index(tid*chunk_size, data) if tid!=0 else 0
    end = adjust_index((tid+1)*chunk_size, data) if tid != num_workers-1 else len(data)

    # t = threading.Thread(target=worker, args=(tid, lines, data[start:end],))
    t = worker_thread(tid, lines, data[start:end])
    ts.append(t)
    t.start()

data1=''
for tid, t in enumerate(ts):
    t.join()
    print('Thread {} finished.'.format(t.tid))
    data1+=t.st
t1 = time.time()

with open(string_file+'.rep', 'w') as f:
    f.write(data1)
print('It takes total {} (s).'.format(t1-t0))
print('Done.')