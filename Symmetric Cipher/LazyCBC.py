import requests
from Crypto.Cipher import AES
from binascii import unhexlify



plain = (b'a'*(16*3)).hex()
print(plain)
cipher = 'b5f50831e235181c2d41d2181700e635deeb695f3162fa27d9b592411a581ac34dee45cbadf38a798bac923cd2793a2d'
fake_cipher = cipher[:32] + '0'*32 + cipher[:32]
print(fake_cipher)
fake_plain = '616161616161616161616161616161615bb48b0050bca96eb613172eaa928638cda711cb88dc6eb004694f93f6d22923'
fake_plain = bytes.fromhex(fake_plain)
iv = [0]*16
for i in range(len(iv)):
   iv[i] = fake_plain[i] ^ fake_plain[32+i] #chiantos, je le fais à la main
   
print(iv.hex())


   
   


# The iv is the key.
# the equations are : 
# key = iv = d(c0) ^ p0

# p0 = d(c0) ^ iv
# p1 = d(c1) ^ c0 
# p2 = d(c2) ^ c1

# if c1=0 and c2=c0, we can have : 
#     p0 ^ p2 = d(c0) ^ iv ^ d(c0) = iv = key
    
# We need to create something with these caracteristics, and xor p0 and P2.filter

# we create a plaintext with 3 blocks : all a's --> 48 a --> 48x61 en hex.

# on le cypher (avec encrypt), et puis on le modifie pour avoir les caractéristiques voulues : c1=0 et C2=C0

# fake_cipher = cipher[:32] + '0'*32 + cipher[:32]

# On le decrypt. Ca nous dis que ca va pas et ca nous donne le plaintext associé 
# On peut donc prendre p0 et p2, les XOR. On a donc le iv, qui est donc egal à la clé. 
# On demange le flag, on l'a en hex, on le decode et c'est bon !