
from math import atan

def newton_method(f, fd, x0, eps, dom=(None, None)):
  left = right = False
  if dom[0] != None:
    left = True
    x_left = dom[0]
  if dom[1] != None:
    right = True
    x_right = dom[1]
  n = 0
  while True:
    x1 = x0 - f(x0)/fd(x0)
    if left and x1 < x_left:
      x1 = (x0+x_left)/2.
    if right and x1 > x_right:
      x1 = (x0+x_right)/2.
    n += 1
    if abs(x0-x1) < eps: break
    x0 = x1
  return x1,n

def secant_method(f,x0,x1,eps):
  n = 1
  while True:
    x2 = x1 - f(x1)/(f(x0)-f(x1))*(x0-x1)
    n += 1
    if abs(x1-x2) < eps: break
    x0,x1 = x1,x2
  return x2,n


def simple_method(F,x0,eps):
  n = 0
  while True:
    x1 = F(x0)
    n += 1
    if abs(x0-x1) < eps: break
    x0 = x1
  return x1,n


if __name__ == "__main__":
  
  # simple iteration method
  # f = 2x^5 - 5x^4 + x^3 - 3x^2 + 4x - 1 = 0 
  F = lambda x: (1.-2.*x**5+5.*x**4-x**3+3.*x**2)/4.   
  eps = 1e-5
  
  x_simple = simple_method(F,0.,eps)
  y_simple = F(x_simple[0])
  print "simple iteration: ",x_simple,y_simple
  
  #print "\n"
  
  # newton and secant methods 
  a,b,c = 1.22,2.1,0.24
  f = lambda x: x-a-b*atan(c*x)
  fd = lambda x: 1-b*c/(1+(c*x)**2)
  eps = 1e-6
  
  x_newton = newton_method(f,fd,100.,eps)
  y_newton = f(x_newton[0])
  print "Newton method: ",x_newton,y_newton
  
  x_secant = secant_method(f,-100.,100.,eps)
  y_secant = f(x_secant[0])
  print "secant method: ",x_secant,y_secant
  
  
  