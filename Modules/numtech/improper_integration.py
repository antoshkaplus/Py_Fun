
from proper_integration import Integral    
from math import sin, pi
   
def ignoring_singularity(func,seg,index,phi,eps):   
  func_new = lambda x: func(x) if abs(x-seg[index]) > phi else 1.
  
  I = Integral(func_new,seg)
  return I.solve_by_simpson(eps)
  
def processing_to_the_limit(func,seg,eps):
  x1 = 1.
  x0 = 1./2.
  I = 0.
  n_iter = 0
  while True:
    n_iter += 1
    i = Integral(func,(x0,x1)).solve_by_simpson(eps)[0]  
    if abs(i) < eps:
      break
    I += i
    x1 = x0
    x0 /= 2.
  return I,n_iter
  
if __name__ == "__main__":
  eps = 1e-3    
  """
  func = lambda x: 1./(x**(1./2.))
  seg,index,phi = (0.,1.),0,1e-6
  print ignoring_singularity(func,seg,index,phi,eps)
  """
  
  """
  func = lambda x: 1./x * sin(1./x)
  seg = (0.,1.)
  print processing_to_the_limit(func,seg,eps)
  """
  
  print pi
  
  eps = 1e-4
  
  func1 = lambda x: sin(x)/x 
  I1 = ignoring_singularity(func1,[0.,1.],0,1e-8,eps)
  
  func2 = lambda y: 1./y * sin(1./y)
  I2 = processing_to_the_limit(func2,[0.,1.],eps)
  
  I = I1[0] + I2[0]
  print 2*I
  