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
        pattern = re.compile(r'^[A-Za-z\s]+ \d+[a-zA-Z]? \d{4}[A-Z]{2}$')
        result = bool(pattern.match(address))
        return result, ("Valid address" if result else "Invalid address")
    
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
        try:
            cursor.execute("SELECT Username FROM Members")
            ExistingUsernames = cursor.fetchall()
        except:
            ExistingUsernames = ""
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
        if AccountType.lower() != "consultant" and AccountType.lower() != "admin":
            Age = AccountManager.input_with_validation("age", AccountManager.Is_Valid_age, "")
            Gender = AccountManager.input_with_validation("gender", AccountManager.Is_Valid_gender, "Please enter 'male', 'female', or 'other'.")
            Weight = AccountManager.input_with_validation("weight", AccountManager.Is_Valid_weight, "")
            Address = AccountManager.input_with_validation("address", AccountManager.Is_Valid_Address, "Please enter your street name, house number and postal code")
            City = AccountManager.input_with_validation("city", AccountManager.Is_Valid_City, "")
            Email = AccountManager.input_with_validation("email", AccountManager.Is_Valid_email, "")
            PhoneNumb = AccountManager.input_with_validation("phone number", AccountManager.Is_Valid_phone, "(6-XXXXXXXX) or (6XXXXXXXX)")
        else:
            Age = None
            Gender = None
            Weight = None
            Address = None
            City =  None
            Email = None
            PhoneNumb = None
        AccountManager.CreateAccount(Username, Password, FirstName.capitalize(), LastName.capitalize(), Age, Gender, Weight, Address, City, Email, PhoneNumb, AccountType)

    def CreateAccount(Username, Password, FirstName, LastName, Age, Gender, Weight, Address, City, Email, NewPhoneNumb, Type = "Member"):
        if not isinstance(LoggedInAccount.CurrentLoggedInAccount, Account): 
            print("Aborted.") 
            return
        FailureCounter = 0
        if Type.lower() == "consultant" or Type.lower() == "admin":
            results = [AccountManager.Is_Valid_Username(Username), AccountManager.Is_Valid_Password(Password), AccountManager.Is_Valid_FirstName(FirstName), AccountManager.Is_Valid_LastName(LastName)]
            for result in results:
                if not result[0]:
                    print(result[1])
                    FailureCounter = FailureCounter + 1
        else:
            results = [AccountManager.Is_Valid_Username(Username), AccountManager.Is_Valid_Password(Password), AccountManager.Is_Valid_FirstName(FirstName), AccountManager.Is_Valid_LastName(LastName), AccountManager.Is_Valid_age(Age), AccountManager.Is_Valid_gender(Gender), AccountManager.Is_Valid_weight(Weight), AccountManager.Is_Valid_Address(Address), AccountManager.Is_Valid_City(City), AccountManager.Is_Valid_email(Email), AccountManager.Is_Valid_phone(NewPhoneNumb)]
            for result in results:
                if not result[0]:
                    print(result[1])
                    FailureCounter = FailureCounter + 1
        if FailureCounter > 0: return

        if Type.lower() != "consultant" and Type.lower() != "admin":
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
    
    TempPasswordForReset = "TempPassword123!"

    # na inloggen als wachtwoord gelijk is aan AccountManager.TempPasswordForReset
    def ResetPasswordInput(Acc: Account):
        print("What will be your new Password?")
        NewPassword = input("> ")
        AccountManager.ChangePassword(NewPassword, Acc)

    # voor admin om password van gebruiker te veranderen naar AccountManager.TempPasswordForReset
    def ResetPassword(Acc: Account):
        AccountManager.ChangePassword(AccountManager.TempPasswordForReset, Acc)

    def ChangePassword(NewPassword: str, Acc: Account, CurrentPassword: str = None) -> tuple[bool, str]:
        Decrypt("DataBase.db.enc", "VeryGoodPassWord", Members.SourceDB)
        connection = sqlite3.connect(Members.SourceDB)
        cursor = connection.cursor()
        if CurrentPassword != None:
            cursor.execute("SELECT PasswordHash FROM Members WHERE Username = ?",(Acc.Username,))
            PWHash = cursor.fetchone()[0]
            if not bcrypt.checkpw(CurrentPassword.encode("utf-8"),PWHash):
                connection.close()
                Encrypt(Members.SourceDB, "VeryGoodPassWord")
                return False, "Current password is incorrect"
        Result, Message = AccountManager.Is_Valid_Password(NewPassword)
        if not Result:
            connection.close()
            Encrypt(Members.SourceDB, "VeryGoodPassWord")
            return Result, Message 
        cursor.execute( "UPDATE Members SET PasswordHash = ? WHERE Username = ?", (bcrypt.hashpw(NewPassword.encode("utf-8"),bcrypt.gensalt()), Acc.Username))
        connection.commit()
        connection.close()
        Encrypt(Members.SourceDB, "VeryGoodPassWord")
        return True, "Changed Password"
        
    def ChangePasswordInput():
        print("What is your current password?")
        CurrentPassword = input("> ")
        print("What will be your new password?")
        NewPassword = input("> ")
        Result, Message = AccountManager.ChangePassword(NewPassword, LoggedInAccount.CurrentLoggedInAccount, CurrentPassword)
        if not Result:
            print(Message)

    def SearchAccount(query, currentuser):
        Decrypt("DataBase.db.enc", "VeryGoodPassWord", Members.SourceDB)
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        search_pattern = f"%{query}%"
  
        base_query = """SELECT * FROM Members WHERE 
                        (Username LIKE ? OR
                        PasswordHash LIKE ? OR
                        FirstName LIKE ? OR
                        LastName LIKE ? OR
                        Age LIKE ? OR
                        Gender LIKE ? OR
                        Weight LIKE ? OR
                        Address LIKE ? OR
                        City LIKE ? OR
                        Email LIKE ? OR
                        PhoneNumber LIKE ? OR
                        Type LIKE ? OR
                        RegistrationDate LIKE ? OR
                        MemberID LIKE ?)"""
        print(currentuser.Type.lower())
        if currentuser.Type.lower() == "consultant":
            base_query += " AND Type = 'Member'"
        elif currentuser.Type.lower() == "admin":
            base_query += " AND(Type = 'Member' OR Type = 'Consultant')"
        elif currentuser.Type.lower() == "superadmin":
            base_query += " AND NOT Type = 'SuperAdmin'"
        base_query += " LIMIT 1"
        cursor.execute(base_query, (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern,
                                    search_pattern, search_pattern, search_pattern, search_pattern, search_pattern,
                                    search_pattern, search_pattern, search_pattern, search_pattern))
        row = cursor.fetchone()
        connection.close()
        Encrypt(Members.SourceDB, "VeryGoodPassWord")
        if row:
            account = Account(
                Username=row[0],
                PasswordHash=row[1],
                FirstName=row[2],
                LastName=row[3],
                Age=row[4],
                Gender=row[5],
                Weight=row[6],
                Address=row[7],
                City=row[8],
                Email=row[9],
                PhoneNumb=row[10],
                Type=row[11]
            )
            account.RegistrationDate = row[12]
            account.MemberID = row[13]
            return account
        else:
            print("No account found")
            return None
        
    def DeleteAccount(account):
        Decrypt("DataBase.db.enc", "VeryGoodPassWord", Members.SourceDB)
        if not isinstance(account, Account):
            raise ValueError("Expected an Account instance")
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Members WHERE MemberID = ?", (account.MemberID,))
        connection.commit()
        connection.close()
        Encrypt(Members.SourceDB, "VeryGoodPassWord")


    def EditAccount(account):
        if not isinstance(account, Account):
            raise ValueError("Expected an Account instance")
        print("="* 30)
        print("What would u like to change? ")
        print("1. First Name:")
        print("2. Last Name:")
        print("3. Age:")
        print("4. Gender:")
        print("5. Weight:")
        print("6. Address:")
        print("7. City:")
        print("8. Email:")
        print("9. Phone Number:")  

        option = input("Choose an option to update (1-9): ")
        fields = ["FirstName", "LastName", "Age", "Gender", "Weight", "Address", "City", "Email", "PhoneNumb"]

        if option in [str(i) for i in range(1, 10)]:
            field = fields[int(option) - 1]
            new_value = input(f"What would you like to change {field} to: ")
            AccountManager.UpdateMemberData(account.MemberID, field, new_value)
            print(f"{field} has been updated.")
        else:
            print("Invalid option selected.")

    def UpdateMemberData(MemberID, field, new_value):
        Decrypt("DataBase.db.enc", "VeryGoodPassWord", Members.SourceDB)
        with sqlite3.connect('DataBase.db') as conn:
            cur = conn.cursor()
            query = f"UPDATE Members SET {field} = ? WHERE MemberID = ?"
            cur.execute(query, (new_value, MemberID))
            conn.commit()
        Encrypt(Members.SourceDB, "VeryGoodPassWord")

    def ChangeAccount(LoggedinAccount):
        AccountToFind = input("Enter account detail: ")
        Database.LogAction(LoggedinAccount.Username if LoggedinAccount != None else None,"Selecting from menu options.", f"Looking up {AccountToFind}",False)
        member = AccountManager.SearchAccount(AccountToFind, LoggedinAccount)
        if member != None:
            loop = True
            if loop:
                if LoggedinAccount.Type.lower() == "superadmin" or LoggedinAccount.Type.lower() == "admin":
                    AccountManager.ChoiceAdmin(member, LoggedinAccount, loop)
                elif LoggedinAccount.Type.lower() == "consultant":
                    AccountManager.ChoiceConsultant(member, LoggedinAccount, loop)
            else:
                print("No account found")
    
    def ChoiceAdmin(member, LoggedinAccount, loop):
        while loop:
            print("Found account:")
            member.Print()
            print("1. Return")
            print("2. Edit account")
            print("3. Delete account")
            print("4. Reset password")
            choice2 = input("Enter your choice: ")
            if choice2 == "1":
                loop = False
            elif choice2 == "2":
                Database.LogAction(LoggedinAccount.Username if LoggedinAccount != None else None,"Selecting from menu options.", f"Editing {member.Username}",False)
                loop = False
                AccountManager.EditAccount(member)
            elif choice2 == "3":
                Database.LogAction(LoggedinAccount.Username if LoggedinAccount != None else None,"Selecting from menu options.", f"Deleting {member.Username}",False)
                AccountManager.DeleteAccount(member)
                print("Account succesfully deleted!")
                input()
                loop = False
            elif choice2 == "4":
                AccountManager.ResetPassword(member)
                input()
                loop = False
            else:
                print("Invalid input")
                input()

    def ChoiceConsultant(member, LoggedinAccount, loop):
        while loop:
            print("Found account:")
            member.Print()
            print("1. Return")
            print("2. Edit account")
            choice2 = input("Enter your choice: ")
            if choice2 == "1":
                loop = False
                return
            elif choice2 == "2":
                Database.LogAction(LoggedinAccount.Username if LoggedinAccount != None else None,"Selecting from menu options.", f"Editing {member.Username}",False)
                loop = False
                AccountManager.EditAccount(member)
            else:
                print("Invalid input")
                input()