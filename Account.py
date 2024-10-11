from datetime import date, datetime
import random
import sqlite3
from Database import Members
#from Database import Members
from Encrypt import Decrypt, Encrypt
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from binascii import hexlify, unhexlify

class Account:
    def __init__(self, Username, PasswordHash, FirstName, LastName, Age, Gender, Weight, Address, City, Email, PhoneNumb, Type = "Member"):
        today = date.today()
        self.Username = Username
        self.PasswordHash = PasswordHash
        self.FirstName = FirstName
        self.LastName = LastName
        self.Age = Age
        self.Gender = Gender
        self.Weight = Weight
        self.Address = Address
        self.City = City
        self.Email = Email
        self.PhoneNumb = PhoneNumb
        self.Type = Type
        self.RegistrationDate = today.strftime("%d/%m/%Y")
        self.MemberID = self.GenerateMemberID()

    def GenerateMemberID(self):
        Numb0 = int(str(self.RegistrationDate)[8])
        Numb1 = int(str(self.RegistrationDate)[9])
        random_digits = [random.randint(0, 9) for _ in range(7)]
        Numb9 = (Numb0 + Numb1 + sum(random_digits)) % 10
        randomNumb = int(f"{Numb0}{Numb1}{''.join(map(str, random_digits))}{Numb9}")
        Decrypt(Members.EncryptedDB, Members.HardCodePassword, Members.SourceDB)
        
        conn = None
        try:
            conn = sqlite3.connect(Members.SourceDB)
            cur = conn.cursor()
            try:
                cur.execute('SELECT MemberID FROM Members')
                rows = cur.fetchall()
                existing_ids = [row[0] for row in rows]
                while randomNumb in existing_ids:
                    random_digits = [random.randint(0, 9) for _ in range(7)]
                    Numb9 = (Numb0 + Numb1 + sum(random_digits)) % 10
                    randomNumb = int(f"{Numb0}{Numb1}{''.join(map(str, random_digits))}{Numb9}")
            except Exception as e:
                print(f"An error occurred while querying the database: {e}")
        except Exception as e:
            print(f"An error occurred while connecting to the database: {e}")
        finally:
            if conn:
                conn.close()
            Encrypt(Members.SourceDB, Members.HardCodePassword)
            return randomNumb
    
    def Print(self):
        print("Username:", self.Username)
        print("Fullname:", self.FirstName, self.LastName)
        print("Age:",self.Age)
        print("Gender:",self.Gender)
        print("Weight:",self.Weight)
        print("Address:",self.Address, self.City)
        print("Email:",self.Email)
        print("Phone Number:",self.PhoneNumb)
        print("Account Type:",self.Type)
        print("Registration date: ", self.RegistrationDate)
        print("Member ID:", self.MemberID)

    def Encrypt(self, public_key) -> list:
        encrypted_data = []
        words = [self.Username, self.FirstName, self.LastName, str(self.Age), self.Gender, str(self.Weight), self.Address, self.City, self.Email, self.PhoneNumb, self.Type, self.RegistrationDate, str(self.MemberID)]
        for word in words:
            data_to_encrypt = word.encode('utf-8')  
            cipher_rsa = PKCS1_OAEP.new(public_key)
            encrypted = cipher_rsa.encrypt(data_to_encrypt)
            encrypted_data.append(hexlify(encrypted))
        return encrypted_data
    