"""
Commands for interprocessing communications
"""

# AI commands

# which values play user
CROSS = "a" 
ZERO = "z"

# after command sends 6 bytes 
# for 3 (row,col) cells which shows 
# ai or user winning combination 
DEFEAT = "d"  # user defeat 
VICTORY = "v" # user victory

DRAW = "r" 


# USER commands 

# start new game
START = "s"

# after command sends 3 bytes 
# for path length path of file 
# where are boards stand then 
# path sends
BOARDS = "b"

# BOTH commands
EXIT = "e"

# after command sends 2 byte
# for (row,col) move
POINT = "p" # make move



