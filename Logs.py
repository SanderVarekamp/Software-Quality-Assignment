from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from binascii import hexlify, unhexlify
from datetime import date, datetime


class Logs:
    def __init__(self, username: str, activity: str, info: str, sus: bool, datum = None, time = None, ):
        if datum is None:
            self.date = date.today().strftime("%d/%m/%Y")
        else:
            self.date = datum
        if time is None:
            self.time = datetime.now().strftime("%H:%M:%S")
        else:
            self.time = time
        self.username = username
        self.activity = activity
        self.info = info
        self.suspicious = sus

    def Encrypt(self, public_key) -> list:
        encrypted_data = []
        words = [self.date, self.time, self.username, self.activity, self.info, str(self.suspicious)]
        for word in words:
            try:
                data_to_encrypt = word.encode('utf-8')  
                cipher_rsa = PKCS1_OAEP.new(public_key)
                encrypted = cipher_rsa.encrypt(data_to_encrypt)
                encrypted_data.append(hexlify(encrypted))
            except:
                pass
        return encrypted_data
    
    def Print(self):
        print("Date:", self.date, "|" "Time:", self.time, "|" "Username:", self.username, "|" "Activity:", self.activity, "|" "Information:", self.info, "|" "Suspicious:", self.suspicious)