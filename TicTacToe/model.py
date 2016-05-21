
import sys
import os 
import pickle
from random import choice


import commands


USER = 1
AI = 0
CROSS = 1
ZERO = 0
EMPTY = 2

def myall(arr,val):
  """ are all values of list the same """
  return all(map(lambda x: x==val,arr))

class ConstBoard:
  """ hashable board, which used as a key 
  to a dictionary of {board:usefulness} 
  for AI move choices
  """
  def __init__(self,arr):  
    self.b = list(arr)
    h = 0
    p = 1
    for a in arr:
      h+=a*p
      p*=10      
    self.h = h
 
  def __eq__(self,cb): 
    return cb.h == self.h  
 
  def __hash__(self):
    return self.h
 
 
class Board:
  """ board is saved by rows in 9 length array """
  def __init__(self):
    self.b = [EMPTY]*9 # crosses and zeros
  
  def result(self,val):
    b = self.b
    # by columns
    for j in range(3):
      if myall(b[j:9:3],val):
        return ((i,j) for i in range(3))
    
    # by rows
    for i in range(0,7,3):
      if myall(b[i:i+3],val):
        return ((i/3,j) for j in range(3))
    
    
    if myall((b[0],b[4],b[8]),val): return ((i,i) for i in range(3))
    if myall((b[2],b[4],b[6]),val): return ((i,2-i) for i in range(3))
   
    return False
      
  def __str__(self):
    b = self.b
    def ch(k):
      return {EMPTY:" ",ZERO:"o",CROSS:"x"}[k]
    def row(i):  
      s = i*3
      return ch(b[s])+"|"+ch(b[s+1])+"|"+ch(b[s+2]) 
    def sep():
      return "-----"
    
    return row(0)+"\n"+sep()+"\n"+row(1)+"\n"+sep()+"\n"+row(2)
    
  def move(self,who,(i,j)):
    """ make a move on game board """
    self.b[i*3+j] = who
  
  def empty(self,(i,j)):
    return self.b[i*3+j] == EMPTY 
  
  def copy(self):
    new = Board()
    new.b = list(self.b)
    return new
  
  def const(self):
    return ConstBoard(self.b)

  def clear(self):
    self.b = [EMPTY]*9
    
  
class Game:
  def __init__(self):
    self.board = Board()
    
    # where to take AI boards
    self.boards_path = None
    # booleans
    self.user_move = None
    self.surrender = None
    # AI boards dictionary
    self.boards = {}
  
  def start(self):
    """ start listen to commands """
    try:
      self.listen()  
    finally:
      c = commands
      self.tell(c.EXIT)
    
  def listen(self):
    c = commands
    read = sys.stdin.read 
    while True:
      ch = read(1)
      if ch == c.START:
        self.new()
      elif ch == c.POINT:
        p = map(int,read(2))
        self.user_move = p
        break
      elif ch == c.EXIT:
        self.exit()
      elif ch == c.BOARDS:  
        p_len = int(read(3))
        self.unpack_boards(read(p_len))
  
  def tell(self,comm,args=None):
    c = commands
    s = "" 
    if comm in (c.CROSS,c.ZERO,c.DEFEAT,c.VICTORY,c.DRAW):
      s += comm 
      if comm in (c.DEFEAT,c.VICTORY):
        s += "".join(map(lambda a:"".join(map(str,a)),args))
    elif comm == c.POINT:
      s += comm+"".join(map(str,args))
    out = sys.stdout
    out.write(s)
    out.flush() # immediately send command
  
  def new(self):  
    c = commands
    b = self.board
    bs_db = self.boards
    bs_cross = []
    bs_zero = []
    
    listen = self.listen
    tell = self.tell
    
    b.clear()
    
    def user_move(val):
      listen()
      b.move(val,self.user_move)
      
    def ai_move(val):
      p = self.choose_move(val)
      tell(c.POINT,p)
      b.move(val,p)
      return p
    
    q = choice((USER,AI))
    if q == USER: 
      tell(c.CROSS)
      cross_move = lambda: user_move(CROSS)
      zero_move = lambda: ai_move(ZERO)
    else:
      tell(c.ZERO)
      cross_move = lambda: ai_move(CROSS)
      zero_move = lambda: user_move(ZERO)
 
    i = 0
    flag = EMPTY   
    comb = None # winning combination
    while True:
      cross_move()
      i+=1
      
      comb = b.result(CROSS)
      if comb:
        flag = CROSS
        break      
              
      if i==5: break # no more moves
      
      bs_cross.append(b.const())
      zero_move()
      bs_zero.append(b.const())      
      
      comb = b.result(ZERO)
      if comb:
        flag = ZERO
        break
   
    if flag != EMPTY:
      if flag == ZERO:
        inc = bs_zero
        dec = bs_cross
      else: # flag == CROSS:        
        inc = bs_cross
        dec = bs_zero          
      for i in inc:
        if i in bs_db: 
          bs_db[i]+=1
        else: bs_db[i]=1
      for d in dec:  
        if d in bs_db:
          bs_db[d]-=1
        else: bs_db[d]=-1
    
    res = EMPTY
    if (q==USER and flag==CROSS) or (q==AI and flag==ZERO): 
      tell(c.VICTORY,comb)
    elif (q==AI and flag==CROSS) or (q==USER and flag==ZERO):
      tell(c.DEFEAT,comb)
    else: tell(c.DRAW)  
      
  def choose_move(self,val):
    bs = self.boards
    b = self.board
    mvs = []
    
    s = -10000 
    
    for i in range(3):
      for j in range(3):
        p = (i,j)
        if b.empty(p):
          c = b.copy()
          c.move(val,p)
          c = c.const()
          if c not in bs:
            bs[c] = 0
          h = bs[c] 
          if h>s:
            mvs = [p]
            s = h
          if h==s:
            mvs.append(p)
            
    return choice(mvs)
    
  def unpack_boards(self,path):
    if self.boards_path:
      self.pack_boards()
    
    if os.path.exists(path) and os.path.getsize(path) > 0:    
      with open(path,"r") as file:  
        boards = pickle.load(file)
    else: 
      boards = {}
    self.boards = boards
    self.boards_path = path
    
  def pack_boards(self):
    with open(self.boards_path,"w") as file:
      pickle.dump(self.boards,file)
      
  def exit(self):
    # saving AI before exit 
    if self.boards_path: 
      self.pack_boards()
    sys.exit(0)
  
if __name__ == "__main__":
  g = Game()  
  g.start()