import os 

import cv2 

import torch
import torchvision as tv

from pycocotools.coco import COCO

workfolder = "/media/shawnle/1d06d0af-a74d-4e24-904e-109c07747950/home/mpnet-melodic/Downloads/industryobj-0.9/train"
num_img = 200000
output = os.path.join(workfolder, "..", "output","train200k")

class simpleCOCOdataset(tv.datasets.coco.CocoDetection):
    def __init__(self, ann_file, root):
        super(simpleCOCOdataset, self).__init__(root, ann_file)

cocodat = simpleCOCOdataset(os.path.join(workfolder, 'trainval.json'), workfolder)

c=0
start_at = 0
for k, a in cocodat.coco.anns.items():
    x,y,w,h = a['bbox']
    cid = a['category_id']
    cname = cocodat.coco.cats[cid]['name']
    iid = a['image_id']
    try: 
        im = cocodat.coco.imgs[iid]
    except:
        continue
    
    img = cv2.imread(os.path.join(workfolder, im['file_name']))

    try:
        h_exp=int(0.15*h)
        w_exp=int(0.15*w)
        cropped_image = img[y-h_exp:y+h+h_exp, x-w_exp:x+w+w_exp]
    except:
        print('cropping failed.')
        continue
    if not os.path.exists(os.path.join(output, cname)): 
        os.makedirs(os.path.join(output, cname))
    try: 
        cv2.imwrite(os.path.join(output, cname, "{}_{}.jpg".format(iid,k)),cropped_image)
        c+=1
        if c<start_at:
            os.remove(os.path.join(output, cname, "{}_{}.jpg".format(iid,k)))
    except: 
        continue
    if c>start_at+num_img: break 
print('Done.')