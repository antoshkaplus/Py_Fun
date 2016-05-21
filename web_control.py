
kWebsites = [
"justanimedubbed.tv",
"twitch.tv",
"youtube.com",
"netfix.com",
"netflix.com",

"ej.ru",
"kasparov.ru",
"habrahabr.ru",    
]

def add_web_derivatives(websites):
    webs = list(websites)
    for w in websites:
        webs.append("www." + w)
    return webs
    
kWebsites = add_web_derivatives(kWebsites)

# my hosts will be placed betwwen strings of ### strings

kSeparator = "\n###\n"
def remove_hosts(s):
   start = s.find(kSeparator)
   finish = s.rfind(kSeparator) + len(kSeparator)
   if (start == -1 or finish == -1): return s
   return s[:start] + s[finish:]

def add_hosts(s):
    s += kSeparator
    s += "\n".join(map(lambda x: "127.0.0.1 " + x, kWebsites))
    s += kSeparator
    return s

#kTurnOffTime = 

import os
import datetime as dt
import time

while True:
    hosts_file = open("/etc/hosts")
    s = hosts_file.read()
    hosts_file.close()
    
    time_to_sleep = 0
    cur_dt = dt.datetime.now()
    if cur_dt.hour < 11:
        # everything should be open
        s = remove_hosts(s)
        #time_to_sleep = ((11 - cur_dt.hour)*60 - cur_dt.minute)*60
    elif cur_dt.hour < 19:
        # everything should be closed 
        s = add_hosts(s)
        #time_to_sleep = ((19 - cur_dt.hour)*60 - cur_dt.minute)*60
    else:
        # everything should be open
        s = remove_hosts(s)  
        #time_to_sleep = ((24 - cur_dt.hour + 11)*60 - cur_dt.minute)*60
    
    tmp_file = open('/tmp/hosts.tmp', 'w')
    tmp_file.write(s)
    tmp_file.close()
    
    os.system("sudo mv /tmp/hosts.tmp /etc/hosts")
    os.system("sudo dscacheutil -flushcache")
    break
    time.sleep(time_to_sleep)
    

