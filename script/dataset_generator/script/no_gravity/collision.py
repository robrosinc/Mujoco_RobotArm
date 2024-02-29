import os
import shutil
from tqdm import tqdm

import numpy as np
from mujoco_py import load_model_from_path, MjSim, MjViewer
import mujoco
import time, datetime
import csv
import random
 
from utils import compute

class RobotSimulator:
    def __init__(self, mjcf_path, offset, csv_path):
        self.model = load_model_from_path(mjcf_path)
        self.sim = MjSim(self.model)
        self.viewer = MjViewer(self.sim)
        self.joint_names = ['Continuous_1', 'Continuous_2', 'Continuous_3',
                            'Continuous_4', 'Continuous_5', 'Continuous_6', 'Continuous_7']
        self.joint_indices = [self.model.joint_names.index(name) for name in self.joint_names]

        self.x_desired = [0,0,0]
        self.x_current = [0,0,0]
        self.Kp = 300
        self.Kd_joint = 0.0
        self.Ki = 0.1
        self.integral_error = np.zeros(3)
        self.Kd = 0.0
        self.error = 0
        self.prev_error = 0
        self.dt = 1.0 / 60.0  
        self.angle = np.zeros(len(self.joint_indices))
        self.prev_angles = np.zeros(len(self.joint_indices))

        self.offset = offset

        self.rows = 3
        self.cols = 7

        self.q_prev = [0 for i in range(7)]
        self.tau = None
        self.tau_values = None
        self.q_values = None
        self.marked_positions = []

        self.desired_positions = self.load_desired_positions(csv_path)
        self.current_sequence_index = 0     

        self.create_output_folder()
        self.reset_values()

        # RING for COLLISION

        self.random_step = 0
        self.random_link = None



    def update_ring_pose(self, pos, quat):
        """Update the ring's position and orientation."""
        mocap_id = self.sim.model.body_mocapid[self.sim.model.body_name2id('mocap_ring')]
        self.sim.data.mocap_pos[mocap_id] = pos
        self.sim.data.mocap_quat[mocap_id] = quat

        # physical_id = self.sim.model.body_name2id("physical_ring")
        # self.sim.model.body_pos[physical_id] = pos
        
    def update_physical_ring(self, sim, mocap_body_name, joint_name):
        mocap_id = self.sim.model.body_mocapid[self.sim.model.body_name2id(mocap_body_name)]
        mocap_pos = self.sim.data.mocap_pos[mocap_id]
        mocap_quat = self.sim.data.mocap_quat[mocap_id]

        joint_qpos_addr = self.sim.model.get_joint_qpos_addr(joint_name)
        if isinstance(joint_qpos_addr, tuple):
            start_index = joint_qpos_addr[0]
        else:
            start_index = joint_qpos_addr

        self.sim.data.qpos[start_index:start_index+3] = mocap_pos
        self.sim.data.qpos[start_index+3:start_index+7] = mocap_quat



        self.sim.forward()


    def get_link_pose(self, link_name):
        pos = self.sim.data.get_body_xpos(link_name)
        quat = self.sim.data.get_body_xquat(link_name)
        return pos, quat
    
    def place_ring_at_link(self, link_name):
        """Place the ring at the pose of the specified link."""
        pos, quat = self.get_link_pose(link_name)
        self.update_ring_pose(pos, quat)
        self.update_physical_ring("mocap_ring","physical_ring", "physical_ring_joint")




    def load_desired_positions(self, csv_path):
        """Load desired positions from a CSV file."""
        positions = []
        with open(csv_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header
            for row in reader:
                positions.append([float(row[i]) for i in range(3)]) 
        return positions    

    def write_marker(self):
        FK_position = (f"FK :{float(self.x_current[0]):.2f}, {float(self.x_current[1]):.2f}, {float(self.x_current[2]):.2f}")
        Desired_position = (f"Desired :{float(self.x_desired[0]):.2f}, {float(self.x_desired[1]):.2f}, {float(self.x_desired[2]):.2f}")

        self.viewer.add_marker(pos=(np.array([0,0,0])),
                            label="mujoco orientation", size=np.array([.01, .01, .01]))
        self.viewer.add_marker(pos=([-self.x_current[0], -self.x_current[1], self.x_current[2]]),
                            label=FK_position, size=np.array([.01, .01, .01]), rgba=np.array([1,0,0,1]), type=2)
        self.viewer.add_marker(pos=([-self.x_desired[0], -self.x_desired[1], self.x_desired[2]]),
                            label=Desired_position, size=np.array([.01, .01, .01]), rgba=np.array([0,1,0,1]), type=2)
        
        self.render_trajectory()
        
    def F_calcalator(self, angle):
        self.error = np.array(self.x_desired) - self.x_current
        self.integral_error += self.error * self.dt
        # print("error is :", np.linalg.norm(self.error))

        angle_errors = angle - self.prev_angles
        tau_d = self.Kd_joint * angle_errors / self.dt
        self.prev_angles = angle
        derivative = (self.error - self.prev_error) / self.dt

        F = self.Kp * self.error + self.Ki * self.integral_error # PD, PI control
        # F = self.Kp * error # only PD control
        return F
    
    def add_marker(self, pos):
        position = [-pos[0], -pos[1], pos[2]]
        # print("marker position is :", pos)
        self.viewer.add_marker(pos=position, size=np.array([.01, .01, .01]), rgba=np.array([0,1,0,1]), label="", type=2)

    def render_trajectory(self):
        """
        render all markers in marked_positions
        """
        for pos in self.marked_positions:
            # print("marked position length is : ",len(self.marked_positions))
            self.add_marker(pos)

    def move_robot(self, tau):
        for i, joint_idx in enumerate(self.joint_indices):
            self.sim.data.ctrl[joint_idx] = tau[i]

    def move_robot_to_position(self):
        # self.angle = self.sim.data.qpos.copy()
        self.x_current = compute.compute_xc(self.angle)
        F = self.F_calcalator(self.angle)
        self.prev_error = self.error  
        J = compute.compute_jacobian(self.angle, self.rows, self.cols)
        self.tau = J.T.dot(F) - 100*(self.angle - np.array(self.q_prev)) 

        self.move_robot(self.tau)
        self.write_marker()


    def reset_simulation(self):
        self.sim.reset()

    def reset_values(self):
        self.q_values = [[] for _ in range(7)]
        self.tau_values = [[] for _ in range(7)]

    def save_values(self):
        for i in range(7):
            filename = os.path.join(self.input_data_folder, f"fre_joint_{i+1}.csv")
            with open(filename, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.q_values[i])

        for i in range(7):
            filename = os.path.join(self.target_data_folder, f"fre_joint_{i+1}.csv")
            with open(filename, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.tau_values[i])


    def create_output_folder(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        base_folder = f"../csv/joint_data/temp/{current_time}"
        self.input_data_folder = os.path.join(base_folder, "input_data")
        self.target_data_folder = os.path.join(base_folder, "target_data")
        os.makedirs(self.input_data_folder, exist_ok=True)
        os.makedirs(self.target_data_folder, exist_ok=True)

    def run_simulation(self):
        reached_point = False

        if self.current_sequence_index >= len(self.desired_positions):
            print("All sequences have been simulated.")
            return False  

        start_time = time.time()

        self.x_desired = self.desired_positions[self.current_sequence_index]  # Update desired position
        # self.x_desired = [0.15, -0.15, -0.65] 

        self.current_sequence_index += 1 
        self.reset_values()

        self.random_step = np.random.randint(1000)

        step_count = 0


        while True: 
            step_count += 1

            if step_count == self.random_step:
                link_name = np.random.choice(['link_3', 'link_5'])
                print(link_name)
                print("bump")
                self.place_ring_at_link(link_name)

            current_time = time.time()

            if current_time - start_time > 5:
                if not reached_point:
                    print("3 second passed")
                    return False
                else:
                    break

            self.angle = self.sim.data.qpos.copy() 
            self.angle = self.angle[:7] 
            print(self.angle)
            self.move_robot_to_position()
        
            for i in range(7):
                self.angle[i] = self.angle[i] - self.offset[i]
                self.q_values[i].append(self.angle[i])
                self.tau_values[i].append(self.tau[i])

            self.q_prev = self.angle
            self.sim.step()
            self.viewer.render()

            if np.linalg.norm(self.error) < 0.05:
                print("done")
                reached_point = True
                break 
        
        return True  
            
            
mjcf_path = "/home/robros/model_uncertainty/model/ROBROS/robot/base.xml"
offset = [0,0,0,0,0,0,0]
csv_path = "/home/robros/model_uncertainty/script/visualize_workspace/random_selected_data.csv"

robot_sim = RobotSimulator(mjcf_path, offset,csv_path)

sequence_count = 5000

for sequence_number in tqdm(range(sequence_count), desc="Simulating Sequences"):
    result = robot_sim.run_simulation()
    if result:  # run_simulation에서 True 반환 시에만 save_values 호출
        robot_sim.save_values()
    robot_sim.reset_simulation()