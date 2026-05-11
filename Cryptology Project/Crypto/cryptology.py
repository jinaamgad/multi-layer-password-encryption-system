import os

from Crypto.Hash import SHA256
from Crypto.Cipher import DES, AES
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import base64

# ======================================================
#  RSA RAW DETERMINISTIC ENCRYPTION (NO RANDOM PADDING)
# ======================================================

def rsa_raw_encrypt(public_key, data):
    n = public_key.n
    e = public_key.e

    m = int.from_bytes(data, byteorder='big')
    c = pow(m, e, n)

    return c.to_bytes((n.bit_length() + 7) // 8, byteorder='big')


# ======================================================
#           PERMANENT SYMMETRIC KEYS
# ======================================================

if not os.path.exists("keys.bin"):
    print("Generating permanent keys (first time only)...")
    DES_KEY = b"12345678"          # 8 bytes
    AES_KEY = get_random_bytes(32) # AES-256
    with open("keys.bin", "wb") as f:
        f.write(DES_KEY + AES_KEY)
else:
    with open("keys.bin", "rb") as f:
        data = f.read()
        DES_KEY = data[:8]
        AES_KEY = data[8:40]


# ======================================================
#               RSA PUBLIC/PRIVATE KEYS
# ======================================================

if not os.path.exists("rsa_public.pem"):
    key = RSA.generate(2048)
    with open("rsa_public.pem", "wb") as f:
        f.write(key.publickey().export_key())
    with open("rsa_private.pem", "wb") as f:
        f.write(key.export_key())

rsa_public = RSA.import_key(open("rsa_public.pem", "rb").read())


# ======================================================
#                   REGISTER FUNCTION
# ======================================================

def register(username, password):
    try:
        hash_bytes = SHA256.new(password.encode()).digest()

        des_enc = DES.new(DES_KEY, DES.MODE_ECB).encrypt(pad(hash_bytes, 8))

        aes = AES.new(AES_KEY, AES.MODE_CBC)
        aes_enc = aes.encrypt(pad(des_enc, 16))

        rsa_enc = rsa_raw_encrypt(rsa_public, aes_enc)

        final_b64 = base64.b64encode(rsa_enc).decode()
        iv_b64 = base64.b64encode(aes.iv).decode()

        with open("users.txt", "a", encoding="utf-8") as f:
            f.write(f"{username}:{final_b64}:{iv_b64}\n")

        print(f"Registered successfully: {username}")
        return True
    except Exception as e:
        print(f"Registration failed: {e}")
        return False


# ======================================================
#                    LOGIN FUNCTION
# ======================================================

def login(username, password):
    if not os.path.exists("users.txt"):
        return False

    for line in open("users.txt", encoding="utf-8"):
        parts = line.strip().split(":")
        if len(parts) != 3:
            continue

        stored_user, stored_final, stored_iv = parts

        if stored_user == username:
            hash_bytes = SHA256.new(password.encode()).digest()
            des_enc = DES.new(DES_KEY, DES.MODE_ECB).encrypt(pad(hash_bytes, 8))

            iv = base64.b64decode(stored_iv)
            aes = AES.new(AES_KEY, AES.MODE_CBC, iv)
            aes_enc = aes.encrypt(pad(des_enc, 16))

            rsa_calc = rsa_raw_encrypt(rsa_public, aes_enc)
            calculated_b64 = base64.b64encode(rsa_calc).decode()

            if calculated_b64 == stored_final:
                return True
            else:
                return False

    return False


# ======================================================
#                         MENU
# ======================================================

if __name__ == "__main__":

    print("\n" + "="*60)
    print("   CRYPTOLOGY PROJECT - MULTI-LAYER PASSWORD SYSTEM")
    print("   SHA-256 → DES → AES-CBC → RSA (DETERMINISTIC)")
    print("="*60 + "\n")

    while True:
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("\nChoose (1-3): ").strip()

        if choice == "1":
            u = input("Username: ").strip()
            p = input("Password: ").strip()
            if u and p:
                register(u, p)
            else:
                print("Cannot be empty!")

        elif choice == "2":
            u = input("Username: ").strip()
            p = input("Password: ").strip()
            if u and p:
                login(u, p)
            else:
                print("Cannot be empty!")

        elif choice == "3":
            print("Thanks Dr. Marwa")
            break

        else:
            print("Invalid choice!")
