import os
import shutil

import PIL
from PIL import Image

import numpy as np

# work_folder = "/media/shawnle/1d06d0af-a74d-4e24-904e-109c07747950/home/mpnet-melodic/Downloads/ssl_curate_data"
work_folder = "/media/shawnle/1d06d0af-a74d-4e24-904e-109c07747950/home/mpnet-melodic/Downloads/jpg_wrong_images"

img_list = "png_renamed_images.txt"

with open(img_list, 'r') as f:
    lines = f.readlines()
lines = [l.strip() for l in lines]

err_cnt = 0
do_rename = False
for jpg_img in lines:
    src = jpg_img.replace('.jpg','.png')
    dst = jpg_img

    asrc = os.path.join(work_folder, src)
    adst = os.path.join(work_folder, dst)
    print('renaming {} to {} ...'.format(src,dst))
    if do_rename:
        shutil.move(asrc,adst)
print('Done.')
    

