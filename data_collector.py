import os
import shutil
import cv2

import PIL
from PIL import Image

import numpy as np

work_folder = "/media/shawnle/1d06d0af-a74d-4e24-904e-109c07747950/home/mpnet-melodic/Downloads/ssl_curate_data/"
target_folder = "PassData547k"
blacklist_clsnm = ['images', 'DetectImages', 'Tool', 'Pass', 'media', 'shawn', 'Train', 'test', 'Example', 'single', 'data', 'Recognizer', 'html']
# filelistname = "pass_data_images_9.txt"
filelistname = "passdata547k_img.txt"
filelist = os.path.join(work_folder, filelistname)
with open(filelist, 'r') as f:
    lines = f.readlines()

perm_idx = np.random.permutation(len(lines))

max_img = 999999 
num = max_img if max_img < len(lines) else len(lines)
min_size = 200
max_size = 2000
use_symlink = True
check_only = True

stats = {'oserr': 0,
'sizeerr': 0,
'notfound': 0,
'valerr': 0,
'typeerr': 0,
'uniderr': 0
}

class NameSelector:
    def __init__(self, classes):
        self.classes = classes

    def select(self,parent_path):
        classname = os.path.basename(parent_path)
        if classname in self.classes :
            return classname
        elif classname != '' and sum([n.lower() in classname.lower() for n in  blacklist_clsnm]) == 0:
            self.classes.add(classname)
            return classname
        else:
            if os.path.dirname(parent_path) != parent_path:
                return self.select(os.path.dirname(parent_path))
            else:
                classname = 'noname' + str(len(self.classes)+1)
                self.classes.add(classname)
                return classname

def check_image(img):
    try:
        with Image.open(img) as im:
            if min(im.size) < min_size or max(im.size) > max_size:
                raise cv2.Error.BadImageSize
            im.convert('RGB')
    except OSError:
        print('OSError with file {} ...'.format(img.strip()))
        stats['oserr'] += 1
    except FileNotFoundError:
        print('File not found {} ...'.format(img.strip()))
        stats['notfound'] += 1
    except TypeError:
        print('Type error with file {} ...'.format(img.strip()))
        stats['typeerr'] += 1
    except ValueError:
        print('Value error with file {} ...'.format(img.strip()))
        stats['valerr'] += 1
    except PIL.UnidentifiedImageError:  
        print('UnidentifiedImageError file {} ...'.format(img.strip()))
        stats['uniderr'] += 1
    except cv2.Error.BadImageSize:
        print('image size too large or too small file {} ...'.format(img.strip()))
        stats['sizeerr'] += 1

all_classes = set()
ns = NameSelector(all_classes)
for id in perm_idx[:num]:
    src = lines[id].strip()
    src_dir = ns.select(os.path.dirname(src))
    dst_fd = os.path.join(work_folder, target_folder, src_dir)

    fn = os.path.basename(src)
    dst = os.path.join(dst_fd, fn)

    try:
        check_image(src)
        if not check_only:
            try:
                if not os.path.exists(os.path.dirname(dst.strip())):
                    os.makedirs(os.path.dirname(dst.strip())) 
                if not use_symlink:
                    shutil.copy(src.strip(), dst.strip())
                else:
                    try:
                        os.symlink(src.strip(), dst.strip())
                    except OSError:
                        print('symlink privilege error')
            except:
                print('copying file {} failed...'.format(dst.strip()))
    except:
        pass 
print('Report:', stats)
print('Done.')
    

