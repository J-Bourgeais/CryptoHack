import hashlib

N_ROUNDS = 10

from AES import (
    bytes2matrix, matrix2bytes,
    inv_shift_rows, sub_bytes, inv_s_box, s_box,
    add_round_key, inv_mix_columns
)

# Your 32-byte ciphertext (2 AES blocks)
ciphertext_hex = "c92b7734070205bdf6c0087a751466ec13ae15e6f1bcdd3f3a535ec0f4bbae66"
ciphertext = bytes.fromhex(ciphertext_hex)

def expand_key(master_key):
    r_con = (
        0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
        0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
        0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
        0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
    )

    key_columns = bytes2matrix(master_key)
    iteration_size = len(master_key) // 4
    i = 1
    while len(key_columns) < (N_ROUNDS + 1) * 4:
        word = list(key_columns[-1])
        if len(key_columns) % iteration_size == 0:
            word.append(word.pop(0))
            word = [s_box[b] for b in word]
            word[0] ^= r_con[i]
            i += 1
        word = bytes(i ^ j for i, j in zip(word, key_columns[-iteration_size]))
        key_columns.append(word)
    return [key_columns[4*i : 4*(i+1)] for i in range(len(key_columns) // 4)]

def decrypt_block(key, ciphertext_block):
    round_keys = expand_key(key)
    state = bytes2matrix(ciphertext_block)
    state = add_round_key(state, round_keys[-1])
    for i in range(N_ROUNDS - 1, 0, -1):
        inv_shift_rows(state)
        state = sub_bytes(state, sbox=inv_s_box)
        state = add_round_key(state, round_keys[i])
        inv_mix_columns(state)
    inv_shift_rows(state)
    state = sub_bytes(state, sbox=inv_s_box)
    state = add_round_key(state, round_keys[0])
    return matrix2bytes(state)

# Brute-force using the wordlist
with open(r"C:\Users\bourg\OneDrive\Bureau\CryptoHack\word.txt", "r", encoding="utf-8") as f:
    words = [line.strip() for line in f]

for word in words:
    key_candidate = hashlib.md5(word.encode()).digest()
    
    # Decrypt all 16-byte blocks
    decrypted = b""
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]
        decrypted += decrypt_block(key_candidate, block)

    if b"crypto{" in decrypted:
        print(f"\nFOUND!")
        print(f"Word: {word}")
        print(f"Password Hash (MD5): {key_candidate.hex()}")
        print(f"Plaintext: {decrypted.decode(errors='ignore')}")
        break
