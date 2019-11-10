import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def count_obj(img):
    labels=np.arange(2,1000).astype('int')
    copy_img=img.copy().astype('int')
    count=-1
    for n in range(img.shape[1]):
        if img[0,n]==0:
            a=5
        if(img[0,n]==1):
            if(copy_img[0,n-1]>0):
                copy_img[0,n]=copy_img[0,n-1].max()
                continue
            if(img[0,n-1]==0):
                count+=1
                copy_img[0,n]=labels[count]
    for m in range(1,img.shape[0]):
        for n in range(0,img.shape[1]):
            if img[m,n]==0:
                a=5
            if img[m,n]==1:
                if(np.any(copy_img[m-1,n-1:n+2]>1)):
                    copy_img[m,n]=copy_img[m-1,n-1:n+2][copy_img[m-1,n-1:n+2]!=0].max()
                    if copy_img[m,n-1]>copy_img[m,n]:
                        copy_img[m,n-1]=copy_img[m,n]
                if(copy_img[m,n-1]>1):
                    copy_img[m,n]=copy_img[m,n-1]
                if((np.all(copy_img[m-1,n-1:n+2]==0)) and (copy_img[m,n-1]==0)):
                    count+=1
                    copy_img[m,n]=labels[count]
    return copy_img, count

#d
def get_centers(img,eroded_img):
    with_centers=img.copy().astype('int')
    for item in np.unique(labeled_trash)[2:]:
        ylims,xlims=np.where(eroded_img==item)
        c_x=np.mean(xlims).astype('int')
        c_y=np.mean(ylims).astype('int')
        with_centers[c_y-1:c_y+2,c_x-1:c_x+2]=0
    return with_centers

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
        box = [xmin,xmax, ymin, ymax  ]
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
np.count_nonzero(trash)
ax[2].imshow(trash.astype('uint8'), cmap='gray')

edges_y = np.diff(trash,axis=0)[:,:-1]
edges_x = np.diff(trash,axis=1)[:-1,:]
edges=edges_x+edges_y

import scipy as sc
from scipy import ndimage
label_im, nb_labels = ndimage.label(trash)

box, boxes, filled,nlabels=get_box(label_im)
fig2,ax2=plt.subplots(len(nlabels))
for n in range(nlabels.max()):
    ax2[n].imshow(boxes[n],cmap='gray')
plt.show()

