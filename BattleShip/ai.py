
from random import randint, choice
from support import *


class State:
  @staticmethod
  def makeMove(ai):
    print "override me"
  @staticmethod 
  def procMove(ai,pt,res):
    print "override me"
  
  
class FindShip(State):
  str = "FindShip"
  @staticmethod
  def makeMove(ai):
    sz = ai.sz
    while True:
      pt = Pt(randint(0,sz-1),randint(0,sz-1))
      if ai.enemyTable[pt]==WATER:
        break
    return pt
  
  @staticmethod
  def procMove(ai,pt,res):
    if res==HIT:
      ai.source = pt
      ai.dirs = ai.enemyTable.posDirs(pt)
      ai.setState(FindLine)
 
 
class FindLine(State):
  str = "FindLine"
  @staticmethod
  def makeMove(ai):
    return choice(ai.dirs)+ai.source

  @staticmethod
  def procMove(ai,pt,res):
    if res==MISS:
      ai.dirs.remove(pt-ai.source)
    elif res==HIT:
      s = ai.source
      isIn = ai.enemyTable.isIn
      
      p1,d1 = s,s-pt
      p2,d2 = pt,pt-s
      
      t = ai.enemyTable
      if not isIn(p1+d1) or t[p1+d1]==MISS:
        ai.way = (p2,d2)
        ai.setState(FinishOff)
      elif not isIn(p2+d2) or t[p2+d2]==MISS:
        ai.way = (p1,d1)
        ai.setState(FinishOff)
      else:
        ai.ways = ((p1,d1),(p2,d2))
        ai.setState(GoByLine)
    else: # SUNK
      ai.setState(FindShip)
      

class GoByLine(State):
  str = "GoByLine"
  @staticmethod
  def makeMove(ai):
    c = choice(ai.ways)
    return c[0]+c[1]
    
  @staticmethod
  def procMove(ai,pt,res):
    w1,w2 = ai.ways
    if res==MISS:
      ai.way = w2 if pt-w1[0]==w1[1] else w1
      ai.setState(FinishOff)
    elif res==HIT:
      if pt-w1[0]==w1[1]:
        ai.ways = ((pt,w1[1]),w2)
      else:
        ai.ways = (w1,(pt,w2[1]))
    else: # SUNK
      ai.setState(FindShip)
      
      
class FinishOff(State):
  str = "FinishOff"
  @staticmethod
  def makeMove(ai):
    return ai.way[0]+ai.way[1]
    
  @staticmethod  
  def procMove(ai,pt,res):
    if res==HIT:
      ai.way = (pt,ai.way[1])
    else: # SUNK
      ai.setState(FindShip)


      
class AI:
  def __init__(self,ships,sz):
    self.sz = sz
    self.enemyTable = EnemyTable(ships,sz)
    self.ships = self.enemyTable.ships
    self.setState(FindShip)
  
  def setState(self,state):
    self.state = state  
    
  def makeMove(self):
    return self.state.makeMove(self)

  def procMove(self,pt,res):
    table = self.enemyTable
    table[pt] = res
    self.state.procMove(self,pt,res)
    
  