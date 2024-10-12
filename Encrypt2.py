# Import necessary modules from pycryptodome
import sqlite3
import shutil
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from binascii import hexlify, unhexlify

from Logs import Logs


class EncryptNew:

    def __init__(self):
        self.private_key = self._load_private_key()
        self.public_key = self._load_public_key()
        self.encrypted_data = []

    def _load_private_key(self):
        with open("private_key.pem", "rb") as file:
            private_key = RSA.import_key(file.read())
        return private_key
    
    def _load_public_key(self):
        with open("public_key.pem", "rb") as file:  
            public_key = RSA.import_key(file.read())  
        return public_key
    
    def encrypt_member(self, user):
        connection = sqlite3.connect('DataBase.db')
        cursor = connection.cursor()    
        cursor.execute("""CREATE TABLE IF NOT EXISTS Members (
                    Username TEXT,
                    PasswordHash TEXT,
                    FirstName TEXT, 
                    LastName TEXT, 
                    Age INTEGER, 
                    Gender TEXT, 
                    Weight INTEGER, 
                    Address TEXT, 
                    City TEXT, 
                    Email TEXT, 
                    PhoneNumber TEXT, 
                    Type TEXT,
                    RegistrationDate TEXT, 
                    MemberID INTEGER
                    )""")
        connection.commit()
        self.encrypted_data = user.Encrypt(self.public_key)
        print(self.encrypted_data[0])
        cursor.execute('INSERT INTO Members VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (self.encrypted_data[0], user.PasswordHash, self.encrypted_data[1], self.encrypted_data[2], self.encrypted_data[3], self.encrypted_data[4], self.encrypted_data[5], self.encrypted_data[6], self.encrypted_data[7], self.encrypted_data[8], self.encrypted_data[9], self.encrypted_data[10], self.encrypted_data[11], self.encrypted_data[12]))
        connection.commit()  
    
    def decrypt_members(self, db_path, given_name):
        from Account import Account
        all_members = []
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Members")
        rows = cursor.fetchall()
        cipher_rsa = PKCS1_OAEP.new(self.private_key)
        for row in rows:
            decrypted_data = []
            for data in row:
                try:
                    decrypted = cipher_rsa.decrypt(unhexlify(data))
                    word = decrypted.decode("utf-8")
                    decrypted_data.append(word)
                except:
                    decrypted_data.append(data)
            account = Account(decrypted_data[0], decrypted_data[1], str(decrypted_data[2]), decrypted_data[3], str(decrypted_data[4]), decrypted_data[5], decrypted_data[6], decrypted_data[7], decrypted_data[8], decrypted_data[9], decrypted_data[10], decrypted_data[11], decrypted_data[12], decrypted_data[13])
            account.RegistrationDate = (decrypted_data[12])
            account.MemberID = str(decrypted_data[13])
            if decrypted_data[0] == given_name and given_name is not None:
                return account
            else:
                all_members.append(account)
        connection.close()
        return all_members
        
    def encrypt_log(self, log):
        connection = sqlite3.connect('DataBase.db')
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS ActivityLog (
                    Date TEXT, 
                    Time TEXT, 
                    Username TEXT, 
                    Activity TEXT, 
                    Information TEXT, 
                    Suspicious TEXT 
                    )""")
        connection.commit()
        self.encrypted_data = log.Encrypt(self.public_key)
        cursor.execute('INSERT INTO ActivityLog VALUES (?, ?, ?, ?, ?, ?)', (self.encrypted_data[0], self.encrypted_data[1], self.encrypted_data[2], self.encrypted_data[3], self.encrypted_data[4], self.encrypted_data[5]))
        connection.commit()
        connection.close()


    def decrypt_log(self, db_path) -> list:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM ActivityLog")
        rows = cursor.fetchall()
        
        cipher_rsa = PKCS1_OAEP.new(self.private_key)
        for row in rows:
            decrypted_data = []
            for data in row:
                try:
                    decrypted = cipher_rsa.decrypt(unhexlify(data))
                    word = decrypted.decode("utf-8")
                    decrypted_data.append(word)
                except:
                    decrypted_data.append(data)
        connection.close()
        return decrypted_data
    
    def SelectFromDatabase(self, accounts, condition, fetchAll, input=None):
        try:
            if input is None:
                filtered_accounts = [account for account in accounts if condition(account)]
            else:
                filtered_accounts = [account for account in accounts if condition(account, input)]

            if fetchAll:
                result = filtered_accounts
            else:
                result = filtered_accounts[0] if filtered_accounts else None
        except:
            result = None
        return result
    
    def DecryptAll(self, thing):
        connection = sqlite3.connect('DataBase.db')
        cursor = connection.cursor()  
        system = EncryptNew()  
        if thing == "Members":
            try:
                print("Decrypting members...")	
                items =  system.decrypt_members("DataBase.db", None)
                print("Creating table...")
                cursor.execute("""CREATE TABLE IF NOT EXISTS Decrypted (
                Username TEXT,
                PasswordHash TEXT,
                FirstName TEXT, 
                LastName TEXT, 
                Age INTEGER, 
                Gender TEXT, 
                Weight INTEGER, 
                Address TEXT, 
                City TEXT, 
                Email TEXT, 
                PhoneNumber TEXT, 
                Type TEXT,
                RegistrationDate TEXT, 
                MemberID INTEGER
                )""")
                connection.commit()
                if items is not None:
                    for user in items:
                        cursor.execute('INSERT INTO Members VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user.Username, user.PasswordHash, user.FirstName, user.LastName, user.Age, user.Gender, user.Weight, user.Address, user.City, user.Email, user.PhoneNumb, user.Type, user.RegistrationDate, user.MemberID))
            except:
                print("An error occurred while decrypting the members.")
        elif thing == "Logs":
            items = self.decrypt_log("DataBase.db")
            cursor.execute("""CREATE TABLE IF NOT EXISTS Decrypted (
                    Date TEXT, 
                    Time TEXT, 
                    Username TEXT, 
                    Activity TEXT, 
                    Information TEXT, 
                    Suspicious TEXT 
                )""")
            connection.commit()
            for log in items:
                cursor.execute('INSERT INTO ActivityLog VALUES (?, ?, ?, ?, ?, ?)', (log.Date, log.Time, log.Username, log.Activity, log.Info, log.Suspicious))
        else:
            return None  
        print("Decryption complete.")
        connection.commit()  

    def ChangeTable(self, table):
        connection = sqlite3.connect('DataBase.db')
        cursor = connection.cursor()
        cursor.execute("DROP TABLE ?"), (table)
        cursor.execute("ALTER TABLE Decrypted RENAME TO ?"), (table)
        connection.commit()
        connection.close()

    def DeleteDecrypted(self):
        connection = sqlite3.connect('DataBase.db')
        cursor = connection.cursor()
        cursor.execute("DROP TABLE Decrypted")
        connection.commit()
        connection.close()

    def Createbackup(self, source_db, destination_db):
        """
        Duplicates the entire database file.
        
        :param source_db: Path to the source database file.
        :param destination_db: Path to the destination database file.
        """
        try:
            shutil.copyfile(source_db, destination_db)
            print(f"Database duplicated successfully from {source_db} to {destination_db}")
        except Exception as e:
            print(f"An error occurred while duplicating the database: {e}")
        return destination_db
    
    def RestoreBackup(self, source_db, destination_db):
        """
        Restores the database file from a backup.
        
        :param source_db: Path to the source database file.
        :param destination_db: Path to the destination database file.
        """
        try:
            shutil.copyfile(source_db, destination_db)
            print(f"Database restored successfully from {source_db} to {destination_db}")
        except Exception as e:
            print(f"An error occurred while restoring the database: {e}")
        return destination_db
    
if __name__ == "__main__":
    system = EncryptNew()
    system.encrypt_member("Database.db", )
    system.DecryptAll("Members")