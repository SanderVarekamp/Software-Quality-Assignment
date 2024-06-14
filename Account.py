from datetime import date, datetime
import random
import sqlite3

from Database import Members
from Encrypt import Decrypt, Encrypt

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
        Decrypt("DataBase.db.enc", "VeryGoodPassWord", Members.SourceDB)
        with sqlite3.connect('DataBase.db') as conn:
            cur = conn.cursor()
            try:
                cur.execute('SELECT MemberID FROM Members')
                rows = cur.fetchall()
                existing_ids = [row[0] for row in rows]
                while randomNumb in existing_ids:
                    random_digits = [random.randint(0, 9) for _ in range(7)]
                    Numb9 = (Numb0 + Numb1 + sum(random_digits)) % 10
                    randomNumb = int(f"{Numb0}{Numb1}{''.join(map(str, random_digits))}{Numb9}")
            except:
                pass
        conn.close()
        Encrypt(Members.SourceDB, "VeryGoodPassWord")
        return randomNumb
    
    def Print(self):
        print("Username:", self.Username)
        print("Password Hash:",self.PasswordHash)
        print("Fullname:", self.FirstName, self.LastName)
        print("Age:",self.Age)
        print("Gender:",self.Gender)
        print("Weight:",self.Weight)
        print("Address:",self.Address, self.City)
        print("Email:",self.Email)
        print("Phone Number:",self.PhoneNumb)
        print("Account Type:",self.Type)