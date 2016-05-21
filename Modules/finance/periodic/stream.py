
# cash flow at the end of an period

from support.equation import newton_method

def PV(arr,r):
  return (sum(a/(1+r)**(i+1) for i,a in enumerate(arr)) if isinstance(arr,list) else
          sum(a/(1+r)**i for i,a in arr.items())) # arr is dict
  
def dPV(arr,r):
  return (sum(-(i+1)*a/(1+r)**(i+2) for i,a in enumerate(arr)) if isinstance(arr,list) else
          sum(-(i)*a/(1+r)**(i+1) for i,a in arr.items())) # arr is dict
  
def FV(arr,r):
  return sum(a*(1+r)**i for i,a in enumerate(arr[::-1]))    

def IRR(c,arr,guess=0.,eps=1e-3): 
  return (newton_method(lambda r: PV(arr,r)-c,
                        lambda r: dPV(arr,r),guess,eps))
     
 