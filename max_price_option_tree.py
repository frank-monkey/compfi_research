from dataclasses import dataclass

S_0 = 8 #initial price
n = 10 #periods till maturity
r = 0.25 #interest rates (in decimal form)
u = 2 #upside factor
d = 0.5 #downside factor

p = ((1+r-d)/(u-d))
q = 1 - p

@dataclass
class node:
    w: float #weight out of 1
    S: float #Stock price currently
    Y: float #Max stock price
    k: int #iteration

queue = []
queue.append(node(1,S_0,S_0,0))
while(queue[0].k!=n):
    up=node(queue[0].w*p, queue[0].S*u, max(queue[0].S*u, queue[0].Y), queue[0].k+1)
    down=node(queue[0].w*q, queue[0].S*d, queue[0].Y, queue[0].k+1)
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

print(queue)
print(len(queue))

sum=0
while(queue):
    sum+=queue[0].w*queue[0].Y
    queue.pop(0)

sum += (1/(1+r))**n*sum

print(sum)