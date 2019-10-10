import rosbag

from opencv import cv2
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

from pprint import pprint

bridge = CvBridge()

filename = 'example_rosbag_H3'
read_bag = rosbag.Bag('/data/'+filename+'.bag')
write_bag = rosbag.Bag('/data/'+filename+'_annotated.bag','w')

try:
    i = -1
    for topic, msg, t in read_bag.read_messages():
        i = i+1
        unix_timestamp = t.to_sec()

        pprint(msg)

        try:
            img = bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            print(e)

        h, w = np.shape(img)

        # org
        org = (np.floor(h/4), np.floor(3/8*w))

        # font
        fontFace = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1

        # Blue color in BGR
        color = (255, 0, 0)

        cv2.putText(img, str(unix_timestamp), org, fontFace, fontScale, color)

        if i == 0:
            cv2.imshow('Annotated image', img)

        new_msg = bridge.cv2_to_imgmsg(img, "bgr8")

        write_bag.write(topic, t, new_msg)

finally:
    read_bag.close()
    write_bag.close()