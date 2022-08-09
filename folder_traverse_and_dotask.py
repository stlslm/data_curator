import os
import shutil

do_task=True#False#True
do_copy=True
count=999999
cnt=0

def task(file):
    try:
        print('filename:', file, ' --> ', os.readlink(file))
        target = os.readlink(file)
        if do_copy:
            shutil.move(file, file+'.bk')
            shutil.copy(target, file)
            global cnt
            cnt+=1
        print('copying ',target,' to ',file,'...')
    except OSError:
        print(file,' is not a symlink. skipping...')

def walk_and_do(path, task=None):
    all = []
    global cnt
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.bmp') or f.endswith('.jpeg'):
                if do_task:
                    task(os.path.join(root,f))
                #cnt+=1
                if cnt>count:
                    return
        for d in dirs:
            print('recursive to root {}, folder {}...'.format(root,d))
            walk_and_do(os.path.join(root,d), task)

def count_links(path, task=None):
    all = []
    cnt = 0
    for root, dirs, files in os.walk(path):
        if len(dirs)==0:
            for f in files:
                if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.bmp') or f.endswith('.jpeg'):
                    path = os.path.join(root,f)
                    if os.path.islink(path):
                        cnt+=1
                        print(path)
                    else:
                        print('failed check:',path)
        else:
            print(dirs)
            return 0
    return cnt

if __name__ == '__main__':

    #path="./PassData547k/"
    path="/home/solomon/public/Shawn/Datasets/solom_ssl/Images"
    #path="/home/solomon/public/Shawn/Datasets/solom_ssl/Images/industryobj-0.6/"
    walk_and_do(path, task)
    #print('there are total: ', count_links(path), ' links.')
    print('Done.')