
import numpy as np
import matplotlib.pyplot as plt

# equally spaced nodes

class EquidistantNodes:
  """ 
  h - distance between nodes
  seg - tuple of x0 and xN
  table - table of differences
    [i,j] - i - order of difference
            j - index    
  """
  
  class Interpolation:
    forward_newton = 1
    backward_newton = 2
    forward_gaussian = 3
    backward_gaussian = 4
    stirling = 5
    finite_diff_bessel = 6
  
    @staticmethod
    def str(k):
      res = ""
      t = EquidistantNodes.Interpolation
      if k == t.forward_newton:
        res = "forward Newton formula"
      elif k == t.backward_newton: 
        res = "backward Newton formula"
      elif k == t.forward_gaussian:
        res = "forward Gaussian formula"
      elif k == t.backward_gaussian:
        res = "backward Gaussian formula"
      elif k == t.stirling:
        res = "Stirling formula"
      elif k == t.finite_diff_bessel:
        res = "Bessel formula"
      return res
  
  def __init__(self,x_lb,x_ub,N,y_array):
    self.n = N-1 # number of segments
    self.h = (x_ub-x_lb)/(N-1)
    self.seg = (x_lb,x_ub)
    self.table = EquidistantNodes.compute_table_of_diffs(y_array) 
    self.x_array = [x_lb + i*(x_ub-x_lb)/(N-1) for i in range(N)]
    
  def get_Xs(self):
    return self.x_array 
  
  @staticmethod
  def norm(array):
    return np.sqrt(sum(map(lambda x:x**2,array)))
  
  @staticmethod
  def count_sign_changes(array):
    c = 0
    for i in range(1,len(array)):
      if (array[i-1]>0. and array[i]<0. or
          array[i-1]<0. and array[i]>0.):
        c+=1
    return c   
  
  @staticmethod
  def compute_table_of_diffs(y_array):
    table = [list(y_array)]
    n = len(y_array)
    
    norm0 = EquidistantNodes.norm(y_array)
    for i in range(1,n):
      t = table[i-1]
      m = len(t)-1
      c = m*[None]
      for k in range(m): 
        c[k] = t[k+1]-t[k] 
      norm1 = EquidistantNodes.norm(c)
      
      if (norm1 > norm0 and 
          EquidistantNodes.count_sign_changes(c)/float(len(c)) > 1./3.):
        break
      table.append(c)  
      norm0 = norm1
    return table   
  
  def get_left_node(self,x):
    i = int((x-self.seg[0])/self.h)
    xl = self.seg[0] + i*(self.seg[1]-self.seg[0])/self.n
    return i,xl
  
  def get_right_node(self,x):
    i,xl = self.get_left_node(x)
    return i+1,xl+self.h
  
  def get_nearest_node(self,x):
    i = int((x-self.seg[0])/self.h)
    xl = self.seg[0] + i*(self.seg[1]-self.seg[0])/self.n
    xr = xl + self.h 
    return (i+1,xr) if x-xl > xr-x else (i,xl)  
  
  def forward_newton_interpolation(self,u,i):
    t = self.table
    # v - u factor, p - order, r - factorial
    v,p,r = 1,0,1
    s = t[p][i]
    while p+1 < len(t) and i < len(t[p+1]) and t[p+1][i] != None:
      v *= u-p
      p += 1
      r *= p
      s += v*t[p][i]/r
    return s,self.Interpolation.forward_newton
    
  def backward_newton_interpolation(self,u,i):
    t = self.table
    # v - u factor, p - order, r - factorial
    v,p,r = 1,0,1
    s = t[p][i]
    while p+1 < len(t) and i-1 >= 0 and t[p+1][i-1] != None:
      v *= u+p
      p += 1
      r *= p
      i -= 1
      s += v*t[p][i]/r
    return s,self.Interpolation.backward_newton
      
  def forward_gaussian_interpolation(self,u,i):
    t = self.table
    # v - u factor, p - order, r - factorial
    v,p,r,j = 1,0,1,0
    s = t[p][i]
    while True:
      p += 1
      r *= p
      if p%2.==0:
        i -= 1
        j += 1
        v *= u-j
      else:
        v *= u+j
      if not (p < len(t) and 0 <= i < len(t[p]) and t[p][i] != None):
        break      
      s += v*t[p][i]/r
    return s,self.Interpolation.forward_gaussian
        
  def backward_gaussian_interpolation(self,u,i):
    t = self.table
    # v - u factor, p - order, r - factorial
    v,p,r,j = 1,0,1,0
    s = t[p][i]
    while True:
      p += 1
      r *= p
      if p%2.==0:
        j += 1
        v *= u+j
      else:
        i -= 1
        v *= u-j
      if not (p < len(t) and 0 <= i < len(t[p]) and t[p][i] != None):
        break      
      s += v*t[p][i]/r
    return s,self.Interpolation.backward_gaussian
  
  def stirling_interpolation(self,u,i):
    return ((self.forward_gaussian_interpolation(u,i)[0] + 
             self.backward_gaussian_interpolation(u-1,i+1)[0])/2.,
            self.Interpolation.stirling)
           
  def finite_diff_bessel_interpolation(self,u,i):
    t = self.table
    # v - u factor, p - order, r - factorial
    v,p,r,j = 1,0,1,0
    
    c1 = 1./2.
    c2 = (2.*u-1.)/2.
    
    s = c1*(t[p][i]+t[p][i+1])
    while True:
      p += 1
      r *= p
      if p%2.==0:
        c = c1
        v *= (u+j)*(u-j-1)
        j += 1
        
        w = 0
        if p < len(t) and 0 <= i < len(t[p]):
          w += t[p][i]
          if 0 <= i-1 < len(t[p]): 
            w += t[p][i-1] 
        else: break
        
        i -= 1
      else:
        c = c2
        if not (p < len(t) and 0 <= i < len(t[p])): 
          break        
        w = t[p][i]
      
      s += c*v*w/r
    return s,self.Interpolation.finite_diff_bessel   

  def interpolate(self,x):
    n = self.n
    h = self.h
    
    i,xp = self.get_left_node(x)
    q = (x-xp)/self.h  
    
    # for stirling, first gauss and bessel the same 
    n_diffs = len(self.table)
    r = n_diffs/2 + n_diffs%2
    while not (0 <= i-r+1 <= n-n_diffs):  
      n_diffs -= 1
      r = n_diffs/2 + n_diffs%2
    n_center = n_diffs

    # for forward newton
    n_diffs = len(self.table)
    while not (i <= n-n_diffs): 
      n_diffs-=1
    n_begin = n_diffs
    
    # for backward newton
    n_diffs = len(self.table)
    while not (0 <= i-n_diffs+1):  
      n_diffs -= 1
    n_end = n_diffs
    
    n_max = max(n_begin,n_center,n_end)
    
    if n_max == n_center:
      if 0.25 <= abs(q) <= 0.75:
        i,xp = self.get_left_node(x)
        method = self.finite_diff_bessel_interpolation
      else:
        i,xp = self.get_left_node(x)
        method = self.stirling_interpolation
    else:
      if n_max == n_end:
        i,xp = self.get_right_node(x)
        method = self.backward_newton_interpolation      
      else:
        i,xp = self.get_left_node(x)
        method = self.forward_newton_interpolation
    u = (x-xp)/self.h
    return method(u,i)
    
  
if __name__ == "__main__":
  
  # tests  
  def general_tests(i):
    x0,xN,N = -0.6,1.2,19
    x_array = [-0.5243,1.0483,-0.1882,-0.1144,0.8562]
    if i==0:
      y_array = [-7.4305,6.8754,6.4145,6.0298,5.7063,5.4320,5.1978,
                  4.9960,4.8219,4.6719,4.5437,4.4360,4.3482,4.2800,
                  4.2310,4.2006,4.1876,4.1897,4.2033]
    elif i==1:
      y_array = [2.0385,2.6063,3.0825,3.4851,3.8289,4.1255,4.3841,
                 4.6115,4.8128,4.9916,5.1503,5.2907,5.4141,5.5220,
                 5.6160,5.6989,5.7741,5.8469,5.9242]    
    elif i==2:
      y_array = [8.3262,7.8362,7.4098,7.0442,6.7346,6.4755,6.2606,
                 6.0835,5.9385,5.8208,5.7274,5.6575,5.6128,5.5985,
                 5.6237,5.7016,5.8506,6.0945,6.4632]    

    
    return x0,xN,N,y_array,x_array
      
  
  # computing
  def execute_test(x_lb,x_ub,N,y_array,x_array):
    t = EquidistantNodes(x_lb,x_ub,N,y_array)
     
    print "difference order: ",len(t.table),"\n"
    
    X = t.get_Xs()
    Y = y_array
    
    X_int = x_array
    Y_int = []
    
    for x in x_array:
      i1 = t.get_left_node(x)[0]
      print "interpolating point:",x
      print "neighbouring values:",y_array[i1],y_array[i1+1]
      y,flag = t.interpolate(x)           
      print "answer: ",y
      print "used formula: ",EquidistantNodes.Interpolation.str(flag),"\n"  
      Y_int.append(y)
    print "\n"   

    plt.plot(X,Y,"go")
    plt.plot(X_int,Y_int,"r+")  
     
    plt.show() 
    
  
  def execute_proof(x_lb,x_ub,N,func,x_array): 
    y_array = [func(x) for x in 
               [x_lb + i*(x_ub-x_lb)/(N-1) for i in range(N)]]
    t = EquidistantNodes(x_lb,x_ub,N,y_array)
    
    # for x_array
    y_exact = [func(x) for x in x_array]
    
    X = t.get_Xs()
    Y = y_array
    
    X_int = x_array
    Y_int = []
    
    for x in x_array:
      i1 = t.get_left_node(x)[0]
      print "interpolating point:",x
      print "neighbouring values:",y_array[i1],y_array[i1+1]
      y,flag = t.interpolate(x)           
      print "answer:",y,flag,"\n"  
      Y_int.append(y)
    print "\n"   
    
    print [y1-y2 for y1,y2 in zip(y_exact,Y_int)]
    
    plt.plot(X_int,Y_int,"go")  
    plt.plot(X_int,y_exact,"r+")  
 
    plt.show() 
    
  
  
  
  #execute_test(*general_tests(0))
  
  #"""
  x_lb,x_ub,N,y_array,x_array = general_tests(0) 
  func = lambda x: x**4-x**2+1
  execute_proof(x_lb,x_ub,N,func,x_array)
  #"""
   