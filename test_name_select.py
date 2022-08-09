import os

name = '/media/shawnle/Pass_Data/3. Pass Data/JH/BK/RTX4K/20210528_Test4TRI/Instance Segmentation4 Tool1/Images/t000023.bmp\n'
blacklist_clsnm = ['images', 'DetectImages', 'Tool', 'Pass', 'media', 'shawn', 'Train', 'test', 'Example', 'single', 'data']

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

all_classes = set()
for c in ['RTX4K','1','CAT']: all_classes.add(c)
ns = NameSelector(all_classes)
print(ns.select(os.path.dirname(name)))
print('Done.')