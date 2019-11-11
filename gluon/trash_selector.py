import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from gluoncv import utils
import os
import sys
import zipfile
import mxnet as mx


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
        box = [xmin, ymin, xmax, ymax]
    # roi2, roi, labels[1:]
    return box, img.shape[0], labeled_img.shape[1], labels[1:]


def get_trash():
    outpath = os.path.abspath('')+'/trash_images'
    os.mkdir(outpath)
    urls = np.genfromtxt('trash_urls.txt', delimiter='\n', dtype='str')
    for url in urls:
        utils.download(url, path=outpath)
    lpath = os.path.abspath('')+'/trash_labels'
    os.mkdir(lpath)
    #trash_boxes = np.zeros((len(urls), 4), dtype='str')
    with open('val.lst', 'w') as fw:
        for i in range(len(urls)):
            img = plt.imread(outpath+'/'+urls[i])
            img = label_trash(img)
            #trash_boxes[i, :], w, h, ids = get_box(img)
            trash_box[i, :], w, h, ids = get_box(img)
            A, B, C, D = 4, 5, w, h
            #trash_boxes[i, 1:-1:2] /= flot(w)
            #trash_boxes[i, 2:-1:2] /= float(h)
            trash_box[1:-1:2] /= flot(w)
            trash_box[2:-1:2] /= float(h)
            labels = np.hstack((ids.reshape(-1, 1), trash_box)).astype('float')
            str_idx = [str(i)]
            str_header = [str(x) for x in [A, B, C, D]]
            str_labels = [str(x) for x in labels]
            str_path = [outpath+'/'+urls[i]]
            line = '\t'.join(str_idx + str_header + str_labels + str_path) + '\n'
            fw.write(line)

    #np.save(lpath+'/trash_boxes', trash_boxes)
    return trash_boxes


#with open('val.lst', 'w') as fw:
#    for i in range(4):
#        line = write_line('dog.jpg', img.shape, all_boxes, all_ids, i)
#        print(line)
#        fw.write(line)
#
#
#def write_line(img_path, im_shape, boxes, ids, idx):
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

    import scipy as sc
    from scipy import ndimage
    label_im, nb_labels = ndimage.label(trash)

    box, boxes, filled, nlabels = get_box(label_im)
    fig2, ax2 = plt.subplots(len(nlabels))
    for n in range(nlabels.max()):
        ax2[n].imshow(boxes[n], cmap='gray')
    plt.show()
