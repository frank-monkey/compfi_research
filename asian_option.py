from dataclasses import dataclass
import random

@dataclass
class node:
    w: float #weight out of 1
    S: float #Stock price currently
    Z: float #Sum of stock prices up to now
    k: int #iteration

def call(S_0, K):
    return max(0, S_0 - K)

def put(S_0, K):
    return max(0, K - S_0)

def chooser(S_0, K):
    return max(S_0 - K, K - S_0)

def asian_opt(pricing_method, S_0, k, n, r, u, d):
    p = ((1+r-d)/(u-d))
    q = 1 - p

    queue = []
    queue.append(node(1,S_0,S_0,0))
    while(queue[0].k!=n):
        up=node(queue[0].w*p, queue[0].S*u, queue[0].Z+queue[0].S*u, queue[0].k+1)
        down=node(queue[0].w*q, queue[0].S*d, queue[0].Z+queue[0].S*d, queue[0].k+1)
        queue.append(up)
        queue.append(down)
        queue.pop(0)

    print(queue)
    print(len(queue))

    sum=0
    while(queue):
        sum+=queue[0].w*pricing_method(queue[0].Z/(n+1),k)
        queue.pop(0)

    return (1/(1+r))**n*sum

def asian_opt_montecarlo(pricing_method, S_0, k, n, r, u, d, iterations):
    p = ((1+r-d)/(u-d))
    q = 1 - p

    sum = 0
    for i in range(iterations):
        x = node(1, S_0, S_0, 0)    
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
n = 10 #periods till maturity
r = 0.25 #interest rates (in decimal form)
u = 2 #upside factor
d = 0.5 #downside factor

print(asian_opt(call, S_0, k, n, r, u, d)) 
print(asian_opt_montecarlo(call, S_0, k, n, r, u, d, 100000)) 