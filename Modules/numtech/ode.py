
import numpy as np
import scipy.integrate as spint

import sys
from exceptions import ArithmeticError

import proper_integration as pi




# Computational Functions
  
def compute_one_point(algo,(x0,y0),x1,eps):
  n = 1
  while True:
    h = (x1-x0)/n
    p = np.arange(x0,x1,h)
    
    try:
      y = y0
      for a in p:
        y = algo((a,y),h)
        if np.isinf(y):
          raise ArithmeticError()
      if n == 1: 
        y1 = y
      else:
        y2 = y
        if abs(1.-y1/y2) <= abs(eps):
          break
        y1 = y2
    
    except:
      y2 = y2 if vars().has_key("y2") else y      
      break
      
    n+=1
  
  return y2,n


def compute_multi_point(algo_st,algo,(x0,y0),x1,n_st,eps):
  n = n_st
  n_p = n_st-1
  while True:
    h = (x1-x0)/n
    p = np.arange(x0,x1,h)
    
    ys = [y0]
    for a in p[:n_p]:
      ys += [algo_st((a,ys[-1]),a+h)]
            
    try:
      for a in p[n_p:]:
        y = algo(a,h,ys)
        if np.isinf(y):
          raise ArithmeticError()
        ys = ys[1:]+[y]
        
      if n == n_st: 
        y1 = y
      else: 
        y2 = y     
        if abs(1.-y1/y2) <= abs(eps):
          break
        y1 = y2    
    
    except:
      if not vars().has_key("y2"):
        if vars().has_key("y"):
          y2 = y        
        else: y2 = ys[-1]     
      
      break  
      
    n+=1 
  return y2,n  


# One-Step Methods  
   
def picard_method(F,(x0,y0),x1,eps):
  
  def next((x0,y0),h):
    y2=y1=y0
    while True: 
      I = pi.Integral(lambda x: F(x,y1),(x0,x0+h))
      # take eps from enclosing function
      y2 = y0 + I.solve_by_simpson(eps)[0] 
      if abs(y2-y1) < eps:
        break   
      y1 = y2
    return y2
  
  #return next((x0,y0),x1-x0)
  return compute_one_point(next,(x0,y0),x1,eps)
  
  
# Step-By-Step Methods  

# One Point Methods
  
def euler_method(F,(x0,y0),x1,eps):  
  
  def next((x0,y0),h):
    return y0 + F(x0,y0)*h
  
  return compute_one_point(next,(x0,y0),x1,eps)
  
  
def heum_method(F,(x0,y0),x1,eps):

  def next((x0,y0),h):
    y2=y1=y0
    while True:
      y2 = y0 + h/2.*(F(x0,y0)+F(x0+h,y1))
      if abs(y2-y1) < eps:
        break
      y1 = y2
    return y2      
  
  return compute_one_point(next,(x0,y0),x1,eps)
    

def runge_kutta_2(F,(x0,y0),x1,eps):
  
  def next((x0,y0),h):
    k1 = h*F(x0,y0)
    k2 = h*F(x0+h/2.,y0+k1/2.)
    return y0 + k2
  
  return compute_one_point(next,(x0,y0),x1,eps)  

  
def runge_kutta_3(F,(x0,y0),x1,eps):

  def next((x0,y0),h):
    k1 = h*F(x0,y0)
    k2 = h*F(x0+h/2.,y0+k1/2.)
    k3 = h*F(x0+h,y0+2.*k2-k1)
    return y0 + (k1+4.*k2+k3)/6.
    
  return compute_one_point(next,(x0,y0),x1,eps)
  
  
def runge_kutta_4(F,(x0,y0),x1,eps):
  
  def next((x0,y0),h):
    k1 = h*F(x0,y0)
    k2 = h*F(x0+h/2.,y0+k1/2.)
    k3 = h*F(x0+h/2.,y0+k2/2.)
    k4 = h*F(x0+h,y0+k3)
    
    return y0 + (k1+2.*k2+2.*k3+k4)/6.
  
  return compute_one_point(next,(x0,y0),x1,eps)  


# Multi Point Methods
  
def adams_moulton_method(F,(x0,y0),x1,eps):  

  pr_coeffs = [-9.,37.,-59.,55.]
  cr_coeffs = [1.,-5.,19.,9.]
  
  sm = lambda coeffs,pts: sum(c*F(*p) for c,p in zip(coeffs,pts))
  
  def next(x0,h,ys):
    # construct points
    pts = zip([x0-i*h for i in range(len(ys)-1,-1,-1)],ys)
    
    # predictor formula
    y = pts[-1][1] + h*sm(pr_coeffs,pts)/24. 
    
    # push queue
    pts = pts[1:]+[(pts[-1][0]+h,y)]
    
    while True:
      # corrector formula
      y = pts[-2][1] + h*sm(cr_coeffs,pts)/24.
      
      if np.isinf(y) or abs(y-pts[-1][1]) < eps:
        break
      pts[-1] = (pts[-1][0],y)
    
    return y  
  
  algo_st = lambda pt,x1: runge_kutta_4(F,pt,x1,eps)[0]
  return compute_multi_point(algo_st,next,(x0,y0),x1,4,eps)
    
    
    
if __name__ == "__main__":
  
  def tests(i):
    F=x0=y0=x1=eps=None
    if i==0:
      F = lambda x,y: 3.*x + y**2.
      x0,y0 = 0.,1.
      x1 = 0.1
      eps = 1e-5
    elif i==1:
      F = lambda x,y: -x*(y**2.)
      x0,y0 = 2.,1.
      x1 = x0 + 0.3
      eps = 1e-4
    elif i==2:
      F = lambda x,y: np.sin(y)
      x0,y0 = 0.,1.
      x1 = x0 + 0.1
      eps = 1e-5
    
  def main_tests(i):
    x0,y0 = 0.,1.    
    if i==0:
      x1 = 1.
      p = 1.
      eps = 1e-12
    elif i==1:
      x1 = 0.99
      p = 2.
      eps = 1e-7
    elif i==2:
      x1 = 0.99
      p = 3.
      eps = 1e-5
    F = lambda x,y: y**p 
    
    return F,(x0,y0),x1,eps 
  
  methods = [
             #("runge_kutta 2",runge_kutta_2),
             #("runge kutta 3",runge_kutta_3),
             ("runge kutta 4",runge_kutta_4),
             #("heum_method",heum_method),
             #("euler_method",euler_method),
             ("adams moulton method",adams_moulton_method)
             #("picard method",picard_method)
            ]
           
  for i in range(1,3):       
    print "test %d:" % i  
    for key,val in methods:
      print key,": ",val(*main_tests(i))
  
  
  print "\n e:",np.e
  
  