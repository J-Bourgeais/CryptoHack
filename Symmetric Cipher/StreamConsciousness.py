import requests
from collections import Counter

URL = "https://aes.cryptohack.org/stream_consciousness//encrypt/"

def get_ciphertext():
    r = requests.get(URL)
    return bytes.fromhex(r.json()["ciphertext"])

def xor_bytes(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

# Step 1: Collect ciphertexts
ciphertexts = []
NUM_SAMPLES = 1000

print("[*] Collecting ciphertexts...")
for _ in range(NUM_SAMPLES):
    ct = get_ciphertext()
    ciphertexts.append(ct)

# Step 2: Try to identify candidate ciphertexts that might contain the flag
# Look for long ciphertexts (flag is usually longer than generic lines)
ciphertexts.sort(key=len, reverse=True)
long_ciphers = [ct for ct in ciphertexts if len(ct) >= 16]

print(f"[*] Found {len(long_ciphers)} long ciphertexts (possible flag candidates)")

# Step 3: Try each long ciphertext, assume it starts with "crypto{"
known_prefix = b"crypto{"

for idx, ct in enumerate(long_ciphers):
    ct_prefix = ct[:len(known_prefix)]
    keystream_guess = xor_bytes(ct_prefix, known_prefix)

    # Use guessed keystream to decrypt whole ciphertext
    decrypted = xor_bytes(ct, keystream_guess * (len(ct) // len(keystream_guess) + 1))

    try:
        decoded = decrypted.decode()
        if "crypto{" in decoded:
            print(f"\nFLAG FOUND in ciphertext #{idx}:")
            print(decoded)
            break
    except UnicodeDecodeError:
        continue
else:
    print("No flag found — try collecting more ciphertexts or tweak assumptions.")
