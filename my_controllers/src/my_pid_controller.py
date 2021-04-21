#!/usr/bin/env python2

import rospy
import math
from nav_msgs.msg import Odometry
from tf import transformations
from geometry_msgs.msg import Twist, Point


class prop:

    #Robot variables
    global desired
    position = Point()
    global angle
    angle= 0.0
    global s
    s=0
    global desired_angle
    global k_angle
    k_angle=0.5
    global k_distance
    k_distance=0.5

    #precision values
    dist_precision=1
    angle_precision = (math.pi)/180 #1 degree
    global twist_msg
    twist_msg=Twist()


    def move_angle(self):

        #calculating the angle the bot needs to be at
        desired_angle= atan(desired.y-position.y , desired.x-position.x)
        angular_error= desired_angle-angle

        #condition for checking
        if math.fabs(angular_error)>angle_precision:
            twist_msg.angular.z=angular_error* k_angle
            pub.publish(twist_msg)
            print("[",position.x,"],[",position.y,"]")
        else:
            s=1

    def move_position(self):

        #calculating the Error
        distance_error=math.sqrt(math.pow(desired.x-position.x,2)+math.pow(desired.y-position.y,2))

        #calculating the angle the bot needs to be at
        desired_angle= atan(desired.y-position.y , desired.x-position.x)
        angular_error= desired_angle-angle

        #condition for PD
        if (distance_error>dist_precision):
            twist_msg.linear.x= k_distance *distance_error
            pub.publish(twist_msg)
            print("[",position.x,"],[",position.y,"]")
        else:
            s=2
        if math.fabs(angular_error)>angle_precision:
            twist_msg.angular.z=angular_error* k_angle
            pub.publish(twist_msg)
            print("[",position.x,"],[",position.y,"]")
        else:
            s=1

    def ending(self):
        twist_msg.linear.x=0
        twist_msg.angular.y=0
        pub.publish(twist_msg)


def main():
    t=prop()
    #defining the Publisher and Subsciber and making the node
    global pub
    pub= rospy.Publisher('/cmd_vel',twist, queue_size=1)
    global sub
    sub= rospy.Subsciber('/odom', Odometry,clbk_odom)
    rospy.init_node('my_node', anonymous=True)

    #asking the final position of the bot
    desired=Point()
    desired.x=19
    desired.y=5
    desired.z=0

    rate = rospy.Rate(50)
    global twist_msg
    twist_msg=twist()
    twist_msg.linear.y=0.0
    twist_msg.linear.z=0.0
    twist_msg.linear.x=0.0
    twist_msg.angular.y=0.0
    twist_msg.angular.x=0.0
    twist_msg.angular.z=0.0

    #starting the loop
    while not rospy.is_shutdown():

        #checking what the bot has to do
        if s == 0:
            t.move_angle()
        elif s == 1:
            t.move_position()
        elif s == 2:
            t.ending()
        else:
            rospy.logerr("Error its fucked")
            pass
        rate.sleep()


    if __name__ == '__main__':
        begin()


def clbk_odom():
    global position
    position=msg.pose.pose.position
    quaternion=(msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,msg.pose.pose.orientation.z,msg.pose.pose.orientation.w)
    euler = transformations.euler_from_quaternion(quaternion)
    angle=euler[2]
