import cv2
import rospy
import time

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import String

bridge = CvBridge()

def callback(data):
    rospy.sleep(rospy.Duration(1,0))
    try:
        img = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError, e:
        print e
        return None
    else:
        cv2.imwrite('fetch.jpeg', img)

def im_watcher():
    rospy.init_node('im_watcher', anonymous=True)
    rospy.Subscriber("/head_camera/rgb/image_raw", Image, callback)
    rospy.spin()
    #rate = rospy.Rate(0.2)
    #rate.sleep()

if __name__ == '__main__':
    im_watcher()
