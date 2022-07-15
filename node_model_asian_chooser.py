#Does Asian arithmetic and Asian geometric options in up-down model
from dataclasses import dataclass
import random
import asian_option as ao

@dataclass
class node:
    w: float #weight out of 1
    S: float #Stock price currently
    Z: float #Sum or Product of stock prices up to now
    k: int #iteration

#interest rates don't work as intended
#issues if n==tau
def arithmetic_asian_tail_chooser(S_0, K, n, tau, r, mu, beta):
    if(n-tau==0):
        return max(ao.arithmetic_asian_bachlier(ao.call, S_0, K, n, r, mu, beta), ao.arithmetic_asian_bachlier(ao.put, S_0, K, n, r, mu, beta))
    inc = 0
    queue = []
    queue.append(node(1, S_0, 0, 0)) #prices dont matter till tau
    while(queue[0].k!=tau):
        inc+=1
        up_price = queue[0].S*mu+beta
        down_price = queue[0].S*mu-beta
        p = (((1 + r)*queue[0].S - down_price)/(up_price - down_price))
        q = 1 - p
        up=node(queue[0].w*p, up_price, 0, queue[0].k+1)
        down=node(queue[0].w*q, down_price, 0, queue[0].k+1)
        flag1=True
        flag2=True
        for i in queue:
            match i:
                case node(S=up.S, Z=up.Z, k=up.k):
                    i.w+=up.w
                    flag1=False
                case node(S=down.S, Z=down.Z, k=down.k):
                    i.w+=down.w
                    flag2=False
        if(flag1):
            queue.append(up)
        if(flag2):
            queue.append(down)
        queue.pop(0)
    sum=0
    #print(queue)
    while(queue):
        sum += queue[0].w * max(ao.arithmetic_asian_bachlier(ao.call, queue[0].S, K, n-tau, r, mu, beta), ao.arithmetic_asian_bachlier(ao.put, queue[0].S, K, n-tau, r, mu, beta))
        queue.pop(0)
    #print(inc) #total nodes generated
    #print("no interest: " + str(sum))
    return (1/(r+1))**n * sum

#interest rates don't work as intended
#NOT FINISHED
def arithmetic_asian_full_chooser(S_0, K, n, tau, r, mu, beta):
    op = lambda S, periods : max(ao.arithmetic_asian_bachlier(ao.call, S, K, periods, r, mu, beta), ao.arithmetic_asian_bachlier(ao.put, S, K, periods, r, mu, beta))
    if(n-tau==0):
        return max(ao.arithmetic_asian_bachlier(ao.call, S_0, K, n, r, mu, beta), ao.arithmetic_asian_bachlier(ao.put, S_0, K, n, r, mu, beta))
    inc = 0
    queue = []
    queue.append(node(1, S_0, S_0, 0)) #prices dont matter till tau
    while(queue[0].k!=tau):
        inc+=1
        up_price = queue[0].S*mu+beta
        down_price = queue[0].S*mu-beta
        p = (((1 + r)*queue[0].S - down_price)/(up_price - down_price))
        q = 1 - p
        up=node(queue[0].w*p, up_price, queue[0].Z+up_price, queue[0].k+1)
        down=node(queue[0].w*q, down_price, queue[0].Z+down_price, queue[0].k+1)
        flag1=True
        flag2=True
        for i in queue:
            match i:
                case node(S=up.S, Z=up.Z, k=up.k):
                    i.w+=up.w
                    flag1=False
                case node(S=down.S, Z=down.Z, k=down.k):
                    i.w+=down.w
                    flag2=False
        if(flag1):
            queue.append(up)
        if(flag2):
            queue.append(down)
        queue.pop(0)
    sum=0
    #print(queue)
    while(queue):
        sum += queue[0].w * ((n-tau)*max(ao.arithmetic_asian_bachlier(ao.call, queue[0].S, K, n-tau, r, mu, beta), ao.arithmetic_asian_bachlier(ao.put, queue[0].S, K, n-tau, r, mu, beta)))
        queue.pop(0)
    #print(inc) #total nodes generated
    #print("no interest: " + str(sum))
    return (1/(r+1))**n * sum

print(arithmetic_asian_tail_chooser(100, 120, 10, 10, 0, 1, 3)) 
print(arithmetic_asian_full_chooser(100, 120, 10, 10, 0, 1, 3)) 