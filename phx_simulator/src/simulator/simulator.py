import sys
import time
from math import sin, cos, atan2
import numpy as np
# from simulator.navdata import Navdata

import matplotlib.pyplot as plt
from pylab import *
from mpl_toolkits.mplot3d import Axes3D


class Simulator(object):



    def __init__(self, drone, controller):
        self.drone = drone
        self.controller = controller
        self.step_count = 0
        self.start_time = 0  # in secs
        self.end_time = 1  # in secs
        self.dt = 0.005
        self.x = []
        self.y = []
        self.z = []
        self.roll = []
        self.pitch = []
        self.yaw = []
        self.cmd1 = []
        self.cmd2 = []
        self.cmd3 = []
        self.cmd4 = []
        self.e_yaw = []
        self.e_x = []
        self.e_y = []
        self.e_z = []
        self.roll_des = []
        self.pitch_des = []
        self.yaw_des = []

    def reset(self):
        # TODO: reset all states
        self.theta_desired = np.array([[0.0], [0.0], [0.0]])
        self.thetadot_desired = np.array([[0.0], [0.0], [0.0]])
        self.x_desired = np.array([[0.0], [0.0], [0.0]])
        self.xdot_desired = np.array([[0.0], [0.0], [0.0]])
        self.drone.x = np.array([[0.0], [0.0], [0.0]])
        self.drone.xdot = np.array([[0.0], [0.0], [0.0]])
        self.drone.xdoubledot = np.array([[0.0], [0.0], [0.0]])
        self.drone.theta = np.array([[0.0], [0.0], [0.0]])
        self.drone.omega = np.array([[0.0], [0.0], [0.0]])
        self.drone.thetadot = np.array([[0.0], [0.0], [0.0]])

    def get_drone_pose(self):
        return [self.drone.x.item(0),
                self.drone.x.item(1),
                self.drone.x.item(2),
                self.drone.theta.item(0),
                self.drone.theta.item(1),
                self.drone.theta.item(2)]

    def set_input(self, sim_input):
        self.xdot_desired[0] = sim_input[0]
        self.xdot_desired[1] = sim_input[1]
        self.thetadot_desired[2] = sim_input[2]
        self.xdot_desired[2] = sim_input[3]
        self.xdot_desired = np.dot(self.drone.yaw_rotation(),
                                   self.xdot_desired)

    def set_input_world(self, lin_vel, yaw_vel):
        self.xdot_desired[0] = lin_vel[0]
        self.xdot_desired[1] = lin_vel[1]
        self.xdot_desired[2] = lin_vel[2]
        self.thetadot_desired[2] = yaw_vel

    def simulate_step(self, t, dt):
        self.step_count += 1

        inputCurrents, acc = self.controller.calculate_control_command(dt, self.xdot_desired, self.thetadot_desired.item(2))
        # calculate current angular velocity in body frame
        omega = self.drone.omega
        torques_thrust = self.drone.torques_thrust(inputCurrents)
        # calculate the resulting linear acceleration
        linear_acceleration = self.linear_acceleration(torques_thrust[3],
                                                       self.drone.theta,
                                                       self.drone.xdot)
        # calculate resulting angular acceleration
        omegadot = self.angular_acceleration(torques_thrust[0:3, 0], omega)
        # integrate up new angular velocity in the body frame
        omega = omega + dt * omegadot

        # normalize roll, pitch, yaw
        omega[0] = atan2(sin(omega[0]), cos(omega[0]))
        omega[1] = atan2(sin(omega[1]), cos(omega[1]))
        omega[2] = atan2(sin(omega[2]), cos(omega[2]))

        self.drone.omega = omega
        # calculate roll, pitch, yaw velocities
        self.drone.thetadot = np.dot(self.drone.angle_rotation_to_world().transpose(), omega)
        # calculate new roll, pitch, yaw angles
        self.drone.theta = self.drone.theta + dt * self.drone.thetadot

        self.drone.xdoubledot = linear_acceleration
        # calculate new linear drone speed
        self.drone.xdot = self.drone.xdot + dt * linear_acceleration
        # calculate new drone position
        self.drone.x = self.drone.x + dt * self.drone.xdot

        print("new position", self.drone.x)

        if self.step_count % 50 == 0:  # sample trajectory for plotting
            vel = np.dot(self.rotation(self.drone.theta).transpose(),
                         self.drone.xdot)
            vel = self.drone.xdot

            self.x.append(vel.item(0))
            self.y.append(vel.item(1))
            self.z.append(vel.item(2))

            ang = self.drone.theta

            self.roll.append(ang.item(0))
            self.pitch.append(ang.item(1))
            self.yaw.append(ang.item(2))

            self.cmd1.append(inputCurrents[0] - inputCurrents[2])
            self.cmd2.append(inputCurrents[1] - inputCurrents[3])
            self.cmd3.append(inputCurrents[0] - inputCurrents[1])
            self.cmd4.append(inputCurrents[3])

            self.roll_des.append(self.theta_desired[0])
            self.pitch_des.append(self.theta_desired[1])
            self.yaw_des.append(self.theta_desired[2])

    def simulate(self, duration):
        """Simulate drone dynamics for a duration."""
        self.end_time = duration
        self.reset()

        # Step through the simulation, updating the drone state.
        t = self.start_time
        fig1 = figure(1)
        fig2 = figure(2)
        fig3 = figure(3)
        fig4 = figure(4)

        while t <= self.end_time:
            self.simulate_step(t, self.dt)
            t += self.dt

            # only plot every
            frac = 5.0 * t + self.dt * 0.1

            if((frac - int(frac)) < (self.dt * 0.5)):
                # ion()
                ###########################################
                plt.figure(1)
                fig1.suptitle('Position x, y, z')
                # ax  = fig1.add_subplot(111, projection='3d')
                # ax.plot(self.x, self.y, self.z)
                # ax.axis([-5, 5, -5, 5])
                # ax.set_zlim3d(-5, 5 )
                # ax.set_xlabel('x')
                # ax.set_ylabel('y')
                # ax.set_zlabel('z')
                # plt.ylim(-1.5, +1.5)
                # plt.xlim(-1.5, +1.5)
                ax_x = fig1.add_subplot(311)
                ax_y = fig1.add_subplot(312)
                ax_z = fig1.add_subplot(313)
                # ax_z.ylim(-2.0, 2)
                ax_x.plot(self.x)
                ax_y.plot(self.y)
                ax_z.plot(self.z)
                draw()
                fig1.show()

                plt.figure(2)
                fig2.suptitle('Position roll, pitch, yaw')
                ax_roll = fig2.add_subplot(311)
                ax_roll.plot(self.roll)
                ax_roll.plot(self.roll_des)
                # ax_roll.legend("des", "act", right)
                ax_pitch = fig2.add_subplot(312, sharey=ax_roll)
                ax_pitch.plot(self.pitch)
                ax_pitch.plot(self.pitch_des)

                ax_yaw = fig2.add_subplot(313, sharey=ax_roll)
                ax_yaw.plot(self.yaw)
                ax_yaw.plot(self.yaw_des)
                draw()
                fig2.show()

                plt.figure(3)
                plt.ylim(-5, +5)
                fig3.suptitle('Errors x, y, z, yaw')
                ax_x = fig3.add_subplot(411)
                ax_x.plot(self.e_x)
                ax_y = fig3.add_subplot(412, sharey=ax_x)
                ax_y.plot(self.e_y)
                ax_z = fig3.add_subplot(413, sharey=ax_x)
                ax_z.plot(self.e_z)
                ax_yaw = fig3.add_subplot(414, sharey=ax_x)
                ax_yaw.plot(self.e_yaw)
                draw()
                fig3.show()

                plt.figure(4)
                plt.ylim(-2, 2)
                fig4.suptitle('Control Commands')
                ax_1 = fig4.add_subplot(411)
                ax_1.plot(self.cmd1)
                ax_2 = fig4.add_subplot(412, sharey=ax_1)
                ax_2.plot(self.cmd2)
                ax_3 = fig4.add_subplot(413, sharey=ax_1)
                ax_3.plot(self.cmd3)
                # ax_4 = fig4.add_subplot(414,sharey=ax_1)
                # ax_4.plot(self.cmd4)
                fig4.show()
                pause(0.1)

    def deg2rad(self, degrees):
        """Convert degrees to radians."""
        return np.array(map(math.radians, degrees))

    def rotation(self, angles):
        """Translate angles to intertial/world frame."""
        phi = angles.item(0)
        theta = angles.item(1)
        psi = angles.item(2)

        c_phi = cos(phi)
        s_phi = sin(phi)
        c_theta = cos(theta)
        s_theta = sin(theta)
        c_psi = cos(psi)
        s_psi = sin(psi)

        R = np.array([[c_psi * c_theta,
                       c_psi * s_theta * s_phi - s_psi * c_phi,
                       c_psi * s_theta * c_phi + s_psi * s_phi],
                      [s_psi * c_theta,
                       s_psi * s_theta * s_phi + c_psi * c_phi,
                       s_psi * s_theta * c_phi - c_psi * s_phi],
                      [-s_theta, c_theta * s_phi, c_theta * c_phi]])

        return R

    def linear_acceleration(self, thrust, angles, xdot):
        """Compute the linear acceleration of the drone resulting from."""
        gravity = np.array([[0], [0], [-self.drone.g]])
        R = self.rotation(angles)

        T = np.dot(R, np.array([[0], [0], [thrust]]))
        F_drag = -self.drone.kd * xdot
        a = gravity + (T + F_drag) / self.drone.m
        return a

    def angular_acceleration(self, torques, omega):
        """Compute the linear acceleration of the drone resulting from."""
        omegaddot = np.dot(self.drone.I_inv,
                           (torques.transpose() - np.cross(omega.transpose(),
                            np.dot(self.drone.I, omega).transpose())).transpose())
        return omegaddot
