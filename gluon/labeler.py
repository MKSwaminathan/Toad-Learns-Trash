import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from gluoncv import utils
import os
import sys
import zipfile
import mxnet as mx
import scipy
from scipy import ndimage

# def label_trash(png, name):
#    trash = np.zeros(png.shape)
#    ids = np.where((png[:, :, 1] == 0.2509804))
#    (trash[png[:, :, 1] == 0.2509804]) = [0, 1, 0]
#    (trash[png[:, :, 0] == 0]) += [1, 0, 0]
#    (trash[png[:, :, 2] == 0]) += [0, 0, 1]
#    trash = np.sum(trash, axis=-1)
#    trash[trash < 3] = 0
#    trash[trash == 3] = 1
#    #labels = np.unique(png)
#    roi = np.zeros((png.shape[0], png.shape[1]))
#    #roi2 = np.zeros((png.shape[0], png.shape[1]))
#    i = 0
#    # for l in labels[1:]:
#    l = 1
#    slice_x, slice_y = ndimage.find_objects(trash)# == l)[0]
#    #roi[i] = png[slice_x, slice_y]
#    roi[slice_x, slice_y] = l
#    x, y = np.where(roi == l)
#    ymin, ymax = np.min(y), np.max(y)
#    xmin, xmax = np.min(x), np.max(x)
#    write = (0, (xmin+xmax)/2/png.shape[0], (ymin+ymax)/2/png.shape[1],
#             (xmax-xmin)/png.shape[0], (ymax-ymin)/png.shape[1])
#    st = '%i %g %g %g %g' % write
#    print(name, st)
#    #os.system('echo %s >> data/trash/%name.txt' % st)
#    # roi2, roi, labels[1:]
#    # return box, img.shape[0], png.shape[1], labels[1:]
#    fi=open('data/trash/'+name+'.txt','w+')
#    fi.write(st)
#    fi.close()
#    return trash,write


def label_trash(im_path):  # name):
    #img = plt.imread('data/trash/'+name+'.jpg')
    #png = plt.imread('data/trash_seg/'+name+'_seg.png')
    png = plt.imread(im_path)
    trash = np.zeros(png.shape)
    ids = np.where((png[:, :, 1] == 0.2509804))
    (trash[png[:, :, 1] == 0.2509804]) = [0, 1, 0]
    (trash[png[:, :, 0] == 0]) += [1, 0, 0]
    (trash[png[:, :, 2] == 0]) += [0, 0, 1]
    trash = np.sum(trash, axis=-1)
    trash[trash < 3] = 0
    trash[trash == 3] = 1
    labeled, num_cans = ndimage.label(trash)
    boxes = []
    for i in np.unique(labeled)[1:]:
        ylims, xlims = np.where(labeled == i)
        # We expect all bounding boxes follow this format: (xmin, ymin, xmax, ymax)
        boxes.append([xlims.min(), ylims.min(), xlims.max(), ylims.max()])
    return boxes


def write_line(img_path, im_shape, boxes, ids, idx):
    h, w, c = im_shape
    # for header, we use minimal length 2, plus width and height
    # with A: 4, B: 5, C: width, D: height
    A, B, C, D = 4, 5, w, h
    # concat id and bboxes
    labels = np.hstack((ids.reshape(-1, 1), boxes)).astype('float')
    # normalized bboxes (recommanded)
    labels[:, (1, 3)] /= float(w)
    labels[:, (2, 4)] /= float(h)
    # flatten
    labels = labels.flatten().tolist()
    str_idx = [str(idx)]
    str_header = [str(x) for x in [A, B, C, D]]
    str_labels = [str(x) for x in labels]
    str_path = [img_path]
    line = '\t'.join(str_idx + str_header + str_labels + str_path) + '\n'
    return line


#  idx = 0
#  with open('val.lst', 'w') as fw:
#      for f in os.listdir('data/trash'):
#          if not f[-3:] == 'jpg':
#              continue
#          f=f[:-4]
#          img_path = 'data/trash/' + f + '.jpg'
#          img = plt.imread(img_path)
#          img_seg_path = 'data/trash_seg/' + f + '_seg.png'
#          all_boxes = label_trash(img_seg_path)
#          #all_ids = [0 for i in range(len(all_boxes))]
#          all_ids=np.repeat(0,len(all_boxes))
#          img_shape = img.shape
#          line = write_line(img_path, img_shape, all_boxes, all_ids, idx)
#          print(line)
#          fw.write(line)
#          idx += 1
#  #    name = f[:-8]
#  #    label_trash(name)

#ran im2rec

from gluoncv.data import LstDetection
from gluoncv.data import RecordFileDetection
lst_dataset = LstDetection('val.lst', root=os.path.expanduser('.'))
record_dataset = RecordFileDetection('val.rec', coord_normalized=True)

def test(n):
    print('length:', len(lst_dataset))
    first_img = lst_dataset[n][0]
    print('image shape:', first_img.shape)
    print('Label example:')
    print(lst_dataset[n][1])
    print("GluonCV swaps bounding boxes to columns 0-3 by default")
    
    
    
    
    # we expect same results from LstDetection
    print('length:', len(record_dataset))
    first_img = record_dataset[n][0]
    print('image shape:', first_img.shape)
    print('Label example:')
    print(record_dataset[n][1])
    ax = utils.viz.plot_bbox(first_img, record_dataset[n][1][:,:-1], labels=record_dataset[n][1][:,-1], class_names=np.repeat('trash',len(record_dataset[n][1])))
