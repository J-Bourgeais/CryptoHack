import requests



#Attention : présence de _ dans le mdp --> bug avec json 

BASE_URL = "https://aes.cryptohack.org/ecb_oracle/encrypt/"

def query_oracle(plaintext_hex):
    url = BASE_URL + plaintext_hex + "/"
    r = requests.get(url)
    print("Querying:", url)
    if "ciphertext" in r.json():
        print("Response received successfully.")
        return r.json()["ciphertext"]
    else:
        print("Error:", r.json())
        return None

def get_block(ciphertext_hex, block_num=0):
    # Returns the nth 16-byte block (32 hex chars per block)
    return ciphertext_hex[block_num*32:(block_num+1)*32]

def find_flag():
    block_size = 16
    known_flag = b'crypto{p3n6u1n5'
    # Let's assume flag length up to 40 (adjust if needed)
    max_flag_len = 40

    for i in range(max_flag_len):
        # Number of bytes to pad to align next unknown byte at the end of a block
        pad_len = (block_size - (len(known_flag) % block_size) - 1)
        prefix = b"A" * pad_len

        # Encrypt prefix only to get target block
        target_cipher = query_oracle(prefix.hex())
        if not target_cipher:
            break

        block_num = len(prefix + known_flag) // block_size
        target_block = get_block(target_cipher, block_num)

        # Build dictionary of ciphertext blocks for guesses
        dictionary = {}
        print("guessing...")
        for guess in range(256):
            guess_byte = bytes([guess])
            attempt = prefix + known_flag + guess_byte
            ct = query_oracle(attempt.hex())
            if not ct:
                continue
            dictionary[get_block(ct, block_num)] = guess_byte

        if target_block in dictionary:
            known_flag += dictionary[target_block]
            print(f"Recovered so far: {known_flag}")
            # Stop if we guess the padding or flag ends early
            if known_flag.endswith(b"}"):
                break
        else:
            print("No match found, stopping.")
            break

    return known_flag

if __name__ == "__main__":
    flag = find_flag()
    print("Recovered flag:", flag.decode())
