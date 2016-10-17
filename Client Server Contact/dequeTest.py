#Deque test

from collections import deque

q = deque()
q.append('test1')
q.append('test2')
q.append('test3')

print len(q)
x = q.pop()
print x
print len(q)