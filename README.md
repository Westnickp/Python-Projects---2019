# PythonCode
These are some of the python scripts that I've written that use tkinter to form an interface.

nbodysim.py is an N-Body gravity simulation. It spawns around 100 objects with random velocities, then steps forward in time as they exert gravity on each other. I use a symplectic euler method for the acceleration-velocity-position integration, and there is some force softening if the objects get too close to each other so that the program does not crash or send them off to infinity. 

pong.py is just a simple game of pong. The player controls the right paddle with the up and down arrow keys, and a computer moves on the left. It doesn't keep score, but it will reset if someone scores. If a match is lasting too long, it will also enter a "sudden death mode" where the paddles will approach the middle. 
