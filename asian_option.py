#Does Asian arithmetic and Asian geometric options in up-down model
from dataclasses import dataclass
import random

@dataclass
class node:
    w: float #weight out of 1
    S: float #Stock price currently
    Z: float #Sum or Product of stock prices up to now
    k: int #iteration

def call(S_0, K):
    return max(0, S_0 - K)

def put(S_0, K):
    return max(0, K - S_0)

def chooser(S_0, K):
    return max(S_0 - K, K - S_0)

def asian_arithmetic(pricing_method, S_0, k, n, r, u, d):
    if(n==0):
        return pricing_method(S_0, k)
    p = ((1+r-d)/(u-d))
    q = 1 - p

    queue = []
    queue.append(node(1,S_0,0,0))
    while(queue[0].k!=n):
        up=node(queue[0].w*p, queue[0].S*u, queue[0].Z+queue[0].S*u, queue[0].k+1)
        down=node(queue[0].w*q, queue[0].S*d, queue[0].Z+queue[0].S*d, queue[0].k+1)
        queue.append(up)
        queue.append(down)
        queue.pop(0)

    #print(queue)
    #print(len(queue))

    sum=0
    while(queue):
        sum+=queue[0].w*pricing_method(queue[0].Z/(n),k)
        queue.pop(0)

    return (1/(1+r))**n*sum

def asian_geometric(pricing_method, S_0, K, n, r, u, d):
    inc = 0
    p = ((1 + r - d)/(u - d))
    q = 1 - p
    queue = []
    queue.append(node(1, S_0, 1, 0))
    while(queue[0].k!=n):
        inc+=1
        up=node(queue[0].w*p, queue[0].S*u, queue[0].Z * queue[0].S*u, queue[0].k+1)
        down=node(queue[0].w*q, queue[0].S*d, queue[0].Z * queue[0].S*d, queue[0].k+1)
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
        sum += queue[0].w * pricing_method(queue[0].Z ** (1/n), K)
        queue.pop(0)
    print(inc) #total nodes generated
    print("no interest: " + str(sum))
    return (1/(r+1))**n * sum 

def asian_arithmetic_montecarlo(pricing_method, S_0, k, n, r, u, d, iterations):
    p = ((1+r-d)/(u-d))
    sum = 0
    for i in range(iterations):
        x = node(1, S_0, 0, 0)    
        while (x.k!=n):
            if(random.random() < p):
                x.S*=u
                x.Z+=x.S
                x.k+=1
            else:
                x.S*=d
                x.Z+=x.S
                x.k+=1
        sum += pricing_method((x.Z/(n+1)),k)

    sum/=iterations
    return (1/(1+r))**n*sum

S_0 = 8 #initial price
k = 8 #strike
n = 2 #periods till maturity
r = 0.25 #interest rates (in decimal form)
u = 2 #upside factor
d = 0.5 #downside factor

#print(asian_arithmetic(call, S_0, k, n, r, u, d)) 
#print(asian_arithmetic_montecarlo(call, S_0, k, n, r, u, d, 1000000)) 
#print(asian_geometric(call, 10, 10, 2, 0.25, 2, 0.5))

#interest rates don't work as intended
def arithmetic_asian_bachlier(pricing_method, S_0, K, n, r, mu, beta):
    if(n==0):
        return pricing_method(S_0, K)
    inc = 0
    queue = []
    queue.append(node(1, S_0, S_0, 0))
    while(queue[0].k!=n):
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
        sum += queue[0].w * pricing_method((queue[0].Z/n), K)
        queue.pop(0)
    #print(inc) #total nodes generated
    #print("no interest: " + str(sum))
    return (1/(r+1))**n * sum

#print(arithmetic_asian_bachlier(call, 100, 120, 20, 0, 1, 3)) 
#print(asian_geometric(call, 100, 100, 5, 0, 1.0955, 1/1.0955)) 
print(asian_arithmetic(call, 100, 100, 5, 0, 1.0955, 1/1.0955)) 
#print(asian_arithmetic(call, 100, 100, 5, 0.25, 2, 0.5)) 
'''
class node:
    w: float #weight out of 1
    S: float #Stock price currently
    Z: float #Sum or Product of stock prices up to now
    k: int #iteration
'''