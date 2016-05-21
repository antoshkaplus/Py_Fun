

# GUI that displays data produced and queued by worker threads

import thread, Queue as queue, time
dataQueue = queue.Queue()    # infinite size

def producer(id):
  for i in range(5):
    time.sleep(0.1)
    print('put')
    dataQueue.put('[producer id=%d, count=%d]' % (id, i))

def consumer(root):
  while not dataQueue.empty():
    data = dataQueue.get(block=False)
    root.insert('end', 'consumer got => %s\n' % str(data))
    root.see('end')
  root.after(250, lambda: consumer(root))    # 4 times per sec

def makethreads():
  for i in range(4):
    thread.start_new_thread(producer, (i,))

       
if __name__ == '__main__':
  # main GUI thread: spawn batch of worker threads on each mouse click
  from ScrolledText import ScrolledText
  root = ScrolledText()
  root.pack()
  root.bind('<Button-1>', lambda event: makethreads())
  consumer(root)                       # start queue check loop in main thread
  root.mainloop()                      # pop-up window, enter tk event loop
  
  