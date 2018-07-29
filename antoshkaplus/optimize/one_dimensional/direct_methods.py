
# methods work for unimodal functions 

# quadratic approximation method only for convex functions !!!


""" dichotomy_method """
def dichotomy_method(func,segment,delta=.1**3/3.,eps=.1**3):
  """
  delta < eps/2 since segment [a,b] always
  contain [x-delta,x+delta] where x in [a,b]   
  """    
  a,b = segment
  n = 0
  while b-a > eps:
    n+=1 
    m = (a+b)/2.
    x1,x2 = m-delta,m+delta
    # segemnt exception
    if func(x1) < func(x2): b = x2  
    else: a = x1
  x = (a+b)/2.
  return x,func(x),n

""" end dichotomy_method """


""" golden_section_search """
# one dimensional optimization of convex function
def golden_section_search(func,segment,eps=.1**3):
  tau = 1.618033988
  a,b = segment
  x1,x2 = b-(b-a)/tau,a+(b-a)/tau
  n = 0
  while b-a > eps:
    n+=1
    # segment exception
    if func(x1) < func(x2): 
      b,x2 = x2,x1
      x1 = a+b-x2      
    else: 
      a,x1 = x1,x2
      x2 = a+b-x1
  x = (a+b)/2.
  return x,func(x),n

""" end golden_section_search """ 
  
  
""" quadratic_approximation_method """
def quadratic_approximation_method(func,segment,eps=.1**3):
  """ ps = 3*[(x,f(x))] - three points to find minimum point of  
      corresponding parabola"""
  def approx_min(ps):
    r = lambda i,j: ps[i][0]**2-ps[j][0]**2 
    s = lambda i,j: ps[i][0]-ps[j][0]    
    return (ps[0][1]*r(1,2)+ps[1][1]*r(2,0)+ps[2][1]*r(0,1))/ \
        (2*(ps[0][1]*s(1,2)+ps[1][1]*s(2,0)+ps[2][1]*s(0,1)))
  
  # x1,x3 - endings  
  x1,x3 = segment[0],segment[1] 
  y1,y3 = func(x1),func(x3)
  x2 = (x1+x3)/2. # some random point  
  y2 = func(x2)
  
  x_ = approx_min([(x1,y1),(x2,y2),(x3,y3)])
  y_ = func(x_)
    
  n = 0
  while x3-x1 > eps:
    n+=1
   
    # if adjacent points are almost equal 
    if x2-x1 <= eps: x3 = x2; break
    if x3-x2 <= eps: x1 = x2; break
    
    # approximation minimum
    x_ = approx_min([(x1,y1),(x2,y2),(x3,y3)])
    y_ = func(x_)
    if x1 <= x_ <= x2:
      if y_ <= y2: 
        x3,x2 = x2,x_ # x1 the same
        y3,y2 = y2,y_
      else: 
        x1 = x_; y1 = y_ # x2,x3 the same
    else: # x2 <= x_ <= x3:
      if y_ <= y2: 
        x1,x2 = x2,x_ # x3 the same
        y1,y2 = y2,y_
      else: 
        x3 = x_; y3 = y_ # x1,x2 the same
        
    print(x1,x2,x3)
  x = (x1+x3)/2.
  return x,func(x),n
    
""" end quadratic_approximation_method """    
    

""" modified_quadratic_approximation_method """  
def modified_quadratic_approximation_method(func,segment,eps=.1**3):
  # ps = 3*[(x,f(x))]
  def approx_min(ps):
    r = lambda i,j: ps[i][0]**2-ps[j][0]**2 
    s = lambda i,j: ps[i][0]-ps[j][0]    
    return (ps[0][1]*r(1,2)+ps[1][1]*r(2,0)+ps[2][1]*r(0,1))/ \
        (2*(ps[0][1]*s(1,2)+ps[1][1]*s(2,0)+ps[2][1]*s(0,1)))
  
  # x1,x3 - endings  
  x1,x3 = segment[0],segment[1] 
  y1,y3 = func(x1),func(x3)
  x2 = (x1+x3)/2. # some random point  
  y2 = func(x2)
  
  x_ = approx_min([(x1,y1),(x2,y2),(x3,y3)])
  y_ = func(x_)
     
  n = 1
  while abs(x_-x2) > eps:
    n+=1
    
    dx = min(map(lambda x: abs(x_-x),[x1,x2,x3]))
    x2,y2 = x_,y_
    x1,x3 = x2-dx,x2+dx
    y1,y3 = func(x1),func(x3)
   
    x_ = x2+(dx*(y1-y3))/(2.*(y1-2*y2+y3))
    y_ = func(x_)
    
  x = (x_+x2)/2.
  return x,func(x),n
    
""" end modified_quadratic_approximation_method """
    

if __name__ == "__main__":
      
  def example(k):
    func,seg = None,None
    if k == 1: 
      func = lambda x: 100*(x-0.24)**2  
      seg = (0.,1.)
    elif k == 2:
      func = lambda x: x**2+16./x
      seg = (1.,4.)
    elif k == 3: 
      func = lambda x: (x-1)**4 
      seg = (-2.,3.)
    elif k == 4:
      func = lambda x: x*np.arctan(x)-np.log(1+x**2)/2.
      seg = (-6.,6.)  
    elif k == 5:
      func = lambda x: x*np.sin(1./x)
      seg = (0.2,1.)
    return func,seg
  
  func,seg = example(4)
  
  import numpy as np
  import matplotlib.pyplot as plt
  
  xs = np.arange(seg[0],seg[1],0.01)
  ys = map(func,xs)
  """
  # calculating
  xd,yd,nd = dichotomy_method(func,seg)
  print "dichotomy_method:"," x=",xd," y=",yd," n=",nd
  """
  xg,yg,ng = golden_section_search(func,seg)
  print("golden_section_search:", \
        " x=",xg," y=",yg,"n=",ng)
  """
  xq,yq,nq = quadratic_approximation_method(func,seg)
  print "quadratic_approximation_method:", \
        " x=",xq," y=",yq," n=",nq
  
  xqm,yqm,nqm = modified_quadratic_approximation_method(func,seg)
  print "modified_quadratic_approximation_method:", \
        " x=",xqm," y=",yqm," n=",nqm 
  
  plt.plot(xs,ys,"b",xd,yd,"r+",xg,yg,"gx",xq,yq,"yo",xqm,yqm,"c*")
  """
  plt.plot(xg,yg,"go")
  
  plt.plot(xs,ys,"b")
  plt.show()
