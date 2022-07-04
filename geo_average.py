#optimized geometric average for calls and puts O(n^3) complexity
import pricing_methods
import numpy as np
from dataclasses import dataclass
np.set_printoptions(suppress=True)

@dataclass
class node:
    w: float #weight out of 1
    S: float #Stock price currently
    Y: float #stock price product
    k: int #iteration

def geo_average(pricing_method, S_0, K, n, r, u, d):
    inc = 0
    p = ((1 + r - d)/(u - d))
    q = 1 - p
    queue = []
    queue.append(node(1, 1, 1, 0)) # 1 instead of S_0 cause linear scaling
    while(queue[0].k!=n):
        inc+=1
        up=node(queue[0].w*p, queue[0].S*u, queue[0].Y * queue[0].S*u, queue[0].k+1)
        down=node(queue[0].w*q, queue[0].S*d, queue[0].Y * queue[0].S*d, queue[0].k+1)
        flag1=True
        flag2=True
        for i in queue:
            match i:
                case node(S=up.S, Y=up.Y, k=up.k):
                    i.w+=up.w
                    flag1=False
                case node(S=down.S, Y=down.Y, k=down.k):
                    i.w+=down.w
                    flag2=False
        if(flag1):
            queue.append(up)
        if(flag2):
            queue.append(down)
        queue.pop(0)
    sum=0
    while(queue):
        sum+=queue[0].w*pricing_method(queue[0].Y ** (1/n), K)
        queue.pop(0)
    print(inc) #total nodes generated
    return (1/(r+1))**n * sum * S_0

#print(geo_average(call, 150, 150, 30, 0, 1.055, 0.945))
#print(geo_average(call, 150, 150, 10, 0.25, 2, 0.5)) #would of generate 1024 nodes, generates 385
#print(geo_average(call, 150, 150, 20, 0.25, 2, 0.5)) #would of generate 1048576 nodes, generates 6213
print(geo_average(pricing_methods.call, 150, 150, 40, 0.25, 2, 0.5))
#print(geo_average(call, 150, 150, 50, 0.25, 2, 0.5)) #would of generate 2251799813685248, generates 