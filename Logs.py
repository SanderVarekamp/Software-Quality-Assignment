from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from binascii import hexlify, unhexlify
from datetime import date, datetime


class Logs:
    def __init__(self, username: str, activity: str, info: str, sus: bool):
        self.date = date.today().strftime("%d/%m/%Y")
        self.time = datetime.now().strftime("%H:%M:%S")
        self.username = username
        self.activity = activity
        self.info = info
        self.suspicious = sus

    def Encrypt(self, public_key) -> list:
        encrypted_data = []
        words = [self.date, self.time, self.username, self.activity, self.info, str(self.suspicious)]
        for word in words:
            data_to_encrypt = word.encode('utf-8')  
            cipher_rsa = PKCS1_OAEP.new(public_key)
            encrypted = cipher_rsa.encrypt(data_to_encrypt)
            encrypted_data.append(hexlify(encrypted))
        return encrypted_data