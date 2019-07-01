'''
    calculations
'''

q = []

a = [(1.2, 0.6), (2.6, 0.8), (15.1, 1.3)]
b = [(1.5, 3.2), (5.2, 2.5), (32.1, 5.1)]
c = [(6.2, 7.2), (62.5, 3.4), (254.2, 11.1)]

for x in a:
    q.append(x)

for x in b:
    q.append(x)

for x in c:
    q.append(x)

print(q)

q.sort(key = lambda x:x[0])

print(q)