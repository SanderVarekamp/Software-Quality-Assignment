import sqlite3
import re
from datetime import datetime

from LogActivity import LogActivity
from Employee import Employee

class main:
    def start():
        print("Welcome!")
        print("What would you like to do?")
        print("1.Register new user")
        print("2.Log in")
        print("3.Log out")
        choice = input("Enter your choice")
        if choice == "1":
            main.RegisterNewMember()
        if choice == "2":
            print("WIP")
        if choice == "3":
            print("WIP")

    def Login():
        print

    def RegisterNewMember():
        def input_with_validation(prompt, validation_func, error_message):
            while True:
                value = input(prompt)
                if validation_func(value):
                    return value
                else:
                    print(error_message)
        
        def validate_name(name):
            return name.isalpha()
        
        def validate_age(age):
            return age.isdigit() and 0 < int(age) < 150
        
        def validate_gender(gender):
            return gender.lower() in ['male', 'female', 'other']
        
        def validate_weight(weight):
            return weight.replace('.', '', 1).isdigit() and 0 < float(weight) < 1000
        
        def validate_email(email):
            return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None
        
        def validate_phone(phone):
            return re.match(r"6-\d{8}$", phone) is not None
        
        FirstName = input_with_validation("What is your first name?", validate_name, "Invalid name. Please enter alphabetic characters only.")
        LastName = input_with_validation("What is your last name?", validate_name, "Invalid name. Please enter alphabetic characters only.")
        Age = input_with_validation("What is your age?", validate_age, "Invalid age. Please enter a valid number between 1 and 150.")
        Gender = input_with_validation("What is your gender?", validate_gender, "Invalid gender. Please enter 'male', 'female', or 'other'.")
        Weight = input_with_validation("What is your weight?", validate_weight, "Invalid weight. Please enter a valid number.")
        Address = input("What is your address?")  # Assuming no validation needed
        City = input("What is your city?")  # Assuming no validation needed
        Email = input_with_validation("What is your email?", validate_email, "Invalid email address. Please include '@'.")
        PhoneNumb = input_with_validation("What is your phone number? (6-XXXXXXXX)", validate_phone, "Invalid phone number. Format should be 6-XXXXXXXX.")
        
        NewPhoneNumb = f"31-{PhoneNumb}"
        NewEmployee = Employee(FirstName, LastName, Age, Gender, Weight, Address, City, Email, NewPhoneNumb, True, False, False)
        NewEmployee.InsertData()
        LogActivity.LogAction("Testing", "Created new user", f"Created new user named {FirstName} {LastName}", "No")
        print("User succesfully created.")
        main.start()

    def insertTest():
        E1 = Employee("Emma", "Doe", 36, "Female", 70, 
                      "Wijnhaven 107 3232KL", "Rotterdam", "Emma.Doe@Test.com", "31-6-53458917", True, False, False)
        E1.Print()
        print(E1.RegistrationDate)
        print(E1.MemberID)
        E1.InsertData()

if __name__ == '__main__':
    main.start()