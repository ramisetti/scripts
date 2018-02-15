#!/usr/bin/env python

#### This script contains different implementations to fit (x,y) coordinates to a circle and estimate center xc,yc and radius R values

import numpy as np

#### Reference: Samuel M Thomas, Y.T Chan, A simple approach for the estimation of circular arc center and its radius, Computer Vision, Graphics, and Image Processing, Volume 45, Issue 3, 1989, Pages 362-370, https://doi.org/10.1016/0734-189X(89)90088-1.
# this function is similar to circle_fitting_alg
def circle_fitting(x,y):
	N=len(x)
	p1=np.sum(x)
	p2=np.sum(x*x)
	p3=np.sum(x*y)
	p4=np.sum(y)
	p5=np.sum(y*y)
	p6=np.sum(x*x*x)
	p7=np.sum(x*y*y)
	p8=np.sum(y*y*y)
	p9=np.sum(x*x*y)

	a1 = 2 * (p1*p1 - N*p2)
	b1 = 2 * (p1*p4 - N*p3)
	a2 = b1
	b2 = 2 * (p4*p4 - N*p5)
	c1 = p2*p1 - N*p6 + p1*p5 - N*p7
	c2 = p2*p4 - N*p8 + p4*p5 - N*p9

	xc = (c1*b2-c2*b1)/(a1*b2-a2*b1)
	yc = (a1*c2-a2*c1)/(a1*b2-a2*b1)
	R1 = np.sqrt((p2 - 2*p1*xc + N*xc*xc + p5 - 2*p4*yc + N*yc*yc)/N)	
	Ri = np.sqrt((x-xc)**2 + (y-yc)**2)
	R = np.mean(Ri)
	std_R = np.std(Ri)
	residu = np.sum((Ri-R)**2)
	residu2= np.sum((Ri**2-R**2)**2)
	#print (R1,R)
	return xc,yc,R,std_R

#### Reference: https://dtcenter.org/met/users/docs/write_ups/circle_fit.pdf
def circle_fitting_alg(x,y):
	# coordinates of the barycenter
	x_m = np.mean(x)
	y_m = np.mean(y)
	
	# calculation of the reduced coordinates
	u = x - x_m
	v = y - y_m

	# linear system defining the center in reduced coordinates (uc, vc):
	#    Suu * uc +  Suv * vc = (Suuu + Suvv)/2
	#    Suv * uc +  Svv * vc = (Suuv + Svvv)/2
	
	Suv  = np.sum(u*v)
	Suu  = np.sum(u**2)
	Svv  = np.sum(v**2)
	Suuv = np.sum(u**2 * v)
	Suvv = np.sum(u * v**2)
	Suuu = np.sum(u**3)
	Svvv = np.sum(v**3)

	# Solving the linear system
	A = np.array([ [ Suu, Suv ], [Suv, Svv]])
	B = np.array([ Suuu + Suvv, Svvv + Suuv ])/2.0
	uc, vc = np.linalg.solve(A, B)

	xc = x_m + uc
	yc = y_m + vc

	# Calculation of all distances from the center (xc, yc)
	Ri     = np.sqrt((x-xc)**2 + (y-yc)**2)
	R      = np.mean(Ri)
	std_R  = np.std(Ri)
	residu = np.sum((Ri-R)**2)
	residu2= np.sum((Ri**2-R**2)**2)
	return xc,yc,R,std_R
	
def calc_R(x,y,c):
    """ calculate the distance of each 2D points from the center c=(xc, yc) """
    return np.sqrt((x-c[0])**2 + (y-c[1])**2)

def fhand(c,x,y):
    """ calculate the algebraic distance between the 2D points and the mean circle centered at c=(xc, yc) """
    Ri = calc_R(x,y,c)
    return Ri - Ri.mean()

#### Reference: http://scipy-cookbook.readthedocs.io/items/Least_Squares_Circle.html
def circle_fitting_leastsq(x,y):
	x_m = np.mean(x)
	y_m = np.mean(y)
	center_estimate = x_m, y_m
	center_2, ier = optimize.leastsq(fhand, center_estimate, args=(x,y))

	xc, yc = center_2
	Ri_2 = calc_R(x,y,center_2)
	R = Ri_2.mean()
	std_R = Ri_2.std()
	return xc,yc,R.std_R
