#Projectile motion combined with friction after landing on a surface
#Final Project PHY 111, Dr. Abbott
#Written in Python with the VPython library extension
#Joshua Naughton - Spring 2011

#This tells Python that this program uses functions from the VPython library.
#All of the hard work of animating objects has been pre-packaged by the authors of VPython.
from visual import *

#This sets the parameters for the simulation window and where the camera starts.
scene = display(height=800, width=800, range=100, center=(70,40,0))

#These two lines create the puck and the floor, and define their properties
puck = cylinder(pos=(0,0,0), axis=(0,2,0), radius=2, color=color.green)
floor = box(pos=(50,-1,1), size=(250,2,50), color=(0.7,0.5,0.3))

#Designates a section of the screen where text information will be shown
infobox = label(pos=(20,60,0), height=10, box=0)

#Free-body force diagram of the puck, this creates the arrow graphics
#Initially set to 0 length, will be updated as motion begins
arrow_pos_y = arrow(pos=(120,80,0), axis=(0,0,0), shaftwidth=2, fixedwidth=True, color=color.red)
arrow_neg_y = arrow(pos=(120,80,0), axis=(0,0,0), shaftwidth=2, fixedwidth=True, color=color.red)
arrow_neg_x = arrow(pos=(120,80,0), axis=(0,0,0), shaftwidth=2, fixedwidth=True, color=color.red)

#These are grey x and y-axis lines under the free-body diagram area
xaxis = curve(pos=[(110,80,0), (130,80,0)], color=(0.5,0.5,0.5))
yaxis = curve(pos=[(120,80,0), (120,90,0)], color=(0.5,0.5,0.5))

#Setting the initial values for the puck, its motion will be updated in a moment
puck.velocity = vector(0,0,0)
puck.acceleration = vector(0,0,0)
puck.mass = 1

#Setting the initial acceleration sources
accel_Gravity = vector(0,-9.8,0)
accel_Normal = vector(0,0,0)
accel_KFrict = vector(0,0,0)

coeff_KFrict = 0.45 #Coefficient of kinetic friction

#Setting initial forces involved in motion
force_Gravity = puck.mass * accel_Gravity
force_Normal = vector(0,0,0)
force_KFrict = vector(0,0,0)

#Setting up the projectile launch
shot_speed = 25 #initial speed
shot_angle = 30 #angle of projectile motion
shot_radian = shot_angle * (pi/180) #convert to radians, Python handles angles in radians

shot_velocity = vector(0,0,0) #intialize variable to zero, updated immediately after
shot_velocity.x = shot_speed * cos(shot_radian) #calculate x-component of initial projectile velocity
shot_velocity.y = shot_speed * sin(shot_radian) #calculate y-component of initial projectile velocity
shot_velocity.z = 0 #this simulation is two-dimensional

#Assign calculated values above to the puck object
puck.velocity.x = shot_velocity.x
puck.velocity.y = shot_velocity.y
puck.velocity.z = 0

#Assign acceleration components to the puck object
puck.acceleration.x = accel_Gravity.x + accel_Normal.x + accel_KFrict.x
puck.acceleration.y = accel_Gravity.y + accel_Normal.y + accel_KFrict.y
puck.acceleration.z = 0

#Set time to start at 0 seconds and set the interval at 1/100th of a second.
time = 0
delta_t = 0.01

#Begin the actual motion loop, everything below continues to run in a loop
#repeatedly until "stopped = True" is triggered, which has certain requirements
#described below.
stopped = False
while not stopped:
    
    #Setting the rate is how many times this loop can run per second. If
    #you do not limit the rate, computers calculate the simulation so quickly
    #you won't actually see anything happen. By setting it at 100 times per second
    #and using a delta_t value of 0.01, this creates an essentially real-time simulation
    rate(100)

    #Each time the loop repeats, it takes the previous time and adds 0.01s to it. This
    #value is used only for display purposes in the infobox.
    time = time + delta_t

    #Motion equation for velocity, updated every 0.01s.
    puck.velocity.x = puck.velocity.x + puck.acceleration.x * delta_t
    puck.velocity.y = puck.velocity.y + puck.acceleration.y * delta_t

    #Motion equation for position, updated every 0.01s.
    puck.pos.x = puck.pos.x + puck.velocity.x * delta_t + 0.5 * puck.acceleration.x * delta_t**2
    puck.pos.y = puck.pos.y + puck.velocity.y * delta_t + 0.5 * puck.acceleration.y * delta_t**2

    #Free-body arrows are now updated to show acting forces as the loop progresses,
    #I increased their size by a factor of 3 for display purposes.
    arrow_neg_y.axis.y = 3 * force_Gravity.y
    arrow_pos_y.axis.y = 3 * force_Normal.y
    arrow_neg_x.axis.x = 3 * -force_KFrict.x

    #Once per loop, the section below checks to see if the puck has hit the ground
    #and if it has, runs the code that is nested underneath it. If the puck has not
    #touched the ground, this entire section is ignored.
    if puck.pos.y <= 0:
        
        #This just ensures the puck is on the surface exactly
        puck.pos.y = 0
        puck.velocity.y = 0

        #Since the puck is on the surface, the normal force and friction now influence it
        force_Normal.y = -force_Gravity.y
        force_KFrict.x = coeff_KFrict * force_Normal.y

        #Calculate the accelerations caused by each new force
        accel_Normal.y = force_Normal.y / puck.mass
        accel_KFrict.x = force_KFrict.x / puck.mass

        #Update the component accelerations of the puck
        puck.acceleration.x = accel_Gravity.x + accel_Normal.x - accel_KFrict.x
        puck.acceleration.y = accel_Gravity.y + accel_Normal.y + accel_KFrict.y

    #Once per loop, this section checks to see if the velocity of the puck has
    #come to a near stop (less than or equal to 0.02 m/s), if it has, the code below
    #sets "stopped = True" which terminates the loop cycle, and then sets the puck's velocity
    #to zero to stop the animation. It also removes the kinetic force free-body arrow, so that
    #only gravity and normal are displayed and are at equilibrium. If the puck is going any faster
    #than 0.02 m/s, this section is ignored. This step is necessary to prevent the puck from
    #reversing direction as the velocity goes negative.
    if puck.velocity.x <= 0.02:
        stopped = True
        puck.velocity = (0,0,0)
        puck.acceleration = (0,0,0)
        arrow_neg_x.axis.x = 0
        
    #Once per loop, this section below updates the infobox area with relevant information
    info = "Real-time information:\n"
    info += "Time: "+str(time) + " sec" + "\n"
    info += "Position: (x, y, z): " + str(puck.pos) + " m" + "\n"
    info += "Velocity (x, y, z): " + str(puck.velocity) + " m/s" + "\n"
    info += "Net Acceleration (x, y, z): " + str(puck.acceleration) + " m/s/s" + "\n"
    infobox.text = info
    
