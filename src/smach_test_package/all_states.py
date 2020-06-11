import smach
import rospy


class WaitForRequest(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['reqRcvd'],
                             input_keys=['move_goal'],output_keys=['send_goal'])
    
    def execute(self,userdata):
        if(userdata.move_goal.goal.header.frame_id == 'map' and userdata.move_goal.chargingTime != 0):
            userdata.send_goal = userdata.move_goal
            rospy.loginfo("In State WaitForRequest")
            return 'reqRcvd'


class Move(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['destRchd'],input_keys=['move_goal'])
        self.rosrate = rospy.Rate(0.2)

    def execute(self,userdata):
        rospy.loginfo(userdata.move_goal.goal)
        rospy.loginfo("In State Move")
        self.rosrate.sleep()
        return 'destRchd'

class ReconSocket(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['onConnect'])
        self.rosrate = rospy.Rate(0.2)

    def execute(self,userdata):
        rospy.loginfo("In State ReconSocket")
        self.rosrate.sleep()
        return 'onConnect'

class PlugIn(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['onDisconnect'],input_keys=['move_goal'],output_keys=['output_result'])

    def execute(self,userdata):
        rosrate = rospy.Rate(1.0/userdata.move_goal.chargingTime)
        rospy.loginfo("In State PlugIn")
        rosrate.sleep()
        userdata.output_result = "Task Completed"
        return 'onDisconnect'

def getStateMachine():
    sm = smach.StateMachine(outcomes=['PLUGOUT','ABORTED','PREEMPTED'],
                            input_keys=['action_goal'],
                            output_keys=['result'])
    with sm:
        sm.add('WAITFORREQUEST',WaitForRequest(),
                transitions={
                    'reqRcvd' : 'MOVE'
                },
                remapping={
                    'send_goal': 'wfr_data',
                    'move_goal': 'action_goal'
                })
        sm.add('MOVE',Move(),
                transitions={
                    'destRchd' : 'RECONSOCKET'
                },
                remapping={
                    'move_goal' : 'wfr_data'
                })
        sm.add('RECONSOCKET',ReconSocket(),
                transitions={
                    'onConnect' : 'PLUGIN'
                })
        sm.add('PLUGIN',PlugIn(),
                transitions={
                    'onDisconnect' : 'PLUGOUT'
                },
                remapping={
                    'move_goal' : 'action_goal',
                    'output_result' : 'result'
                })
    
    return sm