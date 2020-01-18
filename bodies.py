import numpy as np
import matplotlib.pyplot as plt
import pynput.mouse as ms
import tkinter
from tkinter import *
import time

	
def haku():
	name=[]
	m=[]
	x0=[]
	y0=[]
	vx0=[]
	vy0=[]
	colors=[]
	file = open('input.dat','r')
	tiedot = file.readlines()
	for rivi in tiedot:
		osarivi = rivi.split()
		name.append(osarivi[0])
		m.append(float(osarivi[1]))
		x0.append(float(osarivi[2]))
		y0.append(-1*float(osarivi[3]))
		vx0.append(float(osarivi[4]))
		vy0.append(-1*float(osarivi[5]))	# - sign to get the origo effectively at bottom 
		colors.append(osarivi[6])
	file.close()					# left
	return name,m,x0,y0,vx0,vy0,colors


def Accel(G,m2,x1,x2,y1,y2,r):				#From newton gravitational law
	ax = -G*m2/(r**3)*(x2-x1)			#The mass accelerated isn't needed here
	ay = -G*m2/(r**3)*(y2-y1)
	return ax,ay

class body():
	def __init__(self,name,mass,x,y,vx,vy,root,canvas,color):	#creating the bodies and setting 
		self.name = name				#properties
		self.m = mass
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy
		canvas.pack()
		self.pic = canvas.create_oval(500+self.x, 500+self.y, 
		500+self.x, 500+self.y, width = 10*np.log10(10*self.m),outline=color)
								#drawing the bodies
	def move(self,bodies,i,N,G,canvas):		#defining the movement of a body while
		dt = 0.001				#supposing constant acceleration it time
		for j in range(N):			#interval dt
			if j == i:			#mass does not effect itself
				continue
			else:
				r = ((self.y-bodies[j].y)**2+(self.x-bodies[j].x)**2)**(1/2)
				ax,ay = Accel(G,bodies[j].m,bodies[j].x,self.x,bodies[j].y,self.y,r)
				dx = 1/2*ax*dt**2+self.vx*dt	#the main calucations to determinate
				dy = 1/2*ay*dt**2+self.vy*dt	#position and velocity of a body j
				self.vx = ax*dt+self.vx
				self.vy = ay*dt+self.vy
				self.x = self.x + dx
				self.y = self.y + dy
				canvas.move(self.pic,dx,dy)	#moving the body
				
				
		
def animation(N,canvas,bodies):				#the "main" part of the program
		G = 1000				#Gravitational constant
		name,m,x,y,vx,vy,colors = haku()		#"unnecessary" repetation of search
		dt = 0.001				#time interval
		Ek = []
		Ep = []
		for i in range(N):			#calculating total energies
			Epot = 0
			Ek.append(1/2*((vx[i])**2+(vy[i])**2))
			for j in range(N):
				if j==i:
					continue
				else:
					rij = ((y[i]-y[j])**2+(x[i]-x[j])**2)**(1/2)
					Epot = Epot - G*m[j]/rij
			Ep.append(Epot)
		for i in range(N):
			E = Ek[i] + Ep[i]
			print(E)
			if E > 0:		#calculating if body i is bounded or not
				print('Body',bodies[i].name,'not bounded')
		while True:
			time.sleep(0.01)	#the main animation
			for i in range(N):
				bodies[i].move(bodies,i,N,G,canvas)			
			canvas.update()

				
	

def main():
	name,m,x,y,vx,vy,colors = haku()		# getting the initial data
	bodies = []				# define a tuple to collect the bodies
	N = len(name)
	root = Tk()				#canvas making
	canvas = Canvas(root, width=1000, height = 1000)
	for i in range(N):
		bodies.append(body(name[i],m[i],x[i],y[i],vx[i],vy[i],root,canvas,colors[i]))
		#expanding the list with new bodies and drawing them in to the canvas
	root.after(0,animation(N,canvas,bodies))#Making calcuations to determinate 
						#new positions and drawing them
	
	
			
if __name__ == "__main__":
    main()
