from datetime import date
import random
import sqlite3

class Employee:
    def __init__(self, FirstName, LastName, Age, Gender, Weight, Address, City, Email, PhoneNumb, IsConsult, IsSysAdm, IsSupAdm):
        today = date.today()
        self.FirstName = FirstName
        self.LastName = LastName
        self.Age = Age
        self.Gender = Gender
        self.Weight = Weight
        self.Address = Address
        self.City = City
        self.Email = Email
        self.PhoneNumb = PhoneNumb
        self.IsConsult = IsConsult
        self.IsSysAdm = IsSysAdm
        self.IsSupAdm = IsSupAdm
        self.RegistrationDate = today.strftime("%d/%m/%Y")
        self.MemberID = self.GenerateMemberID()

    def GenerateMemberID(self):
        Numb0 = int(str(self.RegistrationDate)[8])
        Numb1 = int(str(self.RegistrationDate)[9])
        Numb2 = random.randint(0, 9)
        Numb3 = random.randint(0, 9)
        Numb4 = random.randint(0, 9)
        Numb5 = random.randint(0, 9)
        Numb6 = random.randint(0, 9)
        Numb7 = random.randint(0, 9)
        Numb8 = random.randint(0, 9)
        Numb9 = (Numb0 + Numb1 + Numb2 + Numb3 + Numb4 + Numb5 + Numb6 + Numb7 + Numb8) % 10
        randomNumb = int(str(Numb0) + str(Numb1) + str(Numb2) + str(Numb3) +
                   str(Numb4) + str(Numb5) + str(Numb6) + str(Numb7) + str(Numb8) + str(Numb9))
        with sqlite3.connect('DataBase.db') as conn:
            cur = conn.cursor()
            cur.execute('select MemberID from Members')
            rows = cur.fetchall()
        for row in rows:
            if row == randomNumb:
                return Employee.GenerateMemberID()
        conn.close()
        return randomNumb

    def InsertData(self):
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS Members (
                            FirstName TEXT, 
                            LastName TEXT, 
                            Age INTEGER, 
                            Gender TEXT, 
                            Weight INTEGER, 
                            Address TEXT, 
                            City TEXT, 
                            Email TEXT, 
                            PhoneNumber TEXT, 
                            IsConsult BOOLEAN, 
                            IsSysAdm BOOLEAN, 
                            IsSupAdm BOOLEAN, 
                            RegistrationDate TEXT, 
                            MemberID INTEGER
                          )""")
        cursor.execute("INSERT INTO Members VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                       (self.FirstName, self.LastName, self.Age, self.Gender, self.Weight, 
                        self.Address, self.City, self.Email, self.PhoneNumb, self.IsConsult, 
                        self.IsSysAdm, self.IsSupAdm, str(self.RegistrationDate), self.MemberID))
        connection.commit()
        connection.close()

    def Print(self):
        print(self.FirstName, self.LastName)
        print(self.Age)
        print(self.Gender)
        print(self.Weight)
        print(self.Address, self.City)
        print(self.Email)
        print(self.PhoneNumb)
        print(self.IsConsult)
        print(self.IsSysAdm)
        print(self.IsSupAdm)
