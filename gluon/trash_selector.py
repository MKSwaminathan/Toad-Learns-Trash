import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import gluoncv as gcv
from gluoncv import utils
import os
import sys
import zipfile
import mxnet as mx
import scipy as sc
import scipy.ndimage as ndimage
from gluoncv.data import LstDetection
import scipy as sc
from scipy import ndimage
from gluoncv.data import RecordFileDetection
from gluoncv.utils import download, viz
from mxnet import autograd, gluon


def label_trash(png):
    trash = np.zeros(png.shape)
    ids = np.where((png[:, :, 1] == 0.2509804))
    (trash[png[:, :, 1] == 0.2509804]) = [0, 1, 0]
    (trash[png[:, :, 0] == 0]) += [1, 0, 0]
    (trash[png[:, :, 2] == 0]) += [0, 0, 1]
    trash = np.sum(trash, axis=-1)
    trash[trash < 3] = 0
    trash[trash == 3] = 1
    return trash


def get_box(labeled_img):
    labels = np.unique(labeled_img)
    roi = np.zeros(
        (len(labels[1:]), labeled_img.shape[0], labeled_img.shape[1]))
    roi2 = np.zeros(
        (len(labels[1:]), labeled_img.shape[0], labeled_img.shape[1]))
    i = 0
    for l in labels[1:]:
        slice_x, slice_y = ndimage.find_objects(labeled_img == l)[0]
        #roi[i] = labeled_img[slice_x, slice_y]
        roi[i, slice_x, slice_y] = l
        x, y = np.where(roi[i] == l)
        ymin, ymax = np.min(y), np.max(y)
        xmin, xmax = np.min(x), np.max(x)
        roi2[i, xmin-2:xmin+2, ymin:ymax] = 1
        roi2[i, xmax-2:xmax+2, ymin:ymax] = 1
        roi2[i, xmin:xmax, ymin-2:ymin+2] = 1
        roi2[i, xmin:xmax, ymax-2:ymax+2] = 1
        i += 1
        box = np.array([xmin, ymin, xmax, ymax])
    # roi2, roi, labels[1:]
    # print(labels[1:].shape)
    return box, labeled_img.shape[0], labeled_img.shape[1], labels[1:]


def get_trash():
    outpath = os.path.abspath('')+'/trash_images'
    # os.mkdir(outpath)
    urls = np.genfromtxt('trash_urls.txt', delimiter='\n', dtype='str')[:-1]
    urls = [url for url in urls if 'val' not in url]
    #raw = urls[0:len(urls):2]
    raw = [url for url in urls if 'seg' not in url]
    #seg = urls[1:len(urls):2]
    seg = [url for url in urls if 'seg' in url]
    for ra in raw:
        utils.download(ra, path='trash_images/'+ra[-22:])
    for se in seg:
        utils.download(se, path='trash_images/'+se[-26:])
    #lpath = os.path.abspath('')+'/trash_labels'
    # os.mkdir(lpath)
    #trash_boxes = np.zeros((len(urls), 4), dtype='str')
    with open('val.lst', 'w') as fw:
        for i in range(len(raw)):
            img = plt.imread('trash_images'+'/'+raw[i][-22:])
            l_img = plt.imread('trash_images'+'/'+seg[i][-26:])
            print(img.shape)
            l_img = label_trash(l_img)
            #trash_boxes[i, :], w, h, ids = get_box(img)
            trash_box, h, w, ids = get_box(l_img)
            trash_box = trash_box.astype('float')
            A, B, C, D = 4, 5, w, h
            print(w,h)
            #trash_boxes[i, 1:-1:2] /= flot(w)
            #trash_boxes[i, 2:-1:2] /= float(h)
            print(trash_box)
            trash_box[0:len(trash_box):2] = (trash_box[0:len(trash_box):2])/float(h)
            trash_box[1:len(trash_box):2] = (trash_box[1:len(trash_box):2])/float(w)
            print(trash_box)
            labels = np.hstack((ids, trash_box)).astype('float')
            print(trash_box)
            str_idx = [str(i)]
            str_header = [str(x) for x in [A, B, C, D]]
            str_labels = [str(x) for x in labels]
            str_path = [outpath+'/'+raw[i][-22:]]
            line = '\t'.join(str_idx + str_header +
                             str_labels + str_path) + '\n'
            fw.write(line)
    #np.save(lpath+'/trash_boxes', trash_boxes)
    # return trash_boxes


# with open('val.lst', 'w') as fw:
#    for i in range(4):
#        line = write_line('dog.jpg', img.shape, all_boxes, all_ids, i)
#        print(line)
#        fw.write(line)
#
#
# def write_line(img_path, im_shape, boxes, ids, idx):
#    h, w, c = im_shape
#    # for header, we use minimal length 2, plus width and height
#    # with A: 4, B: 5, C: width, D: height
#    A = 4
#    B = 5
#    C = w
#    D = h
#    # concat id and bboxes
#    labels = np.hstack((ids.reshape(-1, 1), boxes)).astype('float')
#    # normalized bboxes (recommanded)
#    labels[:, (1, 3)] /= float(w)
#    labels[:, (2, 4)] /= float(h)
#    # flatten
#    labels = labels.flatten().tolist()
#    str_idx = [str(idx)]
#    str_header = [str(x) for x in [A, B, C, D]]
#    str_labels = [str(x) for x in labels]
#    str_path = [img_path]
#    line = '\t'.join(str_idx + str_header + str_labels + str_path) + '\n'
#    return line


def demo_selector():
    jpg = plt.imread('ADE_train_00018279.jpg')
    png = plt.imread('ADE_train_00018279_seg.png')
    fig, ax = plt.subplots(3)
    ax[0].imshow(jpg)
    ax[1].imshow(png)
    trash = np.zeros(png.shape)
    ids = np.where((png[:, :, 1] == 0.2509804))
    (trash[png[:, :, 1] == 0.2509804]) = [0, 1, 0]
    (trash[png[:, :, 0] == 0]) += [1, 0, 0]
    (trash[png[:, :, 2] == 0]) += [0, 0, 1]
    trash = np.sum(trash, axis=-1)
    trash[trash < 3] = 0
    trash[trash == 3] = 1
    ax[2].imshow(trash.astype('uint8'), cmap='gray')

    label_im, nb_labels = ndimage.label(trash)

    box, boxes, filled, nlabels = get_box(label_im)
    fig2, ax2 = plt.subplots(len(nlabels))
    for n in range(nlabels.max()):
        ax2[n].imshow(boxes[n], cmap='gray')
    plt.show()


# if __name__ == "__main__":
def regen():
    get_trash()
    lst_dataset = LstDetection('val.lst', root='trash_images/')
    print('length:', len(lst_dataset))
    os.system('python3 im2rec.py \'val.lst\' \'trash_images/\' --pass-through --pack-label')
    print('generated rec')
 
def test_box(n):
    #get_trash()
    #lst_dataset = LstDetection('val.lst', root='trash_images/')
    #print('length:', len(lst_dataset))
    #os.system('python3 im2rec.py \'val.lst\' \'trash_images/\' --pass-through --pack-label')
    #print('generated rec')
    record_dataset = RecordFileDetection('val.rec', coord_normalized=True)
    
    # we expect same results from LstDetection
    print('length:', len(record_dataset))
    first_img = record_dataset[n][0]
    print('image shape:', first_img.shape)
    print('Label example:')
    print(record_dataset[n][1])
    
    dataset = gcv.data.RecordFileDetection('val.rec')
    classes = ['trash']  # only one foreground class here
    image, label = dataset[n]
    #label=label.astype('int')
    print('label:', label)
    # display image and label
    ax = viz.plot_bbox(
        image, bboxes=label[:, :4], labels=label[:, 4:5], class_names=classes, absolute_coordinates=True)
    plt.plot()
    plt.show()
