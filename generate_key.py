from cryptography.fernet import Fernet

key = Fernet.generate_key()
with open("encryption.key", "wb") as key_file:
    key_file.write(key)

print("Key saved to encryption.key")
