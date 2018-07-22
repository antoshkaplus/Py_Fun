
import numpy as np
import matplotlib.pyplot as plt

# numpy.matrix calculations inside !!! 

def gradient_projection_method(func,
                               func_grad,
                               eq_constrs,
                               ineq_constrs,
                               x,eps):  
  n = x.shape[0]
  
  seq = []  
    
  ac_constrs = None
  inac_constrs = None
  A = None  
  
  # important lambda functions  
  conc = lambda a,b: b if a == None else np.vstack((a,b))   
  excl = lambda a,i: (None if a.shape[0] == 1 else
                      np.vstack((a[:i],a[i+1:]))) 
  
  for c in ineq_constrs:
    if c[0,:-1]*x == c[0,-1]:
      ac_constrs = conc(ac_constrs,c[0,:])
      A = conc(A,c[0,:-1])
    else:
      inac_constrs = conc(inac_constrs,c[0,:])    
  if eq_constrs != None:
    A = conc(A,eq_constrs[:,:-1])
  
  special = None
  i = 0
  while i < 10:
    i += 1 
    seq.append(x)
    
    P = np.eye(n) - (np.zeros((n,n)) if A == None else 
                     A.T*((A*A.T).I)*A)
    w = -func_grad(x)
    # descent direction
    p = P*w
  
    if np.max(np.abs(p)) > eps:
  
      alpha = 2.
      if inac_constrs != None:
        """ if has inactive constraints 
            calculate max alpha """    
        vals = [(c[0,-1]-(c[0,:-1]*x)[0,0])/(c[0,:-1]*p)[0,0] 
                for c in inac_constrs]
        if special == None:          
          
        elif inac_constrs.shape[0] != 1:        
          vals[special] = max(vals)+1
          i = np.argmin(vals)
          alpha = vals[i]  
        
      while True:
        x1 = x + alpha*p
        if func(x1) < func(x):
          x = x1
          break
        else: alpha /= 2.
      
      # constraint manipulations
      if inac_constrs != None and alpha == vals[i]:
        ac_constrs = conc(ac_constrs,inac_constrs[i,:])
        A = conc(A,inac_constrs[i,:-1])
        inac_constrs = excl(inac_constrs,i)
      
    elif ac_constrs == None:       
      break
    else: 
      T = (A*A.T).I*A*w # vector Rm     
      k = ac_constrs.shape[0]
      for i,t in enumerate(T[:k]):
        if t < 0: 
          inac_constrs = conc(inac_constrs,ac_constrs[i,:])
          ac_constrs = excl(ac_constrs,i)
          A = excl(A,i) 
          special = inac_constrs.shape[0]-1          
          break
      else:
        break
  return x,func(x),seq


if __name__ == "__main__":  
   
  def test():
    func = lambda x: (2.*x[0,0]**2 + 2.*x[1,0]**2 
                    - 2.*x[0,0]*x[1,0] - 4.*x[0,0] - 6.*x[1,0])
    func_grad = lambda x: np.matrix([[4.*x[0,0]-2.*x[1,0]-4.],
                                     [4.*x[1,0]-2.*x[0,0]-6.]])                  
    eq_constrs = None
    ineq_constrs = np.matrix([[1.,1.,2.],
                              [1.,5.,5.],
                              [-1.,0.,0.],
                              [0.,-1.,0.]])
    x0 = np.matrix([[0],[0]])
    eps = 0.1**3
    return (func, 
            func_grad,
            eq_constrs,
            ineq_constrs,
            x0,eps)
  """
  def test2():
    func = lambda x: (2.*x[0,0]**2 + 2.*x[1,0]**2 
                    - 2.*x[0,0]*x[1,0] - 4.*x[0,0] - 6.*x[1,0])
    func_grad = lambda x: np.matrix([[4.*x[0,0]-2.*x[1,0]-4.],
                                     [4.*x[1,0]-2.*x[0,0]-6.]])                  
    eq_constrs = None
    ineq_constrs = np.matrix([[1.,1.,2.],
                              [1.,5.,5.],
                              [-1.,0.,0.],
                              [0.,-1.,0.]])
    x0 = np.matrix([[0],[0]])
    eps = 0.1**3
    return (func, 
            func_grad,
            eq_constrs,
            ineq_constrs,
            x0,eps)
  """
  x,y,seq = gradient_projection_method(*test())  
  
  print x,y,len(seq)
  
  X = np.arange(-1./2.,2.,0.01)
  Y = np.arange(-1./2.,1.,0.01)    
  Z = np.array([np.array([(test()[0])(np.matrix([[x],[y]])) for x in X]) for y in Y])    
  plt.contour(X,Y,Z)    
  
  
  
  X,Y = map(lambda x:x[0,0],seq),map(lambda x:x[1,0],seq)
  plt.plot(X,Y,'r')
  plt.plot(X,Y,'ro')
  
  plt.show()  
  
 
 