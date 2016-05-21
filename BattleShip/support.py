import random

MISS = 0
HIT = 1
SUNK = 2 
WATER = 3
SHIP = 4

VER = 1
HOR = 2


class Pt:
  def __init__(self,i,j):
    self.r,self.c = i,j
  def __add__(self,other):  
    s, o = self, other
    return Pt(s.r+o.r,s.c+o.c)
  def __sub__(self,other): 
    s, o = self, other
    return Pt(s.r-o.r,s.c-o.c)
  def __eq__(self,other):
    s, o = self, other
    return s.r == o.r and s.c == o.c
    
  def __str__(self):
    return "r: %d, c: %d" % (self.r,self.c)
  def rin(self,b1,b2):
    return b1 <= self.r <= b2
  def cin(self,b1,b2):
    return b1 <= self.c <= b2 
  
  
class Table:
  """ inherit me """  
  def __init__(self,sz,item):
    self.sz = sz
    self.arr = sz*sz*[item]   
   
  def ind(self,pt):
    """ be careful: private method """
    return self.sz*pt.r + pt.c
  
  def __setitem__(self,pt,item):
    self.arr[self.ind(pt)] = item
  
  def __getitem__(self,pt):
    return self.arr[self.ind(pt)]
  
  def __str__(self):
    s = ""
    sz = self.sz
    arr = self.arr
    for i in range(sz):
      s += " ".join(map(str,arr[i*sz:(i+1)*sz]))+"\n"
    return s
  
  def around(self,pt):
    sz = self.sz
    return filter(lambda d: d.rin(0,sz-1) and d.cin(0,sz-1),
                  [pt+Pt(-1,0),pt+Pt(1,0),pt+Pt(0,-1),pt+Pt(0,1),
                   pt+Pt(1,1),pt+Pt(-1,-1),pt+Pt(-1,1),pt+Pt(1,-1)])
   
  def isIn(self,pt):
    sz = self.sz
    return pt.rin(0,sz-1) and pt.cin(0,sz-1)
   
   
class EnemyTable(Table):
  def __init__(self,ships,sz):
    Table.__init__(self,sz,WATER)
    self.ships = ships.copy()
  
  def __setitem__(self,pt,item):
    arr = self.arr
    sz = self.sz
    ind = self.ind
    
    arr[ind(pt)] = item
    
    if item==SUNK:
      stack = [pt]
      count=1
      while stack != []:
        s = stack.pop()
        for a in self.around(s):
          i = ind(a)
          p = arr[i]
          if p==WATER:
            arr[i] = MISS
          elif p==HIT:
            arr[i] = SUNK
            stack.append(a)  
            count+=1
      self.ships[count]-=1
  
  def posDirs(self,pt):
    isIn = self.isIn
    sz = self.sz
    return filter(lambda d: isIn(pt+d) and self[pt+d]==WATER,
                  [Pt(-1,0),Pt(1,0),Pt(0,-1),Pt(0,1)])
  
  
class BaseTable(Table):
  def __init__(self,sz):
    Table.__init__(self,sz,WATER)
    self.ships = {}
   
  def shot(self,pt):
    item = self[pt]
    if item == WATER:
      self[pt] = MISS
    elif item == SHIP:
      self[pt] = SUNK
      sunk = True
      stack = [pt] 
      hit = [pt]
      water = []
      while stack != []:
        s = stack.pop()
        for a in self.around(s):
          p = self[a]
          if p==SHIP:
            sunk = False
            break
          elif p==WATER:
            water.append(a)
          elif p==HIT:
            self[a] = SUNK
            stack.append(a)
            hit.append(a)
        if not sunk: break
      if sunk:
        self.ships[len(hit)]-=1
        for a in water: self[a] = MISS
      else:
        for a in hit: self[a] = HIT
    return self[pt]
    
  def addShip(self,capty,pt,orient):
    isIn = self.isIn
    mv = Pt(0,1) if orient==HOR else Pt(1,0)
    sh = []
    alright = True
    
    for c in range(capty):
      if ((not isIn(pt) or self[pt]!=WATER) or 
           not all(map(lambda g: self[g]==WATER,self.around(pt)))):
        alright = False
        break
      else: sh.append(pt)
      pt = pt+mv 
    if alright:
      for pt in sh:
        self[pt] = SHIP
      ships = self.ships
      if capty in ships:
        ships[capty] += 1
      else: ships[capty] = 1
    return alright
  
  def addShipRand(self,capty):
    rand = random.randint
    choice = random.choice
    sz = self.sz
    while True:
      orient = choice((HOR,VER))
      pt = Pt(rand(0,sz-1),rand(0,sz-1))
      if self.addShip(capty,pt,orient):
        break
 
  def addFleetRand(self,ships):
    func = self.addShipRand
    for capty,numb in ships.items():
      for n in range(numb):
        func(capty)
      
      
      