import re
import sqlite3
import bcrypt
from Account import *
from LoggedInAccount import *

class AccountManager:

    def input_with_validation(prompt, validation_func, requirement):
            while True:
                print("What is the users "+prompt+"? "+requirement)
                value = input("> ")
                result = validation_func(value)
                if result[0]:
                    return value
                else:
                    print(result[1])
                    print()

    def Is_Valid_FirstName(firstname):
        result = firstname.isalpha()
        return result, ("Valid name" if result == True else "Invalid first name input.")
    
    def Is_Valid_LastName(lastname):
        result = lastname.isalpha()
        return result, ("Valid name" if result == True else "Invalid last name input.")
    
    def Is_Valid_age(age):
        result = (isinstance(age, int) or age.isdigit()) and 0 < int(age) < 150
        return result, ("Valid age" if result == True else "Invalid age")
    
    def Is_Valid_gender(gender):
        result = gender.lower() in ['male', 'female', 'other']
        return result, ("Valid gender" if result == True else "Invalid gender")
    
    def Is_Valid_weight(weight):
        result = weight.replace('.', '', 1).isdigit() and 0 < float(weight) < 1000
        return result, ("Valid weight" if result == True else "Invalid weight")
    
    def Is_Valid_Address(address):
        result = address.isalpha()
        return result, ("Valid address" if result == True else "Invalid address")
    
    def Is_Valid_City(city):
        result = city.isalpha()
        return result, ("Valid city" if result == True else "Invalid city")
    
    def Is_Valid_email(email):
        result = re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None
        return result, ("Valid Email" if result == True else "Invalid Email")
    
    def Is_Valid_phone(phone):
        result = re.match(r"6-\d{8}$", phone) is not None or re.match(r"6\d{8}$", phone) is not None, "Invalid phone number."
        return result, ("Valid phone number" if result == True else "Invalid phone number")

    def Is_Valid_Username(username):
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute("SELECT Username FROM Members")
        ExistingUsernames = cursor.fetchall()
        connection.close()

        username = username.lower()
        
        if len(username) < 8: return False, "Username must be at least 8 characters long."
        if len(username) > 10: return False, "Username must be no longer than 10 characters."
        if not re.match(r'^[a-z_]', username): False, "Username must start with a letter or underscore."
        if not re.match(r'^[a-z0-9_\'\.]+$', username): return False, "Username can only contain letters, numbers, underscores, apostrophes, and periods."
        if username in ExistingUsernames: return False, "Username already exists."
        return True, "Username is valid."
    
    def Is_Valid_Password(password):
        if len(password) < 12: return False, "Password must be at least 12 characters long."
        if len(password) > 30: return False, "Password must be no longer than 30 characters."
        if not re.search(r'[a-z]', password): return False, "Password must contain at least one lowercase letter."
        if not re.search(r'[A-Z]', password): return False, "Password must contain at least one uppercase letter."
        if not re.search(r'\d', password): return False, "Password must contain at least one digit."

        special_characters = r'~!@#$%&_\-+=`|\(\){}\[\]:;\'<>,\.?/'
        if not re.search(f"[{re.escape(special_characters)}]", password): return False, "Password must contain at least one special character."
        if not re.match(r'^[a-zA-Z0-9' + re.escape(special_characters) + ']+$', password): return False, "Password contains invalid characters."
        return True, "Password is valid."

    def Is_Valid_AccountType(type):
        if isinstance(LoggedInAccount.CurrentLoggedInAccount, Account):
            AccountTypeList = ['member', 'consultant', 'admin']
            if LoggedInAccount.CurrentLoggedInAccount.Type.lower() == "admin": AccountTypeList.remove("admin")
            elif LoggedInAccount.CurrentLoggedInAccount.Type.lower() == "consultant": AccountTypeList.remove("consultant")

            result = type.lower() in AccountTypeList
            return result, ("Valid type." if result == True else "Invalid type.")
        else: 
            return False, "Invalid logged in account."
    
    def CreateAccountInput():
        if not isinstance(LoggedInAccount.CurrentLoggedInAccount, Account): return

        AccountType = "Member" if LoggedInAccount.CurrentLoggedInAccount.Type.lower() == "consultant" else AccountManager.input_with_validation("account type",AccountManager.Is_Valid_AccountType,"Please enter "+("'member', 'consultant' or 'admin'." if LoggedInAccount.CurrentLoggedInAccount.Type.lower() == "superadmin" else "'member' or 'consultant'."))
        Username = AccountManager.input_with_validation("username", AccountManager.Is_Valid_Username, "Must be between 8 and 10 characters long and can only contain letters, numbers, underscores, apostrophes, and periods. Must start with letter or underscore.")
        Password = AccountManager.input_with_validation("password", AccountManager.Is_Valid_Password, "Must be between 12 and 30 characters long and must contain at least 1 lowercase, uppercase, digit and special character.")
        FirstName = AccountManager.input_with_validation("first name", AccountManager.Is_Valid_FirstName, "")
        LastName = AccountManager.input_with_validation("last name", AccountManager.Is_Valid_LastName, "")
        Age = AccountManager.input_with_validation("age", AccountManager.Is_Valid_age, "")
        Gender = AccountManager.input_with_validation("gender", AccountManager.Is_Valid_gender, "Please enter 'male', 'female', or 'other'.")
        Weight = AccountManager.input_with_validation("weight", AccountManager.Is_Valid_weight, "")
        Address = AccountManager.input_with_validation("address", AccountManager.Is_Valid_Address, "Please enter your street name, house number and postal code")
        City = AccountManager.input_with_validation("city", AccountManager.Is_Valid_City, "")
        Email = AccountManager.input_with_validation("email", AccountManager.Is_Valid_email, "")
        PhoneNumb = AccountManager.input_with_validation("phone number", AccountManager.Is_Valid_phone, "(6-XXXXXXXX) or (6XXXXXXXX)")
        
        AccountManager.CreateAccount(Username, Password, FirstName.capitalize(), LastName.capitalize(), Age, Gender, Weight, Address, City, Email, PhoneNumb, AccountType)

    def CreateAccount(Username, Password, FirstName, LastName, Age, Gender, Weight, Address, City, Email, NewPhoneNumb, Type = "Member"):
        if not isinstance(LoggedInAccount.CurrentLoggedInAccount, Account): 
            print("Aborted.") 
            return

        FailureCounter = 0
        results = [AccountManager.Is_Valid_Username(Username), AccountManager.Is_Valid_Password(Password), AccountManager.Is_Valid_FirstName(FirstName), AccountManager.Is_Valid_LastName(LastName), AccountManager.Is_Valid_age(Age), AccountManager.Is_Valid_gender(Gender), AccountManager.Is_Valid_weight(Weight), AccountManager.Is_Valid_Address(Address), AccountManager.Is_Valid_City(City), AccountManager.Is_Valid_email(Email), AccountManager.Is_Valid_phone(NewPhoneNumb)]
        for result in results:
            if not result[0]:
                print(result[1])
                FailureCounter = FailureCounter + 1
        if FailureCounter > 0: return
        
        NewPhoneNumb = f"31-{NewPhoneNumb}"

        salt = bcrypt.gensalt()
        Password = bcrypt.hashpw(bytes(Password, 'utf-8'), salt)
        NewAccount = Account(Username, Password, FirstName.capitalize(), LastName.capitalize(), Age, Gender, Weight, Address, City, Email, NewPhoneNumb, Type)
        AccountManager.InsertIntoDatabase(NewAccount)
        print("Account created.")

    def InsertIntoDatabase(account):
        if not isinstance(account, Account): return False, "Given account is not of type AccountManager."
        Decrypt("DataBase.db.enc", "VeryGoodPassWord", Members.SourceDB)
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Members VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                       (account.Username, account.PasswordHash, account.FirstName, account.LastName, account.Age, account.Gender, account.Weight, 
                        account.Address, account.City, account.Email, account.PhoneNumb, account.Type, str(account.RegistrationDate), account.MemberID))
        connection.commit()
        connection.close()
        Encrypt(Members.SourceDB, "VeryGoodPassWord")
        return True, "AccountManager inserted into database."

    # def InsertData(self):
    #     connection = sqlite3.connect("DataBase.db")
    #     cursor = connection.cursor()
    #     cursor.execute("""CREATE TABLE IF NOT EXISTS Members (
    #                         FirstName TEXT, 
    #                         LastName TEXT, 
    #                         Age INTEGER, 
    #                         Gender TEXT, 
    #                         Weight INTEGER, 
    #                         Address TEXT, 
    #                         City TEXT, 
    #                         Email TEXT, 
    #                         PhoneNumber TEXT, 
    #                         Type TEXT,
    #                         RegistrationDate TEXT, 
    #                         MemberID INTEGER
    #                       )""")
    #     cursor.execute("INSERT INTO Members VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
    #                    (self.FirstName, self.LastName, self.Age, self.Gender, self.Weight, 
    #                     self.Address, self.City, self.Email, self.PhoneNumb, self.IsConsult, 
    #                     self.IsSysAdm, self.IsSupAdm, str(self.RegistrationDate), self.MemberID))
    #     connection.commit()
    #     connection.close()

