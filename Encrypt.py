import os
import sqlite3
import secrets
import glob
from datetime import date
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

class DBEncryptor:
    SALT_SIZE = 16
    KEY_SIZE = 32
    NONCE_SIZE = 12
    BACKEND = default_backend()

    def __init__(self, password: str):
        self.password = password

    def _generate_key(self, salt: bytes) -> bytes:
        kdf = Scrypt(
            salt=salt,
            length=self.KEY_SIZE,
            n=2**14,
            r=8,
            p=1,
            backend=self.BACKEND
        )
        key = kdf.derive(self.password.encode())
        return key

    def encrypt_file(self, file_path: str, IsBackup = False) -> str:
        with open(file_path, 'rb') as file:
            data = file.read()

        salt = secrets.token_bytes(self.SALT_SIZE)
        nonce = secrets.token_bytes(self.NONCE_SIZE)
        key = self._generate_key(salt)

        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()

        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=self.BACKEND)
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        encrypted_file_data = salt + nonce + encryptor.tag + encrypted_data
        if IsBackup:
            today = date.today()
            formatted_date = today.strftime("%d%m%y")
            count = 0
            encrypted_file_path = "Backups/" + formatted_date + "." + str(count) + '.dbBackup.enc.zip'
            files = glob.glob(os.path.join("Backups", '*'))
            for file_path in files:
                if os.path.isfile(file_path):
                    if encrypted_file_path == "Backups/" + os.path.basename(file_path):
                        count = count+1
                        encrypted_file_path = "Backups/" + formatted_date + "." + str(count) + '.dbBackup.enc.zip'
        else:
            encrypted_file_path = file_path + '.enc'

        with open(encrypted_file_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_file_data)

        if not IsBackup:
            open(file_path, 'wb').close()

        return encrypted_file_path

    def decrypt_file(self, encrypted_file_path: str, output_file_path: str) -> None:
        try:
            with open(encrypted_file_path, 'rb') as encrypted_file:
                encrypted_data = encrypted_file.read()

            salt = encrypted_data[:self.SALT_SIZE]
            nonce = encrypted_data[self.SALT_SIZE:self.SALT_SIZE + self.NONCE_SIZE]
            tag = encrypted_data[self.SALT_SIZE + self.NONCE_SIZE:self.SALT_SIZE + self.NONCE_SIZE + 16]
            ciphertext = encrypted_data[self.SALT_SIZE + self.NONCE_SIZE + 16:]

            key = self._generate_key(salt)

            cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=self.BACKEND)
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(ciphertext) + decryptor.finalize()

            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
            data = unpadder.update(padded_data) + unpadder.finalize()

            with open(output_file_path, 'wb') as output_file:
                output_file.write(data)
        except:
            return

    def read_db(self, db_file_path: str) -> None:
        conn = sqlite3.connect(db_file_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table_name in tables:
            table_name = table_name[0]
            print(f"Table: {table_name}")
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            print("Columns:")
            for column in columns:
                print(f" - {column[1]} ({column[2]})")
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()
            print("Rows:")
            for row in rows:
                print(row)
        conn.close()

def Encrypt(FilePathDB, Password):
    encryptor = DBEncryptor(Password)
    encrypted_file_path = encryptor.encrypt_file(FilePathDB)
    return encrypted_file_path

def EncryptBackup(FilePathDB, Password):
    encryptor = DBEncryptor(Password)
    encrypted_file_path = encryptor.encrypt_file(FilePathDB, True)
    return encrypted_file_path

def Decrypt(EncryptedFilePath, PassWord, DecryptedFilePath):
    encryptor = DBEncryptor(PassWord)
    encryptor.decrypt_file(EncryptedFilePath, DecryptedFilePath)
    return DecryptedFilePath
