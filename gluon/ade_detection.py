import numpy as np
import matplotlib.pyplot as plt
from gluoncv.data import ADE20KSegmentation
import matplotlib.image as mpimg
from gluoncv.utils.viz import get_color_pallete

train_dataset = ADE20KSegmentation(split='train')
val_dataset = ADE20KSegmentation(split='val')
print('Training images:', len(train_dataset))
print('Validation images:', len(val_dataset))

img, mask = val_dataset[0]
# get pallete for the mask
mask = get_color_pallete(mask.asnumpy(), dataset='ade20k')
mask.save('mask.png')

# subplot 1 for img
fig = plt.figure()
fig.add_subplot(1,2,1)
plt.imshow(img.asnumpy().astype('uint8'))
# subplot 2 for the mask
mmask = mpimg.imread('mask.png')
fig.add_subplot(1,2,2)
plt.imshow(mmask)
# display
plt.show()
