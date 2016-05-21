
import math

class Integral:
  # seg must be tuple
  def __init__(self,func,seg):
    self.func = func
    self.seg = seg
  
  # eps - relative absolute error
  def solve_by_trapezoid(self,eps):
    trapezoid = (Integral.trapezium_iteration,3)
    return Integral.dual_recalculation(trapezoid,self.seg,self.func,eps)
    
  def solve_by_simpson(self,eps):
    simpson = (Integral.simpson_iteration,3)  
    return Integral.dual_recalculation(simpson,self.seg,self.func,eps)
  
  def solve_by_gauss(self):
    return Integral.gauss_formula(self.seg,self.func)
  
  
  # this function used to solving methods
  @staticmethod
  def value_sum(seg,func,n):
    return sum(map(func,[seg[0]+(2.*i-1.)/n*(seg[1]-seg[0]) for i in range(1,n/2+1)]))
  
  @staticmethod  
  def trapezium_iteration(seg,func):
    d = seg[1]-seg[0]
    J = d/2.*sum(map(func,seg))
    n = 1
    while True:
      yield J
      n *= 2
      J = J/2.+d/n*Integral.value_sum(seg,func,n) 
    
  @staticmethod  
  def simpson_iteration(seg,func):
    d = seg[1]-seg[0]
    J = d/2.*sum(map(func,seg))
    n = 1
    while True:
      yield J
      n *= 2
      Q = 2./n*Integral.value_sum(seg,func,n)
      if n == 2:
        R = sum(map(func,seg))/6.
      else: 
        R = R/2.+Q/6.
      J = (seg[1]-seg[0])*(R+2.*Q/3.)      
    
  @staticmethod  
  def dual_recalculation((method,mu),seg,func,eps):
    obj = method(seg,func)
    J0 = obj.next()
    J1 = obj.next()
    n = 2
    while (J1 == 0 and J0 != J1) or (J1 != 0 and abs((J1-J0)/J1)/mu > eps):
      J0,J1 = J1,obj.next()
      n += 1
    return J1,n  
    
  @staticmethod  
  def gauss_formula(seg,func):
    t_array = [-0.96028986,
               -0.79666648,
               -0.52553242,
               -0.18343464,
                0.18343464,
                0.52553242,
                0.79666648,
                0.96028986]
    a_array = [ 0.10122854,
                0.22238104,
                0.31370664,
                0.36268378,
                0.36268378,
                0.31370664,
                0.22238104,
                0.10122854]
    J = 0.
    for i in range(8):
      J += a_array[i]*func((seg[0]+seg[1])/2.+(seg[1]-seg[0])/2.*t_array[i])
    return J            
  
  
  
if __name__ == "__main__":
  lg = math.log10
  ln = math.log
  sin = math.sin
  cos = math.cos
  atan = math.atan
  
  seg = [1.9,3.1]
  func = lambda x: x*lg((x**2)*ln(x**2+1)*(cos(x)**2)*atan(x**2)+x*sin(x)**2) 
  
  I = Integral(func,seg)
  
  eps = 1.e-5
  print "epsilon: ",eps
  print "trapezoid solution: ",I.solve_by_trapezoid(eps)
  print "simpson solution: ",I.solve_by_simpson(eps)
  
  print "gauss solution: ",I.solve_by_gauss()
  
  
  
  
  
  