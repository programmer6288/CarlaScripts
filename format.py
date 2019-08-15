from math import sqrt
f = open('v_data_3.txt', 'r')
g = open('velocity_selector.txt', 'w')
lines = f.readlines()
for line in lines:
	line = line.replace('Vector3D(', '')
	line = line.replace(',', '')
	line = line.replace('x=', '')
	line = line.replace('y=', '')
	line = line.replace('z=', '')
	line = line.replace(')', '')
	print(line)
	speed = line.split()
	x, y, z = float(speed[0]), float(speed[1]), float(speed[2])
	g.write(str(sqrt(x*x+y*y+z*z))+'\n')

