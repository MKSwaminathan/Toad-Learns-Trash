import sys
# Need to append path in order to 
# import pyrealsense
sys.path.append('/usr/local/lib/')

import cv2
import time 
import socket
import numpy as np
import mxnet as mx
import gluoncv as gcv
import pyrealsense2 as rs


def apply_brightness_contrast(input_img, brightness = 0, contrast = 0):

    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow

        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()

    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)

        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf

#
# Load the model
#
classes = ['trash']
net = gcv.model_zoo.get_model('ssd_512_mobilenet1.0_custom', classes=classes, pretrained_base=False)
#net.load_parameters('../gluon/ssd_512_mobilenet1.0_trash_backup_2_2_6ep.params')
net.load_parameters('../gluon/ssd_512_mobilenet1.0_trash.params')
# Comnet = denoisingNetwork('dncnn');pile the model for faster speed
net.hybridize()


#
# Configure depth and color streams
#
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 30)
config.enable_stream(rs.stream.infrared, 2, 640, 480, rs.format.y8, 30)

#
# Start streaming
#
pipeline.start(config)

# Params
frame_del = 100

try:

    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        
        # Get two stereo channels 
        nir_lf_frame = frames.get_infrared_frame(1)
        nir_rg_frame = frames.get_infrared_frame(2)
        if not nir_lf_frame or not nir_rg_frame:
            continue
        nir_lf_image = np.asanyarray(nir_lf_frame.get_data())
        nir_rg_image = np.asanyarray(nir_rg_frame.get_data())

        # Stack both images horizontally
        stereo_images = np.hstack((nir_lf_image,nir_rg_image))
    
        # Image pre-processing - Experimentation bench
        cv2.resize(nir_lf_image,(350,240))
        nir_lf_image = cv2.medianBlur(nir_lf_image,1)
        nir_rg_image = cv2.medianBlur(nir_rg_image,1)
        kernel = np.array([0,1,0,1,1,1,0,1,0],dtype=np.uint8)
        nir_lf_image = cv2.erode(nir_lf_image,kernel)
        nir_rg_image = cv2.erode(nir_rg_image,kernel)
        nir_lf_image = apply_brightness_contrast(nir_lf_image,40,20)

        frame_lf = mx.nd.array(cv2.cvtColor(nir_lf_image, cv2.COLOR_BGR2RGB)).astype('uint8')
        frame_rg = mx.nd.array(cv2.cvtColor(nir_rg_image, cv2.COLOR_BGR2RGB)).astype('uint8')


        rgb_nd_lf, frame_lf = gcv.data.transforms.presets.ssd.transform_test(frame_lf, short=512, max_size=700)
        rgb_nd_rg, frame_rg = gcv.data.transforms.presets.ssd.transform_test(frame_rg, short=512, max_size=700)
    
        # Run frame through network
        class_IDs, scores, bounding_boxes = net(rgb_nd_lf)
        class_IDs, scores, bounding_boxes = net(rgb_nd_rg)
        
        # Display the result
        thresh = 0.45
        img_lf = gcv.utils.viz.cv_plot_bbox(frame_lf, bounding_boxes[0], scores[0], class_IDs[0], class_names=net.classes,thresh=thresh)
        img_rg = gcv.utils.viz.cv_plot_bbox(frame_rg, bounding_boxes[0], scores[0], class_IDs[0], class_names=net.classes,thresh=thresh)
    
        # Show images
        cv2.namedWindow('NIR images (left, right)', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('IR Example', np.hstack((img_lf,img_rg)))

        cv2.waitKey(frame_del)
    
finally:

    # Stop streaming
    pipeline.stop()
