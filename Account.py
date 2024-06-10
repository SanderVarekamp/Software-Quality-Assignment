from datetime import date, datetime
import random
import sqlite3

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
        self.MemberID = Account.GenerateId()

    def GenerateId():
        today = datetime.now().year
        RNumbers = ""
        RNumbers += str(today)[-2:-1]
        RNumbers += str(today)[-1:]
        for x in range(7):
            RNumbers += str(random.randint(0,9))

        TotalNumber = 0
        for x in range(len(RNumbers)):
            TotalNumber += int(RNumbers[x:x+1])

        RNumbers += str(TotalNumber%10)
        RNumbers = int(RNumbers)

        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute("SELECT MemberID FROM Members WHERE MemberID = ?",(RNumbers,))
        rows = cursor.fetchall()
        connection.close()
        # for row in rows:
        #     print(row)
        if len(rows) > 0:
            return Account.GenerateId()
        return RNumbers
    
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