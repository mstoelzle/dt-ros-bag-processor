import rosbag

import cv2
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

from pprint import pprint

bridge = CvBridge()

filename = '2019-10-09-12-09-35'
read_bag = rosbag.Bag('/data/'+filename+'.bag')
write_bag = rosbag.Bag('/data/'+filename+'_annotated.bag','w')

try:
    i = -1
    for topic, msg, t in read_bag.read_messages():
        i = i+1
        unix_timestamp = t.to_sec()

        if msg._type == 'sensor_msgs/CompressedImage':
            try:
                img = bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
            except CvBridgeError as e:
                print(e)

            h = img.shape[0]
            w = img.shape[1]

            # org
            org = (int(np.floor(1/8.0*w)),int(np.floor(h/8.0)))

            # font
            fontFace = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 0.8

            # Blue color in BGR
            color = (255, 0, 0)

            cv2.putText(img, str(unix_timestamp), org, fontFace, fontScale, color)

            if i == 0:
                cv2.imwrite('/data/'+filename+'_0.png', img)

            try:
                new_msg = bridge.cv2_to_compressed_imgmsg(img, "jpg")
            except CvBridgeError as e:
                print(e)

            #new_msg.header = msg.header

            write_bag.write(topic, new_msg, t)

finally:
    read_bag.close()
    write_bag.close()