
import math

""" mid-point method """
def mid_point_method(func,func_der,segment,eps=.1**3):
  a,b = segment
  n = 0
  while b-a > eps:
    n+=1 
    x_ = (a+b)/2.
    # segemnt exception
    if func_der(x_) < 0: a = x_  
    else: b = x_
  x = (a+b)/2.
  return x,func(x),n

""" end mid-point method """  

  
""" newton's method """
def newton_method(func,func_der1,func_der2,x0,eps=.1**3):
  """ sufficient condition of convergence f'/f''' > 0 on 
      segment """
  next = lambda x: x-func_der1(x)/func_der2(x)
  x1 = next(x0)
  n = 0
  while abs(x1-x0) > eps:
    n+=1  
    x0,x1 = x1,next(x1)
  x = (x0+x1)/2.
  return x,func(x),n

""" end newton's method """  
  

""" simplified newton's method """
def simplified_newton_method(func,func_der1,x0,y0_der2,eps=.1**3):
  next = lambda x: x-func_der1(x)/y0_der2
  x1 = next(x0)
  n = 0
  while abs(func_der1(x1)) > eps:
    n+=1  
    x0,x1 = x1,next(x1)
  x = x1
  return x,func(x),n

""" end simplified newton's method """  
  

""" secant method """  
def secant_method(func,func_dir,segment,x0,eps=.1**3):
  """ unstable method """
  a,b = segment
  x1 = (a*func_dir(b)-b*func_dir(a))/(func_dir(b)-func_dir(a))
  d0 = func_dir(x0)
  n = 0
  while abs(x1-x0) > eps:
    n += 1 
    d1 = func_dir(x1)
    # compute next step
    x0,x1,d0 = x1,x1-(x1-x0)*d1/(d1-d0),d1
  x = (x1+x0)/2.
  return x,func(x),n
  
""" end secant method """
   

""" cubic approximation method """   
def cubic_approx_method(func,func_dir,segment,eps=.1**3):
  x1,x2 = segment
  y1,y2 = func(x1),func(x2)
  yd1,yd2 = func_dir(x1),func_dir(x2)
  
  z = lambda: yd1+yd2-3*(y2-y1)/(x2-x1)
  w = lambda: math.sqrt(z()**2-yd1*yd2)
  mu = lambda: (w()+z()-yd1)/(2*w()-yd1+yd2)
  
  n = 0
  while x2-x1 > eps:
    print x1,x2
    n+=1
    x_ = x1+mu()*(x2-x1)
    y_,yd_ = func(x_),func_dir(x_)
    
    # pitfall
    if abs(y_) <= eps: break 
    
    if yd1*yd_ < 0: 
      x2,y2,yd2 = x_,y_,yd_
    else: # yd2*yd_ < 0
      x1,y1,yd1 = x_,y_,yd_
      
  x = (x1+x2)/2.
  return x,func(x),n  
  
""" end cubic approximation method """
   
   
if __name__ == "__main__":
      
  def example(k):
    func,der,der2,seg = None,None,None,None
    if k == 1: 
      func = lambda x: 100*(x-0.24)**2  
      der = lambda x: 200*(x-0.24)
      der2 = lambda x: 200
      seg = (0.,1.)
    elif k == 2:
      func = lambda x: x**2+16./x
      der = lambda x: 2.*x + -16./(x*x) 
      der2 = lambda x: 2. + 32./(x**3)
      seg = (1.,4.)
    elif k == 3: 
      func = lambda x: (x-1)**4
      der = lambda x: 4*((x-1)**3)   
      der2 = lambda x: 12*((x-1)**2)      
      seg = (-2.,3.)
    elif k == 4:
      """ unsolvable with newton method due to 
          different signs of first and third 
          derivatives f'/f''' < 0 on segment """
      func = lambda x: x*np.arctan(x)-np.log(1+x**2)/2.
      der = lambda x: np.arctan(x)
      der2 = lambda x: 1./(1.+x*x)
      seg = (-6.,6.)  
    elif k == 5:
      """ like previous variant + 
          difficult to analyze """
      func = lambda x: x*np.sin(1./x)
      der = lambda x: np.sin(1./x)-np.cos(1./x)/x
      der2 = lambda x: -np.sin(1./x)/(x**3)
      seg = (0.2,1.)
    elif k == 6:
      """ newton methods converge only on [3,4] due to
          condition f'/f''' > 0, so, because x* = 3
          we take point x0 = 4 """
      func = lambda x: ((x-1.)**2)*((x-3.)**2)
      der = lambda x: 4*(x-1)*(x-2)*(x-3)
      der2 = lambda x: 4*((x-2)*(x-3)+(x-1)*(2*x-5))
      seg = (2.,4.) 
    return func,der,der2,seg
  
  func,der,der2,seg = example(1)
  
  import numpy as np
  import matplotlib.pyplot as plt
  
  xs = np.arange(seg[0],seg[1],0.01)
  ys = map(func,xs)
  plt.plot(xs,ys,"b")
  
  # calculating
  xmp,ymp,nmp = mid_point_method(func,der,seg)
  print "mid_point_method:"," x=",xmp," y=",ymp," n=",nmp
  plt.plot(xmp,ymp,"ro")
  
  xn,yn,nn = newton_method(func,der,der2,seg[1])
  print "newton_method:"," x=",xn," y=",yn," n=",nn
  plt.plot(xn,yn,"ro")
  
  xns,yns,nns = simplified_newton_method(func,der,seg[1],der2(seg[1]))
  print "simplified_newton_method:"," x=",xns," y=",yns," n=",nns
  plt.plot(xns,yns,"c+")
  
  xse,yse,nse = secant_method(func,der,seg,seg[1])
  print "secant_method:"," x=",xse," y=",yse," n=",nse 
  plt.plot(xse,yse,nse,"c+")
  
  xc,yc,nc = cubic_approx_method(func,der,seg)
  print "cubic_approx_method:"," x=",xc," y=",yc," n=",nc 
  
  plt.show()
