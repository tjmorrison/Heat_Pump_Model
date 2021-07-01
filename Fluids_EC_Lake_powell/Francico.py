#import numpy as np

gamma = 62.4 # specific weight of water lbf/ft^3 at assumed temperature of 15 degrees C
depth = 429.78 # current depth of lake in ft
t = 75 # degrees slope of gate
pi = 3.14
d = t*pi/180 # conversion from radians to degrees
x = np.sin(d) # actual sine value
Height = [5,10,15,20] # height of gate
W = 5 # assumed width of gate
Area = 0
cnt =0;
for i in Height:
    Area = W*i
    h = depth-i/2
    cnt = cnt+1
    Fr[i]= gamma*h*x*Area
    print(Fr)