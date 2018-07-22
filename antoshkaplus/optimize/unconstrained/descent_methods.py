
import numpy as np
import matplotlib.pyplot as plt

# in the calculations use only "numpy" arrays!!! 

from optimization.one_dimensional.direct_methods import golden_section_search


""" gradient method with constant step """
def grad_const_step_method(func,func_grad,x0,step,e):
  n = 0
  
  q = [x0]
  while True:
    w = func_grad(x0)
    x1 = x0 - step*w
    q.append(x1)
    n+=1
    if max(abs(x0-x1)) <= e: 
      x = x1
      break
    x0 = x1
  return x,func(x),n,q

""" end gradient method with constant step """


""" gradient method with crushing step """
def grad_crushing_step_method(func,func_grad,x0,step0,crush,w_coeff,e):
  n = 0
  q = [x0]
  while True:
    w = func_grad(x0)
    w_sq = np.dot(w,w)
    
    step = step0
    while func(x0 - step*w) > func(x0)-w_coeff*step*w_sq: 
      step *= crush
    x1 = x0 - step*w
    q.append(x1) 
    n+=1  
    if max(abs(x0-x1)) <= e:
      x = x1
      break      
    x0 = x1
  return x,func(x),n,q   

""" end gradient method with crushing step """
  
  
""" method of steepest descent """
def steepest_descent(func,func_grad,x0,d,e):
  n = 0
  q = [x0]
  while True:
    w = func_grad(x0)
    w_norm = w/np.sqrt(np.dot(w,w))
    
    func_min = lambda step: func(x0-step*w_norm)
    step = golden_section_search(func_min,(0.,d),e)[0]
    x1 = x0 - step*w_norm
    q.append(x1) 
    n+=1  
    if (abs(func(x0)-func(x1))) <= e:
      x = x1
      break      
    x0 = x1
  return x,func(x),n,q

""" end method of steepest descent """  
  
  
""" newton method """
def newton_method(func,func_grad,func_H,x0,e):
  n = 0
  q = [x0]
  while True:
    w = func_grad(x0)
    H = func_H(x0)
    x1 = x0 - np.array(np.multiply(H.I,w).sum(1).transpose())[0]
    q.append(x1)
    n+=1
    if max(abs(x0-x1)) <= e:
      x = x1
      break
    x0 = x1
  return x,func(x),n,q
    
""" end newton method """  
  
  
  
def example1_grad_const_step():
  func = lambda x: (2*x[0]-1)**2 + (x[1]+1)**2
  func_grad = lambda x: np.array([4*(2*x[0]-1),2*(x[1]+1)])
  func_H = lambda x: np.matrix(((8,0),(0,2)))
  x0 = np.array([-2,1])
  bounds = ((-3.,3.),(-3.,3.))
  step = 0.2
  crush = 0.5
  w_coeff = 0.5
  e = 0.1**3
  return func,func_grad,func_H,x0,bounds,step,crush,w_coeff,e   
   

def example2_grad_const_step():
  func = lambda x: x[0]**2 + 10*(x[1]**2)
  func_grad = lambda x: np.array([2*x[0],20*x[1]])
  x0 = np.array([2.5,2.5])
  bounds = ((-0.5,3.),(-0.5,3.))
  step = 0.09
  e = 0.1**5
  return func,func_grad,x0,bounds,step,e   

def example1_newton_method():
  func = lambda x: x[0]**2 + 10*(x[1]**2)
  func_grad = lambda x: np.array([2*x[0],20*x[1]])
  func_H = lambda x: np.matrix(((2,0),(0,20)))
  x0 = np.array([2.5,2.5])
  bounds = ((-0.5,3.),(-0.5,3.))
  step = 0.9
  crush = 0.8
  w_coeff = 0.5
  e = 0.1**5
  return func,func_grad,func_H,x0,bounds,step,crush,w_coeff,e   
  
"""
  w = 0.5

  f(x1,x2) = 6*(x1**2) - 4*x1*x2 + 3*(x2**2) + 4*np.sqrt(5)*(x1+2*x2) + 22
  x0 = (-2,1), e = 0.01, step = 0.1, crush = 0.5, x* = (-2.2,-4.47)
 
"""  
   
def example_grad_crush_step():
  func = lambda x: (1-x[0])**2 + 100*(x[1]-x[0]**2)**2
  func_grad = lambda x: np.array([2*(x[0]-1)-400*(x[1]-x[0]**2), 
                                  200*(x[1]-x[0]**2)])
  x0 = np.array([-0.6,0.4])
  bounds = ((-0.7,1.5),(-0.3,1.5))
  step = 0.1
  crush = 0.8
  w_coeff = 0.001
  e = 0.1**3
  return func,func_grad,x0,bounds,step,crush,w_coeff,e   
    
  
if __name__ == "__main__":  

  func,func_grad,func_H,x0,bounds,step,crush,w_coeff,e = example1_grad_const_step()  
    
  x1,y1,n1,q1 = grad_crushing_step_method(func,func_grad,x0,step,crush,w_coeff,e)
  x2,y2,n2,q2 = steepest_descent(func,func_grad,x0,5.,e)
  x3,y3,n3,q3 = grad_const_step_method(func,func_grad,x0,step,e)

  x4,y4,n4,q4 = newton_method(func,func_grad,func_H,x0,e)

  print x1,y1,n1,"grad_crushing_step_method"
  print x2,y2,n2,"steepest_descent"
  print x3,y3,n3,"grad_const_step_method"
  print x4,y4,n4,"newton_method"  
      
  X = np.arange(bounds[0][0],bounds[0][1],0.01)
  Y = np.arange(bounds[1][0],bounds[1][1],0.01)    
  Z = np.array([np.array([func([x,y]) for x in X]) for y in Y])    
  plt.contour(X,Y,Z)    
  #plt.scatter(x1[0],x1[1],marker='o',c='y')

  X,Y = zip(*q1)
  plt.plot(X,Y,'r')
  plt.plot(X,Y,'ro')
  X,Y = zip(*q2)
  plt.plot(X,Y,'y')
  plt.plot(X,Y,'yo')
  X,Y = zip(*q3)
  plt.plot(X,Y,'g')
  plt.plot(X,Y,'go')
  X,Y = zip(*q4)
  plt.plot(X,Y,'c')
  plt.plot(X,Y,'co')
  
  #plt.plot()
  plt.show()    
      
      
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
