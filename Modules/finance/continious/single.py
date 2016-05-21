
from math import log, e

def PV(fv,r,n):
  return fv/e**(r*n)

def FV(pv,r,n):
  return pv*e**(r*n)
  
def R(pv,fv,n):
  return log(float(fv)/pv)/n

def ER(rs,k=None):
  return rs*k if k!=None else sum(rs)
  
def N(pv,fv,r):
  return log(float(fv)/pv)/r
  

