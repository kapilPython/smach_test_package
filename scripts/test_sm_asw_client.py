#!/usr/bin/env python
import rospy
from actionlib import SimpleActionClient
from smach_test_package.msg import testAction,testGoal

def active():
    rospy.loginfo('goal became active')

def res(state,result):
    rospy.loginfo(str(result))

def fdbck(feedback):
    rospy.loginfo(str(feedback.feedback))

if __name__ == "__main__":
    rospy.init_node('test_smach_asw_client_node')
    cl = SimpleActionClient('test_smach_action_server',testAction)
    cl.wait_for_server()
    tg = testGoal()
    tg.goal.header.frame_id = 'map'
    tg.goal.header.stamp = rospy.Time().now()
    tg.chargingTime = 10.0
    cl.send_goal(tg,active_cb=active,done_cb=res,feedback_cb=fdbck)
    rospy.loginfo('Goal sent')
    cl.wait_for_result() 