
# cash flow at the end of an period

from single import PV as sgPV
from math import log

def PV(c,r,g=None,n=None):
  pv = None
  if g == None:
    if n == None: # perpetuity
      pv = c/r
    else: 
      pv = (c*(1.-1/(1+r)**n)/r if r != 0. else
            sgPV(c*n,r,1))
  else: # with growth rate
    if n == None: # perpetuity
      pv = c/(r-g)
    else:
      pv = (c*(1-((1+g)/(1+r))**n)/(r-g) if r != g else
            sgPV(c*n,r,1))
  return pv
  
def FV(c,r,n):
  return c*((1+r)**n-1)/r  
  
def PMT(r,n,pv=None,fv=None):
  return (fv*r/((1+r)**n-1) if pv == None else
          pv*r/(1-1/(1+r)**n))

def N(c,r,pv):
  return log(c/(c-pv*r),1+r)

def G(pv,c,r,n=None):
  g = None
  if n == None:
    g = r-float(c)/pv
  else: 
    # should write formulae here 
    pass
  return g
  
