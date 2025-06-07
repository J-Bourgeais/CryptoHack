import requests

BASE = "https://aes.cryptohack.org/symmetry/"

#get encrypted flag
r = requests.get(f"{BASE}/encrypt_flag/")
cipher = bytes.fromhex(r.json()['ciphertext'])
iv = cipher[:16]
enc_flag = cipher[16:]

#get keystream by sending plaintext = 0x00 * len(enc_flag) with same IV
plaintext = '00' * len(enc_flag)
r2 = requests.get(f"{BASE}/encrypt/{plaintext}/{iv.hex()}/")
keystream = bytes.fromhex(r2.json()['ciphertext'])

#decrypt flag
flag = bytes(a ^ b for a, b in zip(enc_flag, keystream))
print("FLAG:", flag.decode())
