import os
import shutil

import PIL
from PIL import Image

import numpy as np

work_folder = "/media/shawnle/1d06d0af-a74d-4e24-904e-109c07747950/home/mpnet-melodic/Downloads/ssl_curate_data/"
target_folder = "PassData547k_symlink"
blacklist_clsnm = ['images', 'DetectImages', 'Tool', 'Pass', 'media', 'shawn', 'Train', 'test', 'Example', 'single', 'data', 'Recognizer', 'html']
filelistname = "pass_data_images_9.txt"
filelist = os.path.join(work_folder, filelistname)
with open(filelist, 'r') as f:
    lines = f.readlines()

perm_idx = np.random.permutation(len(lines))

max_img = 500 
num = max_img if max_img < len(lines) else len(lines)
min_size = 200
max_size = 2000
use_symlink = True

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

all_classes = set()
ns = NameSelector(all_classes)
for id in perm_idx[:num]:
    src = lines[id]
    src_dir = ns.select(os.path.dirname(src))
    dst_fd = os.path.join(work_folder, target_folder, src_dir)

    fn = os.path.basename(src)
    dst = os.path.join(dst_fd, fn)

    try:
        check_image(src)
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
print('Done.')
    

