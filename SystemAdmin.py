import sqlite3
from Consultant import *
class SystemAdmin():
    def GetMemberData(MemberID):
        with sqlite3.connect('DataBase.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Members WHERE MemberID =?", (MemberID,))
            data = cur.fetchone()
            if data:
                print(data)
                print("=" * 30)
                print("What would you like to change? ")
                print("1. First Name:")
                print("2. Last Name:")
                print("3. Age:")
                print("4. Gender:")
                print("5. Weight:")
                print("6. Address:")
                print("7. City:")
                print("8. Email:")
                print("9. Phone Number:")
                print("10. IsConsultant:")

                option = input("Choose an option to update (1-10): ")
                fields = ["FirstName", "LastName", "Age", "Gender", "Weight", "Address", "City", "Email", "PhoneNumb", "IsConsultant"]

                if option in [str(i) for i in range(1, 11)]:
                    field = fields[int(option) - 1]
                    new_value = input(f"What would you like to change {field} to: ")
                    SystemAdmin.UpdateMemberData(MemberID, field, new_value)
                    print(f"{field} has been updated.")
                else:
                    print("Invalid option selected.")
            else:
                print("No member found with that MemberID.")

