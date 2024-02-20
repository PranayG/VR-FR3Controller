import time

import mujoco
import mujoco.viewer
import mediapy as media
import matplotlib.pyplot as plt
import numpy as np
import pickle


model= mujoco.MjModel.from_xml_path("world.xml")
data = mujoco.MjData(model)

# target = np.array(
# [ 0.13356409 ,0.01067754, -0.01287296, -0.0694974 , -0.00348183,  0.46568362,
#  -0.06095309])

q_track = []

with mujoco.viewer.launch_passive(model, data) as viewer:

    # Close the viewer automatically after 30 wall-seconds.
    start = time.time()
    viewer.sync()
    render = True
    viewer.cam.distance = 3.0
    viewer.cam.azimuth = 90
    viewer.cam.elevation = -45
    viewer.cam.lookat[:] = np.array([0.0, -0.25, 0.824])
    model.opt.gravity[2] =0

    Kp = 10.0
    Kd = 3.0
    kTolerance = 1e-2

    with open('q.pkl', 'rb') as file: 
    
    # Call load method to deserialze 
        myvar = pickle.load(file) 

        joint_values = [data[0] for data in myvar]
        timestamps = [data[1] for data in myvar]

        q_leader = joint_values[0]
        # print("Leader\t",q_leader)

    start = time.time()

    while viewer.is_running() and time.time() - start < 1:
        step_start = time.time()
        viewer.sync()

        q_follower = data.qpos[:7].copy()
        dq_follower = data.qvel[:7].copy()

        print("Leader\t",q_leader)
        print("Follower\t",q_follower)


        kNorm = np.abs(q_leader - q_follower)
        
        print("kNorm",kNorm)

        if np.all(kNorm) < kTolerance:
            print("ROBOTS ARE ALIGNED")

        else: 
            print("ROBOTS ARE NOT ALIGNED\t")
            print("GOING TO ALIGN MODE\t")

            

#         error = target - q
#         print("Error \t" , error)
#         # error_norm = np.linalg.norm(error)
#     # mj_step can be replaced with code that also evaluates
#     # a policy and applies a control signal before stepping the physics.
#         mujoco.mj_step(model, data)

#     # # Pick up changes to the physics state, apply perturbations, update options from GUI.
#         viewer.sync()
#         # print(data.qpos[:7])
#         tau = Kp * error + Kd * (0 - dq)
#         data.ctrl[:7] = tau
#         time.sleep(2e-5)
#         pose = data.qpos[:7].copy()
#         q_track.append([pose,time.time()-start])

# # print(q_track)

# with open('q_track.pkl', 'wb') as file:
#     pickle.dump(q_track, file)


# with open('q_track.pkl', 'rb') as file: 
    
# # Call load method to deserialze 
#     myvar = pickle.load(file) 

#     # print(myvar[0][0])
#     # plt.plot(myvar[])  
#     # print(myvar[len(myvar)-1])
#     # Extracting joint values and timestamps
#     joint_values = [data[0] for data in myvar]
#     timestamps = [data[1] for data in myvar]

#     # Plot each joint value against its corresponding timestamp
#     for i in range(len(joint_values[0])):
#         joint_values_i = [joints[i] for joints in joint_values]
#         plt.plot(timestamps, joint_values_i, label=f'Joint {i+1}')

#     print(joint_values[len(myvar)-1])



#     # Adding labels and legend
#     plt.xlabel('Timestamp')
#     plt.ylabel('Joint Value')
#     plt.title('Joint Values vs. Timestamp')
#     plt.legend()
#     plt.grid(True)

#     # Show the plot
#     plt.show()
