import os
import matplotlib.pyplot as plt

import numpy as np

imagenet_data_folder = "/media/shawnle/1d06d0af-a74d-4e24-904e-109c07747950/home/mpnet-melodic/Downloads/industryobj-0.9/output/train400k" 

classes = []
img_per_class = dict()
for fd in os.listdir(imagenet_data_folder):
    classes.append(fd)
    ims = os.listdir(os.path.join(imagenet_data_folder, fd))
    img_per_class[fd] = len(ims)

plt.bar(np.arange(len(classes)),np.array(list(img_per_class.values())), tick_label=list(img_per_class.keys()))
plt.xticks(rotation=90)
plt.title('IndustryObject-400k Data Distribution per Class')
plt.show()

print('Total {} classes: {}'.format(len(classes), classes))
print('Data stats:', img_per_class)