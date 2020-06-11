# smach_test_package
# This Package gives you an example code to wrap a smach state machine with an action server

For installing the package go to cd ~/catkin_ws/src
and execute 'git clone https://github.com/kapilPython/smach_test_package.git'

There are mainly three scripts
test_sm_asw_client.py - a simple action server towards smach state machine
test_sm_asw_server.py - an action server wrapper to wrap a smach state machine
test_smach_with_action.py - a normal action server to start a specific state machine on user request

src/all_states.py contains an example state machine with all the states defined

Before running anything go to folder scripts and execute chmod +x .

To run smach state machine with action service wrapper follow below steps on different terminals:-
1. roscore
2. rosrun smach_test_package test_sm_asw_server.py
3. rosrun smach_test_package test_sm_asw_client.py

To run smach state machine with action service server follow below steps on different terminals:-
1. roscore
2. rosrun smach_test_package test_smach_with_action.py
3. rosrun smach_test_package test_sm_asw_client.py