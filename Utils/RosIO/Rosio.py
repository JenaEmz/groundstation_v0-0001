import rospy
import threading
from Utils.RosIO.UAV import UAV
from Utils.EnableMotors import *
class RosIO():
    def __init__(self):
        rospy.init_node("baka")
        self.uav = UAV()
        self.Motorservice = rospy.ServiceProxy("/uav1/enable_motors", EnableMotors)
        self.rosthread = threading.Thread(target = self.rosnode_init)
        self.rosthread.start()

    def rosnode_init(self):

        while not rospy.is_shutdown():
            self.uav.pub_control()
            rospy.sleep(0.1)
        rospy.spin()