import numpy as np
import tkinter as tk
import time
root = tk.Tk()
root.title('N-Body Simulation!')
root.resizable(0,0)
root.wm_attributes("-topmost",1)
canvas = tk.Canvas(root, width=1400, height=750, bd=0, highlightthickness=0)
canvas.pack()
root.update()
## Calculating the value of the universal gravitational constant
G = 6.674*(10**(-11)) # m^3/kg/s^2

# Function that converts from m^3/kg/s^2 to Au^3/Masses of Earth/yr^2
def convert(a):
    # 1 Au^3 = (1.496*(10**11))**3 m
    # 1 Me = 5.972*(10**24) kg
    # 1 yr^2 = (3.154*(10**7))**2 s^2
    Au3 = (1.496*(10**11))**3
    Me = 5.972*(10**24)
    Yr2 = (3.154*(10**7))**2

    converted = a/Au3*Me*Yr2

    return converted

G = convert(G)

def km(x): # Convert to AU
    x = x/(1.496*10**8)
    return x

## Create the mass objects:
class mass(object):
    def __init__(self, mass, xvel=0, yvel=0, randomvel=True, randompos=True, color='blue'):
        self.mass = mass
        self.zoom = 10
        if randompos==True:
            self.xpos = np.random.uniform(-10, 10)
            self.ypos = np.random.uniform(-((10**2 - self.xpos**2)**.5),
                                          ((10**2 - self.xpos**2)**.5))
        else:
            self.xpos = randompos[0]
            self.ypos = randompos[1]
        if xvel == 0 and yvel == 0:
            self.xvel = np.random.uniform(-70,70)
            self.yvel = np.random.uniform(-70,70)
        else:
            self.xvel = xvel
            self.yvel = yvel
        self.canvas = canvas
        self.id = canvas.create_oval(0,0,10,10,fill=color)
        self.canvas.move(self.id,245+self.zoom*self.xpos,245-self.zoom*self.ypos)
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()

    def distance(self, other_mass):
        total_distance = ((self.xpos-other_mass.xpos)**2+(self.ypos-other_mass.ypos)**2)**.5
        if total_distance < 10**-5:
            total_distance = 10**-5
        return total_distance

    def xaccel(self, other_mass):
        ax = -100*G*other_mass.mass*(self.xpos-other_mass.xpos)/self.distance(other_mass)**1.5
        return ax

    def yaccel(self, other_mass):
        ay = -100*G*other_mass.mass*(self.ypos-other_mass.ypos)/self.distance(other_mass)**1.5
        return ay

    def net_accel(self, list_of_masses):
        netax = 0
        netay = 0
        for i in list_of_masses:
            if i != self:
                netax += self.xaccel(i)
                netay += self.yaccel(i)
        self.ax = netax
        self.ay = netay
        return

    def new_pos(self, h):
        oldx = self.xpos
        oldy = self.ypos
        self.xpos += h*self.xvel
        self.ypos += h*self.yvel
        deltax = self.xpos - oldx
        deltay = oldy - self.ypos
        self.canvas.move(self.id, self.zoom*deltax, self.zoom*deltay)
        return

    def new_vel(self, h):
        self.xvel += h*self.ax
        self.yvel += h*self.ay
        return

def create_masses(N, size=1000):
    masses = []
    linmomx = 0
    linmomy = 0
    for i in range(N):
        masses.append(mass(size))
    for i in masses:
        linmomx += i.mass*i.xvel
        linmomy += i.mass*i.yvel
    masses.append(mass(size*10, -linmomx/size/10, -linmomy/size/10))


    return masses

def binarystar(size=10000):
    mass1 = mass(size, xvel=-.1, yvel=15, randompos=[5,0])
    mass2 = mass(size-10, xvel=.1, yvel=-12, randompos=[-5,0])
    masses = [mass1, mass2]

    return masses

def timestep(list_of_masses, h=0.01):
    for mass in list_of_masses:
        mass.new_pos(h)
    for mass in list_of_masses:
        mass.net_accel(list_of_masses)
        mass.new_vel(h)

def usermoveup(list_of_masses):
    for mass in list_of_masses:
        mass.canvas.move(mass.id, 0, -50)
def usermovedown(list_of_masses):
    for mass in list_of_masses:
        mass.canvas.move(mass.id, 0, 50)
def usermoveleft(list_of_masses):
    for mass in list_of_masses:
        mass.canvas.move(mass.id, -50, 0)
def usermoveright(list_of_masses):
    for mass in list_of_masses:
        mass.canvas.move(mass.id, 50, 0)
# def zoomin(list_of_masses):
#     for i in list_of_masses:
#         i.canvas.move(i.id, -i.zoom*i.xpos*.5, i.zoom*i.ypos*.5)
#         i.zoom *= .5
# def zoomaway(list_of_masses):
#     for i in list_of_masses:
#         i.canvas.move(i.id, i.zoom*i.xpos*2, -i.zoom*i.ypos*2)
#         i.zoom *= 2

breakevent = False
def breaktheevent(event):
    global breakevent
    breakevent = True
masses = create_masses(100, 700)
canvas.bind_all('<KeyPress-Left>', lambda event, masses=masses: usermoveleft(masses))
canvas.bind_all('<KeyPress-Right>', lambda event, masses=masses: usermoveright(masses))
canvas.bind_all('<KeyPress-Down>', lambda event, masses=masses: usermovedown(masses))
canvas.bind_all('<KeyPress-Up>', lambda event, masses=masses: usermoveup(masses))
# canvas.bind_all('i', lambda event, masses=masses: zoomin(masses))
# canvas.bind_all('o', lambda event, masses=masses: zoomaway(masses))
canvas.bind_all('q', breaktheevent)

KE = tk.StringVar()
KECounter = 0
ke = 0
kineticenergy = tk.Label(root, textvariable=KE).pack(side=tk.LEFT)
def kineticenergyfunc(list_of_masses):
    global ke, KECounter
    for i in list_of_masses:
        ke += i.mass*(i.xvel**2 + i.yvel**2)
    KECounter += 1
    KE.set('Average KE since start: %d' % (ke/KECounter))

while True:
    timestep(masses, 0.01)
    root.update_idletasks()
    root.update()
    kineticenergyfunc(masses)
    if breakevent:
        print('Quit')
        break

quit()