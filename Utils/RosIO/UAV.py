import rospy
from geometry_msgs.msg import PoseStamped,TwistStamped
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
import numpy as np

class UAV():
    def __init__(self):
        self.name = "/uav" + "1"
        self.control_msg = self.name + '/command/pose'
        self.control_vel_msg = self.name + '/command/twist'
        self.camera_msg = self.name + '/camera/rgb/image_raw'
        self.depthCamera_msg = self.name + '/camera/depth/image_raw'
        self.pub = rospy.Publisher(self.control_msg, PoseStamped, queue_size=1)
        self.PoseSub = rospy.Subscriber(self.name + '/ground_truth_to_tf/pose', PoseStamped, self.getPos)
        self.sp_x = 0  # setpoints
        self.sp_y = 0
        self.sp_z = 0
        self.pose = PoseStamped()
        self.controller = PoseStamped()
        self.controller.header.frame_id = self.name.strip('/') + '/world'
        #rospy.Subscriber(self.camera_msg, Image, self.ImageGet)
        #rospy.Subscriber(self.depthCamera_msg, Image, self.DepthGet)

    def getPos(self, Pos):
        self.pose = Pos

    def returnPosToParent(self):
        return self.pose.pose.position.x,self.pose.pose.position.y

    def pub_control(self):
        self.controller.pose.position.x = self.sp_x
        self.controller.pose.position.y = self.sp_y
        self.controller.pose.position.z = self.sp_z
        self.pub.publish(self.controller)

    def SetPose(self, x=None, y=None, z=None, yaw=None):
        if x is not None:
            self.sp_x = x
        if y is not None:
            self.sp_y = y
        if z is not None:
            self.sp_z = z

    # def ImageGet(self, raw_image):
    #     frame = CvBridge.imgmsg_to_cv2(raw_image, "bgr8")
    #     # frame=cv2.resize(frame,(300,300))
    #     frame = np.array(frame, dtype='uint8')
    #     frame = self.ImageProcess(frame)
    #     self.camera_image = frame
    #     self.image_process_rate = rospy.Rate(30)
    #     self.image_process_rate.sleep()
    #
    # def DepthGet(self, raw_depth):
    #     frame = self.cv_bridge.imgmsg_to_cv2(raw_depth)
    #     frame = np.array(frame, dtype='uint8')
    #     frame = self.DepthProcess(frame)
    #     self.camera_depth = frame