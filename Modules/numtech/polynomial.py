

import numpy as np


class Polynomial:
  def __init__(self,coeffs):
    self.coeffs = list(coeffs)
    
  def decrease(self,x):
    a = self.coeffs
    n = len(a)
    b = (n-1)*[None]
    b[n-2] = a[n-1]
    for i in range(n-2,0,-1):
      b[i-1] = a[i]+x*b[i]    
    self.coeffs = b
  
  def get_value(self,x):
    a = self.coeffs
    s = 0
    p = 1
    for c in a:    
      s += c*p
      p *= x
    return s  
    
  @staticmethod  
  def chebyshev(n):
    """ 
    n - power of polynomial 
    T(n+1) = 2*x*T(n) - T(n-1) 
    T(n) = cos(n*arccos(x))
    """
    
    p0 = Polynomial([1.])
    p1 = Polynomial([0.,1.])     
    res = None
    if n == 0:
      res = p0
    elif n == 1:
      res = p1
    else:
      P = Polynomial
      for i in range(2,n+1):
        p2 = P.sum(P.multiply(p1,2.,1),P.multiply(p0,-1.))
        p0,p1 = p1,p2
      res = p2  
      
    return res  
  
  @staticmethod  
  def multiply(polyn,numb=1.,x_pow=0):
    polyn = polyn.copy()
    a = polyn.coeffs
    a[:] = x_pow*[0.] + map(lambda x: x*numb,a) 
    return polyn
    
  def copy(self):
    return Polynomial(list(self.coeffs))

  def sum(polyn1,polyn2):
    c1,c2 = polyn1.coeffs,polyn2.coeffs
    n1,n2 = len(c1),len(c2)
    big,small = ((list(c1),c2) if n1 > n2 
                               else (list(c2),c1))                           
    for i,s in enumerate(small):
      big[i] += s
    return Polynomial(big)  
    
  @staticmethod    
  def derivative(polyn):
    a = list(polyn.coeffs)
    for i in range(len(a)):
      a[i] *= i 
    return Polynomial(a[1:])  
 
  def zero_power(self,i):
    self.coeffs[i] = 0.
   
if __name__ == "__main__":

  from equation import *


  n = 7
  r = Polynomial.chebyshev(n)
  
  eps = 1e-5
  
  """
  import matplotlib.pyplot as plt
  
  X = np.arange(-100.,100.,0.1)
  Y = map(p.get_value,X)
  
  plt.plot(X,Y)   
  plt.show() 
  """
  
  print "\n Secant method \n"
  p = r.copy()
  for i in range(n):
    func = p.get_value
    x,n_iter = secant_method(func,-2.2,4.5,eps)
    print "solution: ",x," n_iter: ",n_iter
    print "check: ",np.cos(n*np.arccos(x)),"\n"
    p.decrease(x)
  
  print "\n Newton method \n"
  p = r.copy()
  for i in range(n):
    func = p.get_value
    der = Polynomial.derivative(p).get_value
    x,n_iter = newton_method(func,der,0.6,eps)
    print "solution: ",x," n_iter: ",n_iter
    print "check: ",np.cos(n*np.arccos(x)),"\n"
    p.decrease(x)
  
  print "\n Simple iteration method \n"
  p = r.copy()
  for i in range(n):
    if abs(p.coeffs[1]) < eps: break
    v = Polynomial.multiply(p,-1./p.coeffs[1])
    v.zero_power(1)
    F = v.get_value
    x,n_iter = simple_method(F,0.5,eps)
    print "solution: ",x," n_iter: ",n_iter
    print "check: ",np.cos(n*np.arccos(x)),"\n"
    p.decrease(x)
  else: print "all right"


 
    
    





    
     
  
  
  
  