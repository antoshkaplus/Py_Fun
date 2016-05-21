
from random import choice


class Game:
  def __init__(self,p1,p2):
    self.p1 = p1
    self.p2 = p2
  
  def start(self):
    p1,p2 = self.p1,self.p2
    if choice(True,False):
      p1,p2 = p2,p1
    res = None
    while True:
      mv = p1.makeMove()
      mvR = p1.acceptMove(mv)
      p1.procMove(mv,mvR)
      if p1.finish()
        res = p1
        break
      if mvR==MISS:
        p1,p2 = p2,p1
    return res
    
    