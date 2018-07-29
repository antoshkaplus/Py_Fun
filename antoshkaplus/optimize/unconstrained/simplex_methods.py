
import numpy as np
import matplotlib.pyplot as plt

import antoshkaplus.optimize.one_dimensional.direct_methods as dm

# constructing simplexes

def construct_vertex_simplex(x0,edge_len): # 
  n = len(x0)
  v = (np.sqrt(n+1)+n-1)*edge_len/(n*np.sqrt(2))
  w = -n*edge_len/(n*np.sqrt(2))
  q = [x0+v for i in range(n+1)]
  q[0] = np.array(x0)
  for i in range(1,n+1):
    q[i][i-1] += w
  return q

  
def construct_center_simplex(x0,edge_len):
  n = len(x0)
  q = [np.array(x0) for i in range(n+1)]
  for i in range(n+1):
    if i > 0:
      q[i][i-1] += edge_len*np.sqrt(i/(2.*(i+1.)))
    for j in range(i,n):
      q[i][j] -= edge_len/np.sqrt(2.*(j+1.)*(j+2.))
  return q

def gen_pairs(q):
  res = []
  if q != []:
    n = len(q)
    res = [(np.array(q[i]),np.array(q[j])) for i in range(n) for j in range(i)] 
  return res

def gen_pairs_with_elem(q,p):
  res = []
  if q != []:
    n = len(q)
    res = [(np.array(p),np.array(q[i])) for i in range(n)] 
  return res  

# regular simplex methods  

def reg_simplex_constant(func,edge_len,x0):
  q = construct_center_simplex(x0,edge_len)
  q.sort(key=func)
  
  n = len(x0)
  n_iter = 0
  seq = gen_pairs(q)
  while True:
    for i in range(n,-1,-1):
      x_new = 2.*sum(q[:i]+q[i+1:])/n-q[i]
      if func(x_new) < func(q[i]): break
    else:
      break
    q[i] = x_new
    n_iter += 1
    seq.extend(gen_pairs_with_elem(q[:i]+q[i+1:],x_new))
    
    q.sort(key=func)
    
  x = q[0]
  return x,func(x),n_iter,seq


def reg_simplex_with_provided_reduction(func,edge_len,x0,delta,eps):
  q = construct_center_simplex(x0,edge_len)
  q.sort(key=func)

  n = len(x0)
  n_iter = 0
  seq = gen_pairs(q)
  while True:
    x_new = 2.*sum(q[:n])/n-q[n]
    flag = False
    if func(x_new) >= func(q[n]): # simplex reduction
      flag = True
      for i in range(1,n+1):
        q[i] = q[0] + delta*(q[i]-q[0])
    else: q[n] = x_new # replacing last point
    n_iter += 1
    p = (gen_pairs(q) if flag else gen_pairs_with_elem(q[:n],x_new))
    seq.extend(p)

    q.sort(key=func)
    # stopping criterion
    x_c = sum(q)/(n+1)
    if np.sqrt(sum([(func(q[i])-func(x_c))**2 for i in range(n+1)])/(n+1)) < eps:
      break

  x = q[0]
  return x,func(x),n_iter,seq


def reg_simplex_with_continues_reduction(func,reducing_func,edge_len,x0):
  pass

# unregular simplex method

def unreg_simplex(func,edge_len,x0,alpha,beta,gamma,delta,eps):
  """
    alpha - reflection coefficient
    beta - stretch coefficient
    gamma - nip coefficient
    delta - reduction coefficient 
  """
  q = construct_center_simplex(x0,edge_len)
  q.sort(key=func)

  n = len(x0)
  n_iter = 0
  seq = gen_pairs(q)
  while True:
    # reflection of max val point
    x = (1+alpha)*sum(q[:n])/n-alpha*q[n] 

    if func(q[n-1]) >= func(x) >= func(q[0]):
      q[n] = x
      q.sort(key=func)
    elif func(x) < func(q[0]):
      # stretch
      x_ = (1-beta)*sum(q[:n])/n+beta*x
      if func(x_) < func(x):
        q[n] = x_
        q.sort(key=func)
      else:
        q[n] = x
        q.sort(key=func)
    elif func(x) > func(q[n-1]) >= func(q[0]):
      # nip
      if func(x) <= func(q[n]):
        x_ = (1-gamma)*sum(q[:n])/n+gamma*x
      else: # func(x) > func(q[n])
        x_ = (1-gamma)*sum(q[:n])/n+gamma*q[n]
      if func(x_) < func(q[n]):
        q[n] = x_
        q.sort(key=func)
      else:
        # simplex reduction
        for i in range(1,n+1):
          q[i] = q[0] + delta*(q[i]-q[0])
        q.sort(key=func)

    n_iter+=1
    seq.extend(gen_pairs(q))
     
    # stopping criterion
    x_c = sum(q)/(n+1)
    if np.sqrt(sum([(func(q[i])-func(x_c))**2 for i in range(n+1)])/(n+1)) < eps:
      break
  x = q[0]
  return x,func(x),n_iter,seq

    
          

# other direct methods
# d - max step
# eps - how good to optimize by x
def coordinate_descent_method(func,x0,d,eps):
  n = len(x0)
  q = [x0]
  n_iter = 0
  while True:
    x1 = np.array(x0)
    for i in range(n):
      e = np.zeros(n); e[i] = 1.
      phi = lambda alpha: func(x1+alpha*e)
      x1[i] += dm.golden_section_search(phi,(-d,d),eps)[0]
    q.append(x1)
    n_iter += 1
    if max(abs(x1-x0)) <= eps: break
    x0 = x1
  x = x1
  return x,func(x),n_iter,q



def coordinate_descent_method_nonconvex(func,x0,d,eps):
  n = len(x0)
  q = [x0]
  n_iter = 0

  f = func(x0)
  while True:
    x1 = np.array(x0)
    for i in range(n):
      e = np.zeros(n); e[i] = 1.
      phi = lambda alpha: func(x1+alpha*e)
      alpha,f_new,iters = dm.golden_section_search(phi,(-d,d),eps)
      if f_new >= f:
        continue

      f = f_new
      x1[i] += alpha

    q.append(x1)
    n_iter += 1
    if max(abs(x1-x0)) <= eps: break
    x0 = x1
  x = x1
  return x,func(x),n_iter,q


if __name__ == "__main__":

  func = lambda x: 6.*x[0]**2-4.*x[0]*x[1]+3.*x[1]**2+ \
                   4.*np.sqrt(5.)*(x[0]+2.*x[1])+22.
  x0 = np.array((-2.,1.))
  delta = .5
  edge_len = 1
  eps = 0.01
  bounds = ((-3,2),(-5,2))


  alpha = 2
  beta = 5./2.
  gamma = 1./4.
  
  rsc_x,y,n,rsc_q = unreg_simplex(func,edge_len,x0,alpha,beta,gamma,delta,eps)
  print(rsc_x,y,n)
  rspr_x,y,n,rspr_q = reg_simplex_with_provided_reduction(func,edge_len,x0,delta,eps)
  print(rspr_x,y,n)
  
  # x,y,n_iter,q = coordinate_descent_method(func,x0,10.,eps)
  # print x,y,n_iter
      
  X = np.arange(bounds[0][0],bounds[0][1],0.01)
  Y = np.arange(bounds[1][0],bounds[1][1],0.01)    
  Z = np.array([np.array([func([x,y]) for x in X]) for y in Y])    
  plt.contour(X,Y,Z)    
  #plt.scatter(x1[0],x1[1],marker='o',c='y')

  for p in rspr_q:
    X,Y = zip(*p)
    plt.plot(X,Y,'g')
  x,y = zip(rsc_x)
  plt.plot(x,y,'go')
  """
  for p in rspr_q:
    X,Y = zip(*p)
    plt.plot(X,Y,'r')
  x,y = zip(rspr_x)
  plt.plot(x,y,'ro')
  """
  #X,Y = zip(*q)
  #plt.plot(X,Y,'r')
  #plt.plot(X,Y,'ro')
    
  #plt.plot()
  plt.show()    
  
    







