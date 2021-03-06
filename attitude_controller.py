#!/usr/bin/env python

'''
This python file runs a ROS-node of name attitude_control which controls the roll pitch and yaw angles of the eDrone.
This node publishes and subsribes the following topics:
        PUBLICATIONS            SUBSCRIPTIONS
        /roll_error             /pid_tuning_altitude
        /pitch_error            /pid_tuning_pitch
        /yaw_error              /pid_tuning_roll
        /edrone/pwm             /edrone/imu/data
                                /edrone/drone_command

Rather than using different variables, use list. eg : self.setpoint = [1,2,3], where index corresponds to x,y,z ...rather than defining self.x_setpoint = 1, self.y_setpoint = 2
CODE MODULARITY AND TECHNIQUES MENTIONED LIKE THIS WILL HELP YOU GAINING MORE MARKS WHILE CODE EVALUATION.
'''

# Importing the required libraries

from vitarana_drone.msg import *
from pid_tune.msg import PidTune
from sensor_msgs.msg import Imu, LaserScan
from std_msgs.msg import Float32
import rospy
import time
import tf


class Edrone():
    """docstring for Edrone"""

    def __init__(self):
        # initializing ros node with name drone_control
        rospy.init_node('attitude_controller')

        # This corresponds to your current orientation of eDrone in quaternion format. This value must be updated each time in your imu callback
        # [x,y,z,w]
        self.drone_orientation_quaternion = [0.0, 0.0, 0.0, 0.0]

        # This corresponds to your current orientation of eDrone converted in euler angles form.
        # [r,p,y]
        self.drone_orientation_euler = [0.0, 0.0, 0.0]

        # This is the setpoint that will be received from the drone_command in the range from 1000 to 2000
        # [r_setpoint, p_setpoint, y_setpoint]
        self.setpoint_cmd = [0.0, 0.0, 0.0, 0.0]

        # The setpoint of orientation in euler angles at which you want to stabilize the drone
        # [r_setpoint, p_psetpoint, y_setpoint]
        self.setpoint_euler = [0.0, 0.0, 0.0]

        # Declaring pwm_cmd of message type prop_speed and initializing values
        # Hint: To see the message structure of prop_speed type the following command in the terminal
        # rosmsg show vitarana_drone/prop_speed
        self.rollErrorMsg = Float32()
        self.rollErrorMsg.data = 0
        self.yawErrorMsg = Float32()
        self.yawErrorMsg.data = 0
        self.pitchErrorMsg = Float32()
        self.pitchErrorMsg.data = 0
        self.altitudeErrorMsg = Float32()
        self.altitudeErrorMsg.data = 0

        self.pwm_cmd = prop_speed()
        self.pwm_cmd.prop1 = 0.0
        self.pwm_cmd.prop2 = 0.0
        self.pwm_cmd.prop3 = 0.0
        self.pwm_cmd.prop4 = 0.0
        self.height = 0.0

        # initial setting of Kp, Kd and ki for [roll, pitch, yaw]. eg: self.Kp[2] corresponds to Kp value in yaw axis
        # after tuning and computing corresponding PID parameters, change the parameters
        self.Kp = [0, 0, 0, 0]
        self.Ki = [0, 0, 0, 0]
        self.Kd = [0, 0, 0, 0]
        # -----------------------Add other required variables for pid here ----------------------------------------------
        #
        self.rc = edrone_cmd()
        self.rc.rcRoll = 0.0
        self.rc.rcPitch = 0.0
        self.rc.rcYaw = 0.0

        self.laser = LaserScan()
        self.laser.ranges = 0

        self.error = [0.0, 0.0, 0.0, 0.0]
        self.change_error = [0.0, 0.0, 0.0, 0.0]
        self.sum_error = [0.0, 0.0, 0.0, 0.0]
        self.last_error = [0.0, 0.0, 0.0, 0.0]
        # Hint : Add variables for storing previous errors in each axis, like self.prev_values = [0,0,0] where corresponds to [roll, pitch, yaw]
        #        Add variables for limiting the values like self.max_values = [1024, 1024, 1024, 1024] corresponding to [prop1, prop2, prop3, prop4]
        #                                                   self.min_values = [0, 0, 0, 0] corresponding to [prop1, prop2, prop3, prop4]
        #
        # ----------------------------------------------------------------------------------------------------------

        # # This is the sample time in which you need to run pid. Choose any time which you seem fit. Remember the stimulation step time is 50 ms
        self.sample_time = 0.050  # in seconds

        # Publishing /edrone/pwm, /roll_error, /pitch_error, /yaw_error
        self.pwm_pub = rospy.Publisher('/edrone/pwm', prop_speed, queue_size=1)
        # ------------------------Add other ROS Publishers here-----------------------------------------------------
        self.roll_error = rospy.Publisher(
            '/roll_error', Float32, queue_size=1)
        self.pitch_error = rospy.Publisher(
            '/pitch_error', Float32, queue_size=1)
        self.yaw_error = rospy.Publisher(
            '/yaw_error', Float32, queue_size=1)
        self.altitude_error = rospy.Publisher(
            '/altitude_error', Float32, queue_size=1)
        # -----------------------------------------------------------------------------------------------------------

        # Subscribing to /drone_command, imu/data, /pid_tuning_roll, /pid_tuning_pitch, /pid_tuning_yaw
        rospy.Subscriber('/drone_command', edrone_cmd,
                         self.drone_command_callback)
        rospy.Subscriber('/edrone/range_finder_bottom',
                         LaserScan, self.get_altitude)
        rospy.Subscriber('/edrone/imu/data', Imu, self.imu_callback)
        rospy.Subscriber('/pid_tuning_roll', PidTune, self.roll_set_pid)
        rospy.Subscriber('/pid_tuning_pitch', PidTune, self.pitch_set_pid)
        rospy.Subscriber('/pid_tuning_yaw', PidTune, self.yaw_set_pid)
        rospy.Subscriber('/pid_tuning_altitude',
                         PidTune, self.altitude_set_pid)
       # rospy.Subscriber('/edrone/range_finder_bottom' LaserScan, self.get_altitude)
        # -------------------------Add other ROS Subscribers here----------------------------------------------------
        # ------------------------------------------------------------------------------------------------------------

    # Imu callback function
    # The function gets executed each time when imu publishes /edrone/imu/data

    # Note: The imu publishes various kind of data viz angular velocity, linear acceleration, magnetometer reading (if present),
    # but here we are interested in the orientation which can be calculated by a complex algorithm called filtering which is not in the scope of this task,
    # so for your ease, we have the orientation published directly BUT in quaternion format and not in euler angles.
    # We need to convert the quaternion format to euler angles format to understand the orienataion of the edrone in an easy manner.
    # Hint: To know the message structure of sensor_msgs/Imu, execute the following command in the terminal
    # rosmsg show sensor_msgs/Imu

    def imu_callback(self, msg):

        self.drone_orientation_quaternion[0] = msg.orientation.x
        self.drone_orientation_quaternion[1] = msg.orientation.y
        self.drone_orientation_quaternion[2] = msg.orientation.z
        self.drone_orientation_quaternion[3] = msg.orientation.w

        # --------------------Set the remaining co-ordinates of the drone from msg----------------------------------------------

    def drone_command_callback(self, msg):
        self.setpoint_cmd[0] = msg.rcRoll
        self.setpoint_cmd[1] = msg.rcPitch
        self.setpoint_cmd[2] = msg.rcYaw
        self.setpoint_cmd[3] = msg.rcThrottle
        # ---------------------------------------------------------------------------------------------------------------

    # Callback function for /pid_tuning_roll
    # This function gets executed each time when /tune_pid publishes /pid_tuning_roll
    def roll_set_pid(self, roll):
        # This is just for an example. You can change the ratio/fraction value accordingly
        self.Kp[0] = roll.Kp * 0.06
        self.Ki[0] = roll.Ki * 0.008
        self.Kd[0] = roll.Kd * 0.3

    # ----------------------------Define callback function like roll_set_pid to tune pitch, yaw--------------
    def pitch_set_pid(self, pitch):
        self.Kp[1] = pitch.Kp*0.06
        self.Ki[1] = pitch.Ki*0.008
        self.Kd[1] = pitch.kd*0.3

    def yaw_set_pid(self, yaw):
        self.Kp[2] = yaw.Kp*0.06
        self.Ki[2] = yaw.Ki*0.008
        self.Kd[2] = yaw.Kd*0.3

    def altitude_set_pid(self, altitude):
        self.Kp[3] = altitude.Kp*0.006
        self.Ki[3] = altitude.Ki*0.008
        self.Kd[3] = altitude.Kd*0.3
    # ----------------------------------------------------------------------------------------------------------------------

    def get_altitude(self, range):
        rangeList = []
        for i in range.ranges:
            rangeList.append(i)
        self.height = max(rangeList)

    def pid(self):
        # -----------------------------Write the PID algorithm here--------------------------------------------------------------

        # Steps:
        #   1. Convert the quaternion format of orientation to euler angles
        #   2. Convert the setpoin that is in the range of 1000 to 2000 into angles with the limit from -10 degree to 10 degree in euler angles
        #   3. Compute error in each axis. eg: error[0] = self.setpoint_euler[0] - self.drone_orientation_euler[0], where error[0] corresponds to error in roll...
        #   4. Compute the error (for proportional), change in error (for derivative) and sum of errors (for integral) in each axis. Refer "Understanding PID.pdf" to understand PID equation.
        #   5. Calculate the pid output required for each axis. For eg: calcuate self.out_roll, self.out_pitch, etc.
        #   6. Use this computed output value in the equations to compute the pwm for each propeller. LOOK OUT FOR SIGN (+ or -). EXPERIMENT AND FIND THE CORRECT SIGN
        #   7. Don't run the pid continously. Run the pid only at the a sample time. self.sampletime defined above is for this purpose. THIS IS VERY IMPORTANT.
        #   8. Limit the output value and the final command value between the maximum(0) and minimum(1024)range before publishing. For eg : if self.pwm_cmd.prop1 > self.max_values[1]:
        #                                                                                                                                      self.pwm_cmd.prop1 = self.max_values[1]
        #   8. Update previous errors.eg: self.prev_error[1] = error[1] where index 1 corresponds to that of pitch (eg)
        #   9. Add error_sum to use for integral component

        # Converting quaternion to euler angles
        (self.drone_orientation_euler[0], self.drone_orientation_euler[1], self.drone_orientation_euler[2]) = tf.transformations.euler_from_quaternion(
            [self.drone_orientation_quaternion[0], self.drone_orientation_quaternion[1], self.drone_orientation_quaternion[2], self.drone_orientation_quaternion[3]])

        # Convertng the range from 1000 to 2000 in the range of -10 degree to 10 degree for roll axis
       # current_time=time.time()
       # change_time=current_time-last_time
        self.setpoint_euler[0] = self.setpoint_cmd[0] * 0.02 - 30
        self.setpoint_euler[1] = self.setpoint_cmd[1]*0.02 - 30
        self.setpoint_euler[2] = self.setpoint_cmd[2]*0.02 - 30
        self.throttle = self.setpoint_cmd[3]*1.023-1023

        self.error[0] = self.setpoint_euler[0]-self.drone_orientation_euler[0]
        self.error[1] = self.setpoint_euler[1]-self.drone_orientation_euler[1]
        self.error[2] = self.setpoint_euler[2]-self.drone_orientation_euler[2]
        self.error[3] = 3-self.height

        self.change_error[0] = (self.error[0]-self.last_error[0])*0.05
        self.change_error[1] = (self.error[1]-self.last_error[1])*0.05
        self.change_error[2] = (self.error[2]-self.last_error[2])*0.05
        self.change_error[3] = (self.error[3]-self.last_error[3])*0.05

        self.sum_error[0] += self.error[0]/0.05
        self.sum_error[1] += self.error[1]/0.05
        self.sum_error[2] += self.error[2]/0.05
        self.sum_error[3] += self.error[3]/0.05

        # Complete the equations for pitch and yaw axis
        self.out_roll = self.Kp[0]*self.error[0] + \
            self.Ki[0]*self.sum_error[0]+self.Kd[0]*self.change_error[0]

        self.out_pitch = self.Kp[1]*self.error[1] + \
            self.Ki[1]*self.sum_error[1]+self.Kd[1]*self.change_error[1]

        self.out_yaw = self.Kp[2] * self.error[2] + \
            self.Ki[2] * self.sum_error[2] + self.Kd[2] * self.change_error[2]

        self.out_altitude = self.Kp[3]*self.error[3] + self.Ki[3] * \
            self.sum_error[3]+self.Kd[3]*self.change_error[3]

        self.last_error[0] = self.error[0]
        self.last_error[1] = self.error[1]
        self.last_error[2] = self.error[2]
        self.last_error[3] = self.error[3]

        # self.roll_error.publish(self.out_roll)
        # self.pitch_error.publish(self.out_pitch)
        # self.yaw_error.publish(self.yaw_pitch)

        # Also convert the range of 1000 to 2000 to 0 to 1024 for throttle here itslef

        self.pwm_cmd.prop1 = self.throttle + \
            self.out_roll+self.out_pitch+self.out_yaw
        #
        self.pwm_cmd.prop2 = self.throttle - \
            self.out_roll+self.out_pitch-self.out_yaw
        #
        self.pwm_cmd.prop3 = self.throttle + \
            self.out_roll-self.out_pitch-self.out_yaw
        #
        self.pwm_cmd.prop4 = self.throttle - \
            self.out_roll-self.out_pitch+self.out_yaw
        #
        self.rollErrorMsg.data = self.error[0]
        self.pitchErrorMsg.data = self.error[1]
        self.yawErrorMsg.data = self.error[2]
        self.altitudeErrorMsg.data = self.error[3]
        #
        #
        #
        # ------------------------------------------------------------------------------------------------------------------------

        self.pwm_pub.publish(self.pwm_cmd)
        self.roll_error.publish(self.rollErrorMsg)
        self.yaw_error.publish(self.pitchErrorMsg)
        self.pitch_error.publish(self.yawErrorMsg)
        self.altitude_error.publish(self.altitudeErrorMsg)


if __name__ == '__main__':

    e_drone = Edrone()
    # specify rate in Hz based upon your desired PID sampling time, i.e. if desired sample time is 33ms specify rate as 30Hz
    r = rospy.Rate(e_drone.sample_time)
    while not rospy.is_shutdown():
        e_drone.pid()
        r.sleep()
