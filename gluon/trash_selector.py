import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def get_box(labeled_img):
    labels = np.unique(labeled_img)
    roi = np.zeros((len(labels[1:]),labeled_img.shape[0],labeled_img.shape[1]))
    roi2 = np.zeros((len(labels[1:]),labeled_img.shape[0],labeled_img.shape[1]))
    i=0
    for l in labels[1:]:
        slice_x, slice_y = ndimage.find_objects(labeled_img==l)[0]
        #roi[i] = labeled_img[slice_x, slice_y]
        roi[i,slice_x, slice_y]=l
        x,y=np.where(roi[i]==l)
        ymin,ymax=np.min(y),np.max(y)
        xmin,xmax=np.min(x),np.max(x)
        roi2[i,xmin-2:xmin+2,ymin:ymax]=1
        roi2[i,xmax-2:xmax+2,ymin:ymax]=1
        roi2[i,xmin:xmax,ymin-2:ymin+2]=1
        roi2[i,xmin:xmax,ymax-2:ymax+2]=1
        i+=1
        box = [xmin,xmax, ymin, ymax]
    return box, roi2, roi, labels[1:]





jpg=plt.imread('ADE_train_00018279.jpg')
png = plt.imread('ADE_train_00018279_seg.png')
fig,ax = plt.subplots(3)
ax[0].imshow(jpg)
ax[1].imshow(png)
trash=np.zeros(png.shape)
ids=np.where((png[:,:,1]==0.2509804))
(trash[png[:,:,1]==0.2509804])=[0,1,0]
(trash[png[:,:,0]==0])+=[1,0,0]
(trash[png[:,:,2]==0])+=[0,0,1]
trash=np.sum(trash,axis=-1)
trash[trash<3]=0
trash[trash==3]=1
ax[2].imshow(trash.astype('uint8'), cmap='gray')

import scipy as sc
from scipy import ndimage
label_im, nb_labels = ndimage.label(trash)

box, boxes, filled,nlabels=get_box(label_im)
fig2,ax2=plt.subplots(len(nlabels))
for n in range(nlabels.max()):
    ax2[n].imshow(boxes[n],cmap='gray')
plt.show()

