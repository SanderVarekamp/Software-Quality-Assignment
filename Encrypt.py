import sqlite3
import gzip
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
from os import getcwd
from datetime import datetime
from Employee import *

#WIP

def key_creation(password):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), 
                     salt=b'\xfaz\xb5\xf2|\xa1z\xa9\xfe\xd1F@1\xaa\x8a\xc2', 
                     iterations=1024, 
                     length=32, 
                     backend=default_backend())
    key = Fernet(base64.urlsafe_b64encode(kdf.derive(password)))
    return key

def encryption(b, password):
    f = key_creation(password)
    safe = f.encrypt(b)
    return safe

def decryption(safe, password):
    f = key_creation(password)
    b = f.decrypt(safe)
    return b

def open_cdb(name, password):
    with gzip.open(getcwd() + '/' + name + '_crypted.sql.gz', 'rb') as f:
        safe = f.read()
    content = decryption(safe, password)
    content = content.decode('utf-8')
    con = sqlite3.connect('DataBase.db')
    
    # Execute each command separately to handle errors
    for command in content.split(';'):
        command = command.strip()
        if command:
            try:
                con.execute(command)
            except sqlite3.OperationalError as e:
                if "already exists" in str(e):
                    print(f"Skipping creation of table: {e}")
                else:
                    raise
    return con

def save_cdb(con, name, password):
    with gzip.open(getcwd() + '/' + name + '_crypted.sql.gz', 'wb') as fp:
        b = b''
        for line in con.iterdump():
            # Skip the CREATE TABLE commands to prevent duplication of the table structure
            if not line.startswith("CREATE TABLE"):
                b += bytes('%s\n' % line, 'utf8')
        b = encryption(b, password)
        fp.write(b)

def insert_into_encrypted_db(name, password, insert_query, values):
    conn = open_cdb(name, password)
    cursor = conn.cursor()
    cursor.execute(insert_query, values)
    conn.commit()
    save_cdb(conn, name, password)
    conn.close()

if __name__ == '__main__':
    password = b'Sw0rdFish'
    db_name = 'DataBase'
    
    # Create initial encrypted file from existing database
    conn = sqlite3.connect('DataBase.db')
    conn.execute("""CREATE TABLE IF NOT EXISTS Members (
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
    conn.execute("""CREATE TABLE IF NOT EXISTS Logs (
                            Date TEXT, 
                            Time TEXT, 
                            User TEXT, 
                            Activity TEXT, 
                            Information TEXT, 
                            Suspicious TEXT 
                          )""")
    
    # Initial save to create encrypted file
    save_cdb(conn, db_name, password)
    conn.close()

    # Insert a new member into the encrypted database
    E1 = Employee("Emma", "Doe", 36, "Female", 70, 
                  "Wijnhaven 107 3232KL", "Rotterdam", "Emma.Doe@Test.com", "31-6-53458917", True, False, False)
    new_member_query = 'INSERT INTO Members (FirstName, LastName, Age, Gender, Weight, Address, City, Email, PhoneNumber, IsConsult, IsSysAdm, IsSupAdm, RegistrationDate, MemberID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    new_member_values = (E1.FirstName, E1.LastName, E1.Age, E1.Gender, E1.Weight, 
                         E1.Address, E1.City, E1.Email, E1.PhoneNumb, E1.IsConsult, E1.IsSysAdm, E1.IsSupAdm, E1.RegistrationDate, E1.MemberID)
    
    insert_into_encrypted_db(db_name, password, new_member_query, new_member_values)
    
    # Verify insertion
    conn = open_cdb(db_name, password)
    cursor = conn.execute('SELECT * FROM Members')
    headers = list(map(lambda x: x[0], cursor.description))
    print(headers)
    for x in cursor:
        for j in range(len(x)):
            print(headers[j] + ' ', x[j])
        print('\n')
    conn.close()