
import numpy as np
import numpy.linalg as algo

"""
don't forget to use right norm! 
  and CLOSURE
"""


def gauss_method(A,b):
  def swap_rows(p,q):
    t=A[p,:].copy();A[p,:]=A[q,:].copy();A[q,:]=t    
    b[p,0],b[q,0] = b[q,0],b[p,0]
  
  A,b = A.copy(),b.copy()
  
  n = A.shape[0]
  for i in range(n):
    q = i+np.argmax(np.abs(A[i:,i]))
    swap_rows(i,q)
    for k in range(i+1,n):  
      c = A[k,i]/A[i,i] 
      for j in range(i,n):      
        A[k,j] -= A[i,j]*c
      b[k,0] -= b[i,0]*c
      
  # A now is upper triangular
  
  x = np.matrix(np.zeros((n,1)))
  for i in range(n-1,-1,-1):
    c = A[i,i]
    t = b[i,0]
    for j in range(i+1,n):
      t -= x[j,0]*A[i,j]
    x[i,0] = t/c  
 
  return x
  
  
def simple_method(A,b,eps):
  n = A.shape[0]
  x0 = np.matrix(np.zeros((n,1)))
  x1 = np.matrix(np.zeros((n,1)))
  
  n_iter = 0
  while True: 
    for i in range(n):
      x1[i,0] = x0[i,0]-1./A[i,i]*(sum([A[i,j]*x0[j] for j in range(n)])-b[i,0])
    if np.max(abs(x1-x0)) < eps:
      break
    n_iter += 1  
    x0,x1 = x1,x0
  return x1,n_iter      
  
  
def seidel_method(A,b,eps):
  n = A.shape[0]
  x = np.matrix(np.zeros((n,1)))
  
  n_iter = 0
  while True: 
    for i in range(n):
      x[i,0] = -(sum([A[i,j]*x[j,0] for j in range(i)]+
                     [A[i,j]*x[j,0] for j in range(i+1,n)]) - b[i,0])/A[i,i]
    v = A*x-b
    if sum(abs(v[i,0]) for i in range(n)) < eps:
      break
    n_iter += 1  
  
  return x,n_iter   
  
  
  
if __name__ == "__main__":
  
  """
  t = 0.05*1.+0.5
  
  Adirect = np.matrix([[1.6+t,t-4.3,2.5+t,5.8-t],
                       [3.2+t,2.4+t,t-1.1,3.9+t],
                       [t    ,t-11 ,6.1+t,9.7-t],
                       [3.6-t,1.9+t,t-4.4,8.9-t]])  
  Bdirect = np.matrix([[3.87],
                       [5.91],
                       [14.03],
                       [6.55]])
  
  Aiter = np.matrix([[4.8+t,-2.1 ,1.7,t-0.5,0.4  ],
                     [1.1  ,3.9+t,1.6,0.9  ,0.2+t],
                     [0.3  ,t-1.4,5.7+t,-3.2,0.6 ],
                     [1.4+t,0.7  ,1.2  ,6.6+t,3.1],
                     [-2.2,1.3+t ,0.2  ,1.4,6.3+t]])
  Biter = np.matrix([[3.4-t],
                     [2.7+t],
                     [6.6+t],
                     [0.8-t],
                     [9.1-t]])
  eps = 1e-7  
  
  print "gauss elimination:\n",gauss_method(Adirect,Bdirect),"\n"
  print "exact solution:\n",np.linalg.solve(Adirect,Bdirect),"\n"
  
  print "epsilon: ",eps
  print "simple iteration:\n",simple_method(Aiter,Biter,eps),"\n"
  print "seidel method:\n",seidel_method(Aiter,Biter,eps),"\n"
  print "exact soluiton:\n",np.linalg.solve(Aiter,Biter)
  """
  #import sys
  #print sys.float_info
  
  n = 3
  eps = 1e-6
  
  A = np.matrix(np.zeros((n,n)))
  for i in range(n):
    for j in range(n):
      A[i,j] = 1./(i+1+j)
  
  x = np.matrix([[1.] for i in range(n)])
 
  f = A*x
  
  print "gauss elimination:\n",gauss_method(A,f),"\n"
  print "seidel method:\n",seidel_method(A,f,eps),"\n"
  #print "exact solution:\n",algo.solve(A,f),"\n"
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  