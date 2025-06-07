import string
import time
import requests

BASE = "https://aes.cryptohack.org/ctrime/"

# alphabet élargi (ordre inchangé)
alphabet = '}' + '!' + '_' + '@' + '?' + string.ascii_uppercase + string.digits + string.ascii_lowercase

def safe_get(url):
    try:
        r = requests.get(url)
        r.raise_for_status()  # Vérifie le code HTTP (200 OK attendu)
        return r.json()       # Essaye de parser le JSON
    except requests.exceptions.RequestException as e:
        print(f"Erreur réseau / HTTP : {e}")
    except ValueError:
        print(f"Réponse non JSON ou mal formée : {r.text}")
    return None

def bruteforce():
    flag = b'crypto{CRIME'
    # Première requête pour récupérer la longueur de référence
    data = safe_get(f"{BASE}/encrypt/{flag.hex()}/")
    if not data:
        print("Erreur initiale, impossible de récupérer le ciphertext.")
        return
    
    cipher = bytes.fromhex(data['ciphertext'])
    mi = len(cipher)

    while True:
        for c in alphabet:
            test_input = flag + c.encode()
            data = safe_get(f"{BASE}/encrypt/{test_input.hex()}/")
            if not data:
                print("Erreur lors de la requête, on réessaie dans 2s...")
                time.sleep(2)
                continue  # réessayer la même lettre

            cipher = bytes.fromhex(data['ciphertext'])
            print(f"Test '{c}': longueur ciphertext = {len(cipher)}")

            if len(cipher) == mi:
                flag += c.encode()
                mi = len(cipher)
                print(f"Lettre trouvée : '{c}', flag partiel : {flag.decode()}")
                break

            if c == alphabet[-1]:
                # Si aucune lettre n'a maintenu la taille, on considère qu'on a fini ou qu'il faut ajuster
                mi += 2
                print(f"Aucune lettre trouvée, ajustement longueur mi={mi}")

            time.sleep(0.5)  # anti rate-limit

        if flag.endswith(b'}'):
            print(f"Flag complet trouvé : {flag.decode()}")
            break
        else:
            print("On continue la recherche...")

bruteforce()
