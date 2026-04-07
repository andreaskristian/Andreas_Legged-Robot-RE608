import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ==============================
# PARAMETER ROBOT
# ==============================

L1 = 10
L2 = 7

# ==============================
# TRAJECTORY SUDUT JOINT
# Gerakan dibuat lebih kompleks
# ==============================

t = np.linspace(0,40,1500)

theta1_traj = 0.9*np.sin(0.4*t) + 0.4*np.cos(0.9*t)
theta2_traj = 0.8*np.cos(0.6*t) + 0.5*np.sin(1.2*t)

# ==============================
# SETUP PLOT
# ==============================

fig, ax = plt.subplots()

ax.set_xlim(-20,20)
ax.set_ylim(-20,20)
ax.set_aspect('equal')
ax.grid()

# workspace robot
circle1 = plt.Circle((0,0),L1+L2,fill=False,linestyle="--",color='gray')
circle2 = plt.Circle((0,0),abs(L1-L2),fill=False,linestyle="--",color='gray')

ax.add_patch(circle1)
ax.add_patch(circle2)

# robot arm
line, = ax.plot([],[],'o-',lw=4,color='blue')

# joint marker
joint, = ax.plot([],[],'ko',markersize=6)

# trajectory end effector
trajectory, = ax.plot([],[],'r-',lw=1)

# posisi info dibawah robot
text = ax.text(
    0,-18,'',
    fontsize=11,
    ha='center',
    bbox=dict(facecolor='white',alpha=0.8)
)

x_history=[]
y_history=[]

max_trail = 500

# ==============================
# UPDATE ANIMATION
# ==============================

def update(i):

    global x_history,y_history

    theta1 = theta1_traj[i]
    theta2 = theta2_traj[i]

    # ==============================
    # FORWARD KINEMATICS
    # ==============================

    x1 = L1*np.cos(theta1)
    y1 = L1*np.sin(theta1)

    x2 = x1 + L2*np.cos(theta1+theta2)
    y2 = y1 + L2*np.sin(theta1+theta2)

    # robot arm
    line.set_data([0,x1,x2],[0,y1,y2])

    # joint marker
    joint.set_data([0,x1,x2],[0,y1,y2])

    # trajectory line
    x_history.append(x2)
    y_history.append(y2)

    if len(x_history) > max_trail:
        x_history.pop(0)
        y_history.pop(0)

    trajectory.set_data(x_history,y_history)

    # info posisi end effector
    text.set_text(
        f"End Effector Position\n"
        f"X = {x2:.2f}\n"
        f"Y = {y2:.2f}"
    )

    return line,joint,trajectory,text

# ==============================
# ANIMATION
# ==============================

ani = FuncAnimation(
    fig,
    update,
    frames=len(theta1_traj),
    interval=30,
    repeat=True
)

plt.title("2-DOF Robot Arm - Forward Kinematics Simulation")

plt.xlabel("X Position")
plt.ylabel("Y Position")

plt.show()