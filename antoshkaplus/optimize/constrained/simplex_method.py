
import copy as cp

import numpy as np
import matplotlib.pyplot as plt


"""

  support classes

"""

class Object:
  Min = 1
  Max = 2

class Constrs:
  def __init__(self,couple):  
    if couple == None:
      self.empty = True
    else:
      self.empty = False
      self.A,self.B = cp.deepcopy(couple)
      self.shape = self.A.shape
  def __repr__(self):
    return ("Aeq=\n"+
            self.A.__repr__()+"\n"+
            "Beq=\n"+
            self.B.__repr__())
  def copy(self):
    return Constrs(self.get_content())
  def get_shape(self):
    return self.shape
  def is_empty(self):
    return self.empty
  def get_content(self):
    res = None if self.is_empty() else (self.A,self.B)  
    return res
  def concatenate(self,constrs):
    res = None
    if self.is_empty():
      if constrs.is_empty():
        res = Constrs(None)
      else:
        res = constrs.copy()      
    else: 
      if constrs.is_empty():
        res = self.copy()
      else:
        A1,B1 = self.get_content()
        A2,B2 = constrs.get_content() 
        res = Constr((np.vstack((A1,A2)),
                      np.vstack((B1,B2))))
    return res

class EqConstrs(Constrs):
  def __init__(self,couple,eliminated):
    """ eliminated - dictionary (row:column) of
      eliminated columns, row shows element with one """
    self.eliminated  = dict(eliminated)
    Constrs.__init__(self,couple)    
  def __repr__(self):
    return (Constrs.__repr__(self)+"\n"+
            "eliminated:"+self.eliminated.__repr__())
        
 
class LeConstrs(Constrs):
  pass 
    
class ObjFunc:
  def __init__(self,C,obj):
    self.C = C.copy()
    self.obj = obj    
  def get_coeffs(self):
    return self.C  
  def get_object(self):
    return self.obj
  

"""  

  simplex method
  
"""
  
def simplex_method(eq_constrs,obj_func):
  """ A = | Aeq Beq |
          | Cf  F   | """
  
  ### support function (use enclosing vars)
  
  def convert_constrs(eq_constrs):
    """ returns res_eq_constrs with quality of eliminated
        equals quality of equations """
    res_eq_constrs = None
    res_flag = False
    if not eq_constrs.is_empty():
      Aeq,Beq = eq_constrs.get_content()
      el = dict(eq_constrs.eliminated)
      
      k = len(el)
      m,n = Aeq.shape
      P = np.zeros((m,m-k))
      
      i,r = 0,0
      for j in range(m-k):
        while (r < k) and (i in el):
          i+=1; r+=1
        P[i,j] = -1. if Beq[i,0] < 0 else 1.
        el[i] = j+n
        i+=1
      
      A = np.hstack((Aeq,P))
      B = Beq.copy()
      C = np.hstack((np.zeros((1,n)),-np.ones((1,m-k))))
    
      eq_constrs = EqConstrs((A,B),el)
      obj_func = ObjFunc(C,Object.Max)
     
      F,n_iter,sol,flag,eq_constrs = simplex_method(eq_constrs,obj_func)
      if flag:
        res_flag = True
        
        A,B = eq_constrs.get_content()
        A = A[:,:n]
        el = eq_constrs.eliminated
        res_eq_constrs = EqConstrs((A,B),el)
       
    return res_eq_constrs,res_flag

  
  def eliminate_obj_func(p):
    for i,j in enumerate(basis):
      if j == p: 
        k = i      
        break
    
    c = A[-1,p]
    for j in range(n):
      A[-1,j] -= A[k,j]*c
    
  def basis_func_elimination():  
    b = basis[:]    
    m = A.shape[0]-1
    for i in range(m):
      for k,j in enumerate(b): 
        if A[i,j] != 0:
          eliminate(i,j)
          break
      del b[k]
      
  def eliminate(k,p):
    """ k - row of one 
        p - col of zeros """
    m,n = A.shape
    # getting one in (k,p)
    c = A[k,p]
    for j in range(n):
      A[k,j] /= c
    # eliminating other columns
    for i in range(m):
      if i != k:
        c = A[i,p]
        for j in range(n):
          A[i,j] -= A[k,j]*c

  def basis_elimination():          
    """ uses matrix A and basis - list, 
        where value is basis variable """        
    b = basis[:]    
    m = A.shape[0]-1
    for i in range(m):
      for k,j in enumerate(b): 
        if A[i,j] != 0:
          eliminate(i,j)
          break
      del b[k]

  def find_index_for_basis():
    """ returns index of new element inside
        basis, if no such an element flag = False """
    flag = True
    ind = 0
    m = A.shape[0]-1 # function row
    n = A.shape[1]-1 # last coefficient
    for j in range(1,n):
      #if ((obj == Object.Min and A[m,ind] > A[m,j]) or 
      #    (obj == Object.Max and A[m,ind] < A[m,j])): 
      if A[m,ind] < A[m,j]:   
        ind = j
    #if ((obj == Object.Min and A[m,ind] >= 0) or
    #    (obj == Object.Max and A[m,ind] <= 0)):
    if A[m,ind] <= 0:
      flag = False
    return ind,flag
 
  def change_basis(ind):
    """ returns None if finish of algorithm,
        else index of row where variable 
        changed """
    flag = True
    row = None
    m = A.shape[0]-1
    n = A.shape[1]-1
    p = [i for i in range(m) if A[i,ind] > 0]
    if p != []:
      row = p[0]
      for k in p[1:]:
        if A[k,n]/A[k,ind] < A[row,n]/A[row,ind]: row = k 
      basis[row] = ind
    else: 
      flag = False    
    return row,flag

  def get_solution():
    n = A.shape[1]-1
    x = np.zeros((n,1))
    for i,j in enumerate(basis):  
      x[j,0] = A[i,n]
    return x
  
  ### preparation 
  
  F = n_iter = sol = res_constrs = None
  flag = True 
 
  m,n = eq_constrs.get_shape()
  if len(eq_constrs.eliminated.keys()) != m:
    eq_constrs,flag = convert_constrs(eq_constrs)
  
  if flag:     
    Aeq,Beq = eq_constrs.get_content()
    
    # method will always maximize function
    Cf = obj_func.get_coeffs()
    if obj_func.get_object() == Object.Min: 
      Cf *= -1
      
    A = np.vstack((np.hstack((Aeq,Beq)),
                   np.hstack((Cf,np.zeros((1,1)))))) 
    basis = m*[0]
    el = eq_constrs.eliminated
    for i in el.keys(): basis[i] = el[i]    

    basis_func_elimination()
    
    ### algorithm
    
    res = False
    n_iter = 1
    while True:   
      ind,flag = find_index_for_basis()
      
      if not flag:
        res = True
        break
        
      row,flag = change_basis(ind)  
      if not flag: 
        break
      
      eliminate(row,basis[row])
      n_iter+=1
    
    flag = res
    
    sol = get_solution() 
    F = -A[m,n]

    Aeq = A[:-1,:-1]
    Beq = A[:-1,-1]
    el = dict(enumerate(basis))
    res_constrs = EqConstrs((Aeq,Beq),el)
    
  return F,n_iter,sol,flag,res_constrs
 
  
if __name__ == "__main__":
  
  def test_simplex_method(i):
    eq_constrs = obj_func = None
    if i == 0:
      Aeq = np.matrix([[2,4,1,0],
                       [3,1,0,1]])
      Beq = np.matrix([[9],
                       [6]])
      eq_constrs = EqConstrs((Aeq,Beq),{0:2,1:3})
      
      Cf = np.matrix([[6,2,0,0]])
      obj_func = ObjFunc(Cf,Object.Max)
    elif i == 1:
      Aeq = np.matrix([[ 1,1,1,0, 0, 0],
                       [-1,4,0,1, 0, 0],
                       [ 1,0,0,0,-1, 0],
                       [ 0,1,0,0, 0,-1]])
      Beq = np.matrix([[20],
                       [20],
                       [10],
                       [5]])
      eq_constrs = EqConstrs((Aeq,Beq),{0:2,1:3})
      
      Cf = np.matrix([[3,4,0,0,0,0]])
      obj_func = ObjFunc(Cf,Object.Max)      
    return eq_constrs,obj_func

  res = simplex_method(*test_simplex_method(1))
  for r in res:
    print r,"\n"
    
 
  
  