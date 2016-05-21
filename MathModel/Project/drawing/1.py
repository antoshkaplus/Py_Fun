
import Tkinter as tk
from tkFont import Font

# setting tkinter
main = tk.Tk()
font = Font(size=20,weight="bold")
# creating perfect coordinates
c_main = [500,230]
# spring setting
n = 10
dx = 30
x1, x2 = 165+90, 165+90
y1, y2 = 60, 200
c_c0 = [(x1+x2)/2+dx+20,(y1+y2)/2]
pts = []
for k in range(n):
  p = float(k)/(n-1)
  pts.append([x1*p+x2*(1-p) + (dx if k%2 else -dx),
              y1*p+y2*(1-p)])
c_spring = pts
c_surface = [50,200,450,220]
c_support = [[415,60],[425,60],[450,200],[390,200]]
c_beam = [90,55,420,65]
c_joint = [410,50,430,70]
c_ball = [50,20,130,100]
c_pulse = [[90,15],[90,-40]]
c_arrowshape = [10,15,10]
c_S = [110,-13]
c_m = [30,50]
c_2L = [165+90,40]
all = [c_main,c_spring,c_surface,c_support,c_beam,
       c_joint,c_ball,c_m,c_2L,c_pulse,c_S,c_c0] 

def scale(pts,d):
  for i in range(len(pts)):
    if type(pts[i]) == list:
      scale(pts[i],d)
    else:
      pts[i] *= d
      pts[i] = int(pts[i])
      
def shift(pts,dx,dy):
  for i in range(len(pts)):
    if type(pts[i]) == list:
      shift(pts[i],dx,dy)
    else:
      pts[i] += (dx if i%2==0 else dy)
      pts[i] = int(pts[i])
   
scale(all,1.4)   
shift(all,0,80)
      
canvas = tk.Canvas(main,bg="white",width=c_main[0],height=c_main[1])
canvas.pack()
canvas.create_line(*c_spring,**{"fill":"blue","width":5})  
canvas.create_text(*c_c0,**{"text":"c0","font":font})
canvas.create_rectangle(*c_surface,**{"fill":"green","width":0})
canvas.create_polygon(*c_support,**{"fill":"green","width":0})
canvas.create_text(*c_2L,**{"text":"2L","font":font})
canvas.create_rectangle(*c_beam,**{"fill":"brown","width":0})
canvas.create_oval(*c_joint,**{"fill":"red","width":0})
canvas.create_oval(*c_ball,**{"fill":"red","width":0})
canvas.create_text(*c_m,**{"text":"m","font":font})
canvas.create_line(*c_pulse,**{"width":5,"arrow":tk.FIRST,"arrowshape":c_arrowshape})
canvas.create_text(*c_S,**{"text":"S","font":font})

canvas.update()

canvas.postscript(file="rest.ps",width=c_main[0],height=c_main[1])

#main.mainloop()

