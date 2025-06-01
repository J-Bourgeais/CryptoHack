import math
##CRYPTOHACK

##------- Find the GCD - Greatest Common divisor
print(math.gcd(66528, 52920))

##------- extended Euclidean algorithm - u, v such as a⋅u+b⋅v=gcd(a,b)
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0  # gcd, u, v
    else:
        gcd, u1, v1 = extended_gcd(b, a % b)
        u = v1
        v = u1 - (a // b) * v1
        return gcd, u, v

p = 26513
q = 32321

gcd, u, v = extended_gcd(p, q)
print(u,v)


##-------- Modulo

print(8146798528947%17)
print(11%6)