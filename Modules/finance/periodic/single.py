
# cash flow at the end of an period

from math import log

def PV(fv,r,n):
  return fv/(1+r)**n

def FV(pv,r,n):
  return pv*(1+r)**n
  
def R(pv,fv,n):
  return (float(fv)/pv)**(1./n)-1
  
def ER(rs,k=None):
  """
  rs - rates or just one rate
  k - number of compound periods if rs just one number, else None
  """
  return ((1.+rs)**k-1 if k!=None else
          reduce(lambda x,y:x*y,(1.+r for r in rs))-1)
  
def N(pv,fv,r):
  return log(float(fv)/pv,1+r)
  

