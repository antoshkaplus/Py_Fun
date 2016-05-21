
import tkMessageBox as tkMB 

from const import *
from controls import Timer


class Model:
  
  def __init__(self,root):
    self.observers = []
    self.motion = INIT
    self.formula = None
    self.timer = Timer() # work
    self.root = root
    
    self.update_time = 16
    self.update_event = None
    
  def set_formula(self,formula):
    self.formula = formula 
    
  def set_motion(self,motion):
    self.motion = motion
    if motion == START: 
      self.timer.start()
      self.update_turn_on()
    elif motion == STOP: 
      self.timer.stop()
      self.notify_observers()
      self.update_turn_off()
    elif motion == FURTHER: 
      self.timer.further()
      self.update_turn_on()
    elif motion == PAUSE: 
      self.timer.pause()
      self.notify_observers()
      self.update_turn_off()
    
  def set_time_scale(self,val):
    self.timer.set_time_scale(val)
    
  
  # observer's state methods
  def get_time(self):
    return self.timer.get_time()
 
  def get_rotation_val(self):
    val = self.formula.get_val(self.get_time())
    if val == None:
      self.set_motion(STOP)
      tkMB.showerror("Error","Model is broken")
      val = 0.
    return val
    
  def get_motion(self):
    return self.motion
   
    
  def add_observer(self,new_obs):
    for obs in self.observers:
      if obs is new_obs: 
        break
    else: self.observers.append(new_obs)
    
  def rem_observer(self,rem_obs):
    for i,obs in enumerate(self.observers):
      if obs is rem_obs: 
        self.observers[i:i+1] = []
        break
        
  def notify_observers(self):  
    for obs in self.observers:
      obs.update(self)
  
  # model updated ... notify observers
  def update_turn_on(self):
    self.root.after(self.update_time,self.notify_observers)
    self.update_event = self.root.after(self.update_time,self.update_turn_on)
     
  def update_turn_off(self):
    self.root.after_cancel(self.update_event)
  
  
  



  
    
    
    
    



  