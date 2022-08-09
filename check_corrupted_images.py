import os
import shutil

import PIL
from PIL import Image

import numpy as np

# work_folder = "/media/shawnle/1d06d0af-a74d-4e24-904e-109c07747950/home/mpnet-melodic/Downloads/ssl_curate_data"
work_folder = "/media/shawnle/1d06d0af-a74d-4e24-904e-109c07747950/home/mpnet-melodic/Downloads/industryobj-0.9/SolomonData2-0.9"

min_size = 200
max_size = 2000

def check_image(img):
    try:
        with Image.open(img) as im:
            if min(im.size) < min_size or max(im.size) > max_size:
                raise PIL.UnidentifiedImageError
            im.convert('RGB')
    except OSError:
        print('OSError with file {} ...'.format(img))
    except FileNotFoundError:
        print('File not found {} ...'.format(img))
    except TypeError:
        print('Type error')
    except ValueError:
        print('Value error with file {} ...'.format(img))
    except PIL.UnidentifiedImageError:  
        print('UnidentifiedImageError')

err_cnt = 0
for fn in os.listdir(work_folder):
    if fn.endswith('bmp') or fn.endswith('png') or fn.endswith('jpg') or fn.endswith('jpeg'):
        afn = os.path.join(work_folder, fn)

        try:
            check_image(afn)
        except:
            print('read image error {} ...'.format(fn.strip()))
            err_cnt+=1
print('There are total {} corrupted images.'.format(err_cnt))            
print('Done.')
    

