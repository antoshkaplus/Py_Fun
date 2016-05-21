
This is my self-learning Tic-Tac-Toe game.
It learns by assigning score to board 
placing. All board placings are stored 
in dictionary and saved in file. 

Each game gathers board placings and if some player 
wins then score of his board placings increases by 1, 
if some player loses then score of his board placings 
decreases by 1.

Draw uncounts.
  

controlling:
  "n" - new game
  "b" - open file with boards (brain)
  press on square "to move"
  
Program consists of to parts: 
  - core (where AI decides how to move)  
  - client (user GUI)
  user launches view.py (user GUI), which lauches core.
  then this two processes communicate throw pipes 
  (one byte commands, data description and data) 
  
  
What did I learn?
  I learned multiprocessing communication throw pipes.
  I understood necessity of catching exception 
    (tell to company, that "go out" and saving data)
  I found out that for font must use predetermined
    sizes only (!!!no resizing!!!)
  Constants help to hide values. Some common constants 
    should be stand in separate file.
  Don't forget to flush streams. 
  Redirect stderr if uses more than one process because 
    there is no other way to see exceptions and errors  
    
  Look Before You Leap!
  
What do I need to learn deeply?
  How to work with exceptions.
  