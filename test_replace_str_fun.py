import multiprocessing as mp
import threading
from threading import Thread
import time
from time import sleep

multiplier = 0.25
num_workers = int(mp.cpu_count() * multiplier)

def adjust_index(index, st, tg=','):
    """ adjust the index from the given index to the nearest one that is the target character """
    while st[index] != tg:
        index+=1
    return index

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

def work(tid, subs, start, end):
    st = data
    print('Thread {} starts ...'.format(tid))
    for f_jpg in subs:
        f_png = f_jpg.replace('.jpg','.png')
        st = st.replace(f_jpg, f_png)

''' The huge text file (~1.3GB) to be read as one string
'''
string_file = "docs/trainval.json"

''' List contains all the sub-string to be found in the huge string_file
'''
list_file = "docs/png_renamed_images.txt"
lines=["28052022014851_Image_1.jpg",
"28052022015035_Image_1.jpg"]

data="28052022014743_Image_1.jpg, \
28052022014800_Image_1.jpg, \
28052022014817_Image_1.jpg, \
28052022014833_Image_1.jpg, \
28052022014851_Image_1.jpg, \
28052022014908_Image_1.jpg, \
28052022014926_Image_1.jpg, \
28052022014944_Image_1.jpg, \
28052022015001_Image_1.jpg, \
28052022015018_Image_1.jpg, \
28052022015035_Image_1.jpg, \
28052022015051_Image_1.jpg, \
28052022015108_Image_1.jpg, \
28052022015126_Image_1.jpg, \
28052022015142_Image_1.jpg"

chunk_size = len(data) // num_workers
ts = []
t0 = time.time()
for tid in range(num_workers):
    start = adjust_index(tid*chunk_size, data) if tid!=0 else 0
    end = adjust_index((tid+1)*chunk_size, data) if tid != num_workers-1 else len(data)

    t = worker_thread(tid, lines, data[start:end])
    ts.append(t)
    t.start()

data1=''
for tid, t in enumerate(ts):
    print('tid={}; value={}'.format(t.tid, t.st))
    t.join()
    print('Thread {} finished.'.format(tid))
    data1+=t.st
t1 = time.time()

with open(string_file+'.rep', 'w') as f:
    f.write(data1)
print('It takes total {} (s).'.format(t1-t0))
print('Done.')
