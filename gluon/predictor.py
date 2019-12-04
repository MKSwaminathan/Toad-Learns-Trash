import time
from matplotlib import pyplot as plt
import numpy as np
import mxnet as mx
from mxnet import autograd, gluon
import gluoncv as gcv
from gluoncv.utils import download, viz

classes = ['trash']  # only one foreground class here
test_url = 'https://seeclickfix.com/files/issue_images/0104/6669/image.jpg'
download(test_url, 'trash_test.jpg')
net = gcv.model_zoo.get_model(
    'ssd_512_mobilenet1.0_custom', classes=classes, pretrained_base=False)
net.load_parameters('ssd_512_mobilenet1.0_trash_backup_2_2_6ep.params')
#x, image = gcv.data.transforms.presets.ssd.load_test('trash_test.jpg', 512)
x, image = gcv.data.transforms.presets.ssd.load_test(
    ['trash_test.jpg', 'ade2.jpg', 'ADE_train_00012920.jpg'], 512)
for i in range(3):
    cid, score, bbox = net(x[i])
    #ax = viz.plot_bbox(image[i], bbox[0], score[0], cid[0],
    ax = viz.plot_bbox(image[i], bbox[0], score[0], cid[0],
                       thresh=np.max(score), class_names=classes)
    plt.show()
