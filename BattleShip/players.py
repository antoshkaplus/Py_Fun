
from ai import AI
from support import *

class Player:
  def __init__(self):
    self.sz = 10
    self.ships = {1:4,2:3,3:2,4:1}

  def makeMove(self):
    print "override me"
  def procMove(self,pt,res):
    print "override me"
  def acceptMove(self,pt):
    print "override me"
  def finish(self):  
    print "override me"
    
    
class Computer(Player):
  def __init__(self):
    Player.__init__(self)
    ships, sz = self.ships, self.sz
    ai = AI(ships,sz)
    self.ai = ai
    bt = BaseTable(sz)
    bt.addFleetRand(ships) 
    self.baseTable = bt
    
    self.baseShips = bt.ships
    self.enemyShips = ai.ships
    
  def makeMove(self):
    return self.ai.makeMove()
    
  def procMove(self,pt,res):
    self.ai.procMove(pt,res)
    
  def acceptMove(self,pt):
    return self.baseTable.shot(pt)
  
  def finish(self):
    return self.victory() or self.defeat()
  def victory(self):
    return all(a==0 for a in self.enemyShips.values())
  def defeat(self):
    return all(a==0 for a in self.baseShips.values())
   

if __name__ == "__main__":
  from random import choice
  
  #import sys
  #sys.stdout = open("out.txt","w")
  
  p1,p2 = Computer(),Computer()
  if choice((True,False)):
    p1,p2 = p2,p1
  res = None
  
  # remove then
  p1.id = 1
  p2.id = 2
  
  print "initialization is complete"
  
  while True:
    mv = p1.makeMove()
    mvR = p2.acceptMove(mv)
    p1.procMove(mv,mvR)
    if p1.finish() or p2.finish():
      res = p1
      break
    if mvR==MISS:
      p1,p2 = p2,p1
  
  print "game over", res.id, res.victory()==True
  