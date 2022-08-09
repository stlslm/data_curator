import os
import shutil

import PIL
from PIL import Image

import numpy as np

# work_folder = "/media/shawnle/1d06d0af-a74d-4e24-904e-109c07747950/home/mpnet-melodic/Downloads/ssl_curate_data"
work_folder = "/media/shawnle/1d06d0af-a74d-4e24-904e-109c07747950/home/mpnet-melodic/Downloads/jpg_wrong_images"


err_cnt = 0
do_rename = True
for fn in os.listdir(work_folder):
    if fn.endswith('bmp') or fn.endswith('png') or fn.endswith('jpg') or fn.endswith('jpeg'):
        afn = os.path.join(work_folder, fn)

        is_png=False
        with open(afn, 'rb') as f:
            f = f.read()
            b = bytearray(f)
            # print(b[0], ' ' , b[1])
            if b[0]==137 and b[1]==80:
                is_png = True
        
        if fn.endswith('jpg') and is_png:
            print('renaming file {} to png'.format(fn))
            if do_rename:
                fn_png = fn.replace('.jpg','.png')
                afn_png = os.path.join(work_folder, fn_png)
                os.rename(afn, afn_png)
                err_cnt+=1
print('There are total {} corrupted images.'.format(err_cnt))            
print('Done.')
    

