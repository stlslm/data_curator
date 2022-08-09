import multiprocessing as mp
from multiprocessing import Process, Queue
import threading
import time

multiplier = 16
num_workers = mp.cpu_count() * multiplier

def adjust_index(index, st, tg=','):
    """ adjust the index from the given index to the nearest one that is the target character """
    while st[index] != tg:
        index+=1
    return index

def worker(pid, subs, q):
    print('pid={} starts...'.format(pid))
    cid, st = q.get()
    print('pid={} gets cid={} ...'.format(pid,cid))
    for f_jpg in subs:
        f_png = f_jpg.replace('.jpg','.png')
        st = st.replace(f_jpg, f_png)
        q.put((cid,st))

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
ps = []
t0 = time.time()
q = Queue()
for pid in range(num_workers):
    start = adjust_index(pid*chunk_size, data) if pid!=0 else 0
    end = adjust_index((pid+1)*chunk_size, data) if pid != num_workers-1 else len(data)

    cid=pid
    q.put((cid, data[start:end]))
    p = Process(target=worker, args=(pid, lines, q))
    ps.append(p)
    p.start()

data1 = ''
while not q.empty():
    cid, s = q.get()
for pid, p in enumerate(ps):
    p.join()
    print('Process {} finished.'.format(pid))
t1 = time.time()
print('It takes total {} (s).'.format(t1-t0))
print('Done.')