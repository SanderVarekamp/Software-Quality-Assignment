import sqlite3

from Employee import Employee

class main:
    def start():
        print ("Hello world!")
        E1 = Employee("Emma", "Doe", 36, "Female", 70, 
                      "Wijnhaven 107 3232KL", "Rotterdam", "Emma.Doe@Test.com", "0653458917", True, False, False)
        E1.Print()
        print(E1.RegistrationDate)
        print(E1.MemberID)
        E1.InsertData()

if __name__ == '__main__':
    main.start()