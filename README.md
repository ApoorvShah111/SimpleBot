# SimpleBot
This repository holds the work space with the package called Robot. 
To run the gazebo version-

          $ roscd Robot
          $ roslaunch Robot gazebo.launch
          
To control the robot, in a different terminal:

          $ rosrun teleop_twist_keyboard teleop_twist_keyboard.py
          
To run the rviz version-

          $ roscd Robot
          $ roslaunch Robot display.launch model:=urdf/trial.urdf          
