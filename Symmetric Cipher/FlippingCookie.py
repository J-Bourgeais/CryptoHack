from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from datetime import datetime, timedelta

def flip(cookie_hex, plain):
    cookie = bytes.fromhex(cookie_hex)
    cipher_fake = list(cookie)
    iv = list(cookie[:16])  # Start with the original IV

    fake = b'admin=True'


    start = plain.find(b'admin=False')

    for i in range(len(fake)):
        # Modify IV to flip decrypted plaintext
        iv[start + i] ^= plain[start + i] ^ fake[i]

    iv_hex = bytes(iv).hex()
    return cookie_hex[32:], iv_hex  # return ciphertext (block 1+2), modified IV

expires_at = str(int((datetime.today() + timedelta(days=1)).timestamp()))
plain = f"admin=False;expiry={expires_at}".encode()

# Original full cookie from get_cookie()
cookie = '67f1926c9bc24c8d0adc6d2a4e0485fe5b1fa0cbd1861eeafbbfa1365587f946d89dc48cd87b4260a95211b4a45df4a9'

ciphertext, iv = flip(cookie, plain)

print("ciphertext:", ciphertext)
print("iv:", iv)

