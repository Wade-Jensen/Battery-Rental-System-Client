#Url Contact
import Queue

q = Queue.Queue()

try:
    task = q.get(False)
except Queue.Empty:
    # Handle empty queue here
    pass
else:
    # Handle task here and call q.task_done()