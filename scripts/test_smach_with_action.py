#!/usr/bin/env python
import rospy
from smach_test_package.all_states import getStateMachine
from smach_test_package.msg import testAction,testFeedback,testResult
from actionlib import SimpleActionServer
from threading import Thread


class TestServerClass():
    def __init__(self):
        self.smach_action_server = SimpleActionServer('test_smach_action_server',testAction,
                                                      execute_cb=self.execute_cb,auto_start=False)
        self.smach_action_server.start()

    def execute_cb(self,goal):
        sm = getStateMachine()
        sm.userdata.action_goal = goal
        smach_thread = Thread(target=sm.execute)
        smach_thread.start()
        while(smach_thread.is_alive()):
            self.smach_action_server.publish_feedback(testFeedback(str(sm.get_active_states())))
            rospy.loginfo(sm.get_active_states())
            rospy.sleep(rospy.Duration(1.0))
        self.smach_action_server.set_succeeded(testResult("The Task Got Completed"))

if __name__ == "__main__":
    rospy.init_node('test_smach_action_node')
    TestServerClass()
    rospy.spin()