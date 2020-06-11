#!/usr/bin/env python
import rospy
import smach
from smach_ros import ActionServerWrapper
from smach_test_package.all_states import getStateMachine
from smach_test_package.msg import testAction


if __name__ == "__main__":

    rospy.init_node('test_smach_asw_node')

    sm = getStateMachine()

    asw = ActionServerWrapper('test_smach_action_server',testAction,
                                wrapped_container=sm,
                                succeeded_outcomes=['PLUGOUT'],
                                aborted_outcomes = ['ABORTED'],
                                preempted_outcomes = ['PREEMPTED'],
                                goal_key= 'action_goal',
                                result_key= 'action_result' 
                             )
    asw.run_server()
    rospy.spin()