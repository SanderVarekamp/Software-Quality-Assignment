from datetime import date, datetime
import random
import sqlite3
from Database import Members
#from Database import Members
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from binascii import hexlify, unhexlify
from Encrypt2 import EncryptNew

class Account:
    def __init__(self, Username, PasswordHash, FirstName, LastName, Age, Gender, Weight, Address, City, Email, PhoneNumb, Type = "Member", RegistrationDate = None, MemberID = None):
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
        if RegistrationDate == None:
            self.RegistrationDate = today.strftime("%d/%m/%Y")
        else:
            self.RegistrationDate = RegistrationDate
        if MemberID == None:
            self.MemberID = self.GenerateMemberID()
        else:
            self.MemberID = MemberID

    def GenerateMemberID(self):
        print(self.RegistrationDate)
        input()
        Numb0 = int(str(self.RegistrationDate)[8])
        Numb1 = int(str(self.RegistrationDate)[9])
        random_digits = [random.randint(0, 9) for _ in range(7)]
        Numb9 = (Numb0 + Numb1 + sum(random_digits)) % 10
        randomNumb = int(f"{Numb0}{Numb1}{''.join(map(str, random_digits))}{Numb9}")
        #Decrypt(Members.EncryptedDB, Members.HardCodePassword, Members.SourceDB)
        print("1")
        EncryptNew().DecryptAll("Members")
        print("2")
        
        conn = None
        try:
            conn = sqlite3.connect(Members.SourceDB)
            cur = conn.cursor()
            try:
                cur.execute('SELECT MemberID FROM Decrypted')
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
            EncryptNew().DeleteDecrypted()
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
        if self.RegistrationDate == None:
            self.RegistrationDate = date.today().strftime("%d/%m/%Y")
        if self.MemberID == None:
            self.MemberID = self.GenerateMemberID()
        words = [self.Username, self.PasswordHash, self.FirstName, self.LastName, str(self.Age), self.Gender, str(self.Weight), self.Address, self.City, self.Email, self.PhoneNumb, self.Type, self.RegistrationDate, str(self.MemberID)]
        for word in words:
            if word == self.PasswordHash:
                encrypted_data.append(word)
            else:
                data_to_encrypt = word.encode('utf-8')  
                cipher_rsa = PKCS1_OAEP.new(public_key)
                encrypted = cipher_rsa.encrypt(data_to_encrypt)
                encrypted_data.append(hexlify(encrypted))
        return encrypted_data
    