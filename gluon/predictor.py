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
net = gcv.model_zoo.get_model('ssd_512_mobilenet1.0_custom', classes=classes, pretrained_base=False)
net.load_parameters('ssd_512_mobilenet1.0_trash_2fail.params')
x, image = gcv.data.transforms.presets.ssd.load_test('ADE_train_00012920.jpg', 512)
cid, score, bbox = net(x)
ax = viz.plot_bbox(image, bbox[0], score[0], cid[0], class_names=classes)
plt.show()

