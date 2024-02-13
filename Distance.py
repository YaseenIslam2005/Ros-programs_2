#!/usr/bin/python3

import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
import sys
from tf.transformations import euler_from_quaternion

class subsciber():

    def __init__(self):
        
         rospy.init_node("subsciber")
         args = rospy.myargv(argv=sys.argv)
         global distance_1
         global angle 
         angle = float(args[1])
         distance_1 = float(args[2])

         self.pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
         #rospy.Subscriber("joy",Joy,self.callback)
         rospy.Subscriber("odom",Odometry,self.rotary)
         rospy.Subscriber("odom",Odometry,self.distance)
         rospy.loginfo("node has been started")
         self.tw = Twist()
         
   

    # convert quaternion to eular angle 
    def rotary(self,msg):
        roll = None
        pitch = None 
        global yaw
        orientation_q = msg.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
        #convert radians to degrees 
        yaw = yaw *180/3.14
       # print(yaw)


    def distance(self,msg):
        if yaw <=  angle :
            self.tw.angular.z = 1
            self.pub.publish(self.tw)
        else :
            self.tw.angular.z = 0 
        # if the Robot rotated successfully 
        if (self.tw.angular.z == 0) :
            self.pose_x = msg.pose.pose.position.x
            self.pose_y = msg.pose.pose.position.y 
            
            if self.pose_x <= distance_1 :
                self.tw.linear.x = 1
                self.pub.publish(self.tw)
            else :
                self.tw.linear.x = 0
                self.pub.publish(self.tw)

            rospy.loginfo(self.pose_x)

if __name__=='__main__':
     try: 
          pub = subsciber()
         # pub.callback()
          rospy.spin()
     except rospy.ROSInterruptException:
          pass
