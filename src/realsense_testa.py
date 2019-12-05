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


#
# Establish TCP socket connection
#
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
print (host)
print ('Enter port number: ')
read_port = input()
port = int(read_port)
s.bind((host, port))
s.listen(5)


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
    # Poll for connection
    while True:
        try:
            client, addr = s.accept()
            print ('Got connection from', addr)
            connection_verification = 'Connected to Realsense'
            client.send(connection_verification.encode())
            print('Exiting connecter')
            break
        except:
            next

    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()


        # Get two stereo channels 
        nir_lf_frame = frames.get_infrared_frame(1)
        nir_rg_frame = frames.get_infrared_frame(2)
        if not nir_lf_frame or not nir_rg_frame:
            continue
        
        # Convert images to numpy arrays
        nir_lf_image = np.asanyarray(nir_lf_frame.get_data())
        nir_rg_image = np.asanyarray(nir_rg_frame.get_data())

        # Stack both images horizontally
        stereo_images = np.hstack((nir_lf_image,nir_rg_image))
 
    
        # Image pre-processing
        frame_lf = mx.nd.array(cv2.cvtColor(nir_lf_image, cv2.COLOR_BGR2RGB)).astype('uint8')
        frame_rg = mx.nd.array(cv2.cvtColor(nir_rg_image, cv2.COLOR_BGR2RGB)).astype('uint8')

        rgb_nd_lf, frame_lf = gcv.data.transforms.presets.ssd.transform_test(frame_lf, short=512, max_size=700)
        rgb_nd_rg, frame_rg = gcv.data.transforms.presets.ssd.transform_test(frame_rg, short=512, max_size=700)
    

        # Run frame through network
        class_IDs_lf, scores_lf, bounding_boxes_lf = net(rgb_nd_lf)
        class_IDs_rg, scores_rg, bounding_boxes_rg = net(rgb_nd_rg)
       

        # Display the result
        thresh = 0.45
        img_lf = gcv.utils.viz.cv_plot_bbox(frame_lf, bounding_boxes_lf[0], scores_lf[0], class_IDs_lf[0], class_names=net.classes,thresh=thresh)
        img_rg = gcv.utils.viz.cv_plot_bbox(frame_rg, bounding_boxes_rg[0], scores_rg[0], class_IDs_rg[0], class_names=net.classes,thresh=thresh)
    
        
        # Get coordinates
        trash_bound = np.r_[-1,-1,-1,-1]
        scores_lf = scores_lf.asnumpy()
        scores_rg = scores_rg.asnumpy()
        
        if((scores_lf[0,0,0] >= thresh) and (scores_rg[0,0,0]>=thresh)):
            trash_bound = bounding_boxes_lf[0,0].asnumpy()
       
        X = 512
        Y = 700
        y = 0.5*(trash_bound[0] + trash_bound[2])
        x = 0.5*(trash_bound[1] + trash_bound[3])
        angle = -1

        if y/Y >= 0 and y/Y < 0.2:
            angle = 0
        if y/Y >=0.2 and y/Y < 0.4:
            angle = 1
        if y/Y >= 0.4 and y/Y < 0.6:
            angle = 2
        if y/Y >= 0.6 and y/Y < 0.8:
            angle = 3
        if y/Y >= 0.8 and y/Y <= 1:
            angle = 4
        #print (angle)
   
        # Find depth
        bound_lf = bounding_boxes_lf[0,0].asnumpy()
        bound_rg = bounding_boxes_rg[0,0].asnumpy()
        x_lf_min = bound_lf[1]
        x_lf_max = bound_lf[3]

        x_rg_min = bound_rg[1]
        x_rg_max = bound_rg[3]

        x_lf = 0.5*(x_lf_min + x_lf_max)
        x_rg = 0.5*(x_rg_min + x_rg_max)

        depth = -1
        focal_length = 0.00193
        cam_dist = 0.05
        dx = 100*abs(x_lf - x_rg)
        print('x_lf: ',x_lf)
        print('x_rg: ',x_rg)
        print('dx: ',dx)

        multiplier = 10**8
        depth = multiplier*(cam_dist*focal_length)/dx
        orig_depth=2*.05*.00193/np.absolute(x_lf-x_rg)
        print('orig_depth',orig_depth)
        
        print('depth: ',int(depth))

        # Send info to raspi
        msg = 'START '+ str(int(angle)) + ' ' + str(int(depth)) + ' EOM'
        client.send(msg.encode())
        
        # Show images
        cv2.namedWindow('NIR images (left, right)', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('IR Example', np.hstack((img_lf,img_rg)))

        cv2.waitKey(frame_del)
    
finally:

    # Stop streaming
    pipeline.stop()
