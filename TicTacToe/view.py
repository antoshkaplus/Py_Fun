
import tkFont
import Tkinter as tk
import tkFileDialog as tkFD
from tkMessageBox import showerror

import thread
from subprocess import Popen, PIPE
from multiprocessing import Queue

import os
import sys

import commands

EMPTY = "_"
CROSS = "x"
ZERO = "o"

COL_BG = "grey"
COL_CELL = "yellow"
COL_LINE = "black"
COL_CROSS = "red"
COL_ZERO = "green"
COL_SELECT = "blue"

COL_PANEL = "white"


class Board:
  def __init__(self):
    self.clear()
  
  def __getitem__(self,(i,j)):
    return self.b[i][j]  
  def __setitem__(self,(i,j),val):
    self.b[i][j] = val
  
  def clear(self):
    self.b = [[EMPTY]*3 for i in range(3)]

    
class Illustration(tk.Canvas):
  """
    val = text tag
    ij = identifier of text tag
  """
  def __init__(self,master,model):
    tk.Canvas.__init__(self,master,highlightthickness=0,bg=COL_BG)
    self.bind("<Configure>",lambda o:self.resize())
    self.font = tkFont.Font(family="Courier",weight=tkFont.BOLD)
    self.model = model
    self.board = model.board
    
  def resize(self):
    w = self.winfo_width()
    h = self.winfo_height()
    d = int(0.9*min(w,h))
    self.step = step = (d-1)/3
    self.indx = (w-step*3)/2
    self.indy = (h-step*3)/2
    self.size = step*3
    self.font.config(size=int(step*0.8))
    
    self.redraw()
    
  def redraw(self):
    self.delete(tk.ALL)
    
    step = self.step
    size = self.size
    cline = self.create_line
    crect = self.create_rectangle
    
    #bind = lambda id,i,j: self.tag_bind(id,"<Button-1>",lambda o: self.click(i,j))
    
    for k in range(0,size+1,step):
      cline(k,0,k,size,fill=COL_LINE)
      cline(0,k,size,k,fill=COL_LINE)
    
    get_id = self.get_id
    for i,ki in enumerate(range(0,size-1,step)):
      for j,kj in enumerate(range(0,size-1,step)):
        id = get_id(i,j)
        crect(kj+1,ki+1,kj+step,ki+step,width=0,fill=COL_CELL,tag=id)
        #bind(id,i,j)
    self.move(tk.ALL,self.indx,self.indy)
    self.bind("<Button-1>",self.click)
    self.update()
  
  def click(self,o):
    x,y = o.x,o.y
    s = self.step
    i,j = (y-self.indy)/s,(x-self.indx)/s
    if (0<=i<=2) and (0<=j<=2):
      self.model.user_move(i,j)
    
  def update(self):
    board = self.board
    set = self.set_value
    for i in range(3):
      for j in range(3):
        self.set_value(i,j)
  
  def set_value(self,i,j):
    board = self.board
    px = self.indx+(j+1/2.)*self.step
    py = self.indy+(i+1/2.)*self.step
    
    id = "v"+str(i)+str(j)
    self.delete(id)
    
    ctext = lambda s,col: self.create_text(px,py,
                                           font=self.font,
                                           text=s,fill=col,tags=(id,"val"))
    val = board[i,j]
    if val == CROSS:
      ctext("X",COL_CROSS)
    elif val == ZERO:
      ctext("O",COL_ZERO)
      
  def clear(self):
    self.delete("val") 
    self.deselect()
    
  def select(self,arr):
    """ arr - list of points to select """
    get_id = self.get_id
    iconf = self.itemconfig
    for p in arr:
      iconf(get_id(*p),fill=COL_SELECT)
      
  def get_id(self,i,j):
    return "id"+str(i)+str(j) 
      
  def deselect(self):
    getid = self.get_id
    icget = self.itemcget
    iconf = self.itemconfig
    selected = lambda id: icget(id,"fill")==COL_SELECT
    deselect = lambda id: iconf(id,fill=COL_CELL)
    for i in range(3):
      for j in range(3): 
        id = getid(i,j)
        if selected(id): deselect(id)


class Panel(tk.Frame):
  def __init__(self,master):  
    """ wins and loses - tk.IntVar """
    tk.Frame.__init__(self,master)
    font = self.font = tkFont.Font(family="Courier",size=16,weight=tkFont.BOLD)
    
    self.wins = wins = tk.StringVar()
    wins.set("wins: 000")
    self.loses = loses = tk.StringVar()
    loses.set("loses:000")
    
    labw = tk.Label(self,textvariable=wins,bg=COL_PANEL,anchor=tk.S,font=font)
    labl = tk.Label(self,textvariable=loses,bg=COL_PANEL,anchor=tk.N,font=font)
    labw.pack(expand=tk.YES,fill=tk.BOTH,side=tk.TOP)
    labl.pack(expand=tk.YES,fill=tk.BOTH,side=tk.TOP)
    self.labs = [labw,labl]
    
  def inc_wins(self):
    w = self.wins
    s = w.get()
    w.set(s[:-3]+("%03d" % (int(s[-3:])+1)))
  
  def inc_loses(self):
    l = self.loses
    s = l.get()
    l.set(s[:-3]+("%03d" % (int(s[-3:])+1)))
 
    
class Application:
  def __init__(self):
    self.board = Board()
    self.queue = Queue()
    
    root = tk.Tk()      
    root.protocol("WM_DELETE_WINDOW",self.exit)
    self.root = root
    
    panel = Panel(root)
    panel.pack(side=tk.RIGHT,expand=tk.YES,fill=tk.BOTH)
    self.panel = panel
    
    illu = Illustration(root,self) 
    illu.pack(side=tk.LEFT,expand=tk.YES,fill=tk.BOTH)
    self.illu = illu
       
    root.bind("n",lambda o: self.new())
    root.bind("b",lambda o: self.ask_boards())
    
    self.started = False
    
  def listen(self):
    c = commands
    read = self.ai_out.read
    put = self.queue.put
    while True:
      ch = read(1)
      if ch in (c.CROSS,c.ZERO,c.DRAW): 
        put(ch)
      elif ch in (c.VICTORY,c.DEFEAT):
        arr = map(int,read(6))
        comb = [map(int,arr[i:i+2]) for i in range(0,6,2)] 
        put(ch)
        put(comb)
      elif ch == c.POINT:
        p = map(int,read(2))
        put(ch)
        put(p)
      elif ch == c.EXIT:
        self.exit(1)
        
  def tell(self,comm,args=None):
    c = commands
    s = "" 
    if comm in (c.START,c.EXIT):
      s += comm
    elif comm == c.POINT:
      s += comm+"".join(map(str,args))
    elif comm == c.BOARDS:
      path = args[0]
      s += comm+("%03d"%len(path))+path
    self.ai_in.write(s)
    
  def launch_ai(self):
    try:
      head = os.path.split(sys.argv[0])[0]
      model = "model.py"
      error = "stderr_core.txt"
      path = os.path.join(head,model)
      p = Popen(args=["pythonw",path],
                stdin=PIPE,stdout=PIPE,stderr=open(os.path.join(head,error),"w"))
      self.ai_in = p.stdin
      self.ai_out = p.stdout
      thread.start_new_thread(self.listen,())
    except: 
      self.exit(1)
      
  def start(self):  
    self.launch_ai()
    self.root.after(100,self.update)
    self.root.after(200,self.new)
    self.root.mainloop()
  
  def update(self):
    c = commands
    q = self.queue
    if not q.empty():
      comm = q.get()
      if comm in (c.CROSS,c.ZERO):
        u,ai = (CROSS,ZERO) if comm == c.CROSS else (ZERO,CROSS)        
        self.val_user = u
        self.val_ai = ai
      elif comm == c.POINT:
        i,j = q.get(block=True)
        self.board[i,j] = self.val_ai
        self.illu.set_value(i,j)
      elif comm in (c.VICTORY,c.DEFEAT,c.DRAW):
        if not (comm == c.DRAW):
          if comm == c.VICTORY:
            self.panel.inc_wins()
          else: # c.DEFEAT
            self.panel.inc_loses()
          arr = q.get(block=True)
          self.illu.select(arr)  
        self.started = False
    self.root.after_idle(self.update)
  
  def ask_boards(self):
    c = commands
    path = tkFD.askopenfilename(initialdir=os.path.split(sys.argv[0])[0])
    if path: self.tell(c.BOARDS,(path,))
  
  def new(self):
    self.started = True
    c = commands
    self.board.clear()
    self.illu.clear()
    self.tell(c.START)
  
  def user_move(self,i,j):
    try:
      c = commands
      board = self.board
      
      user = self.val_user
      if board[i,j] == EMPTY and self.started:
        board[i,j] = user
        self.illu.set_value(i,j)
        self.tell(c.POINT,(i,j))
    except:
      self.exit(1)
      
  def exit(self,val=0):
    try:
      if val != 0: 
        showerror("Error!","Sorry man... Not this time")
      c = commands
      self.tell(c.EXIT)
    finally:
      sys.exit()
  
  
if __name__ == "__main__":
  app = Application()
  app.start()
  