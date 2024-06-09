import mysql.connector
from mysql.connector import IntegrityError

#check if correct password
def authenticate(username):
    #setting up connection
    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )

    cursor = db.cursor()
    # getting password
    cursor.execute(f"SELECT password FROM user_info WHERE username = '{username}';")
    result = cursor.fetchall()
    passw = result[0][0]
    cursor.close()
    db.close()
    return(passw)

# check if username exists
def verify(username):
    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )

    cursor = db.cursor()
    
    uname_cond = False

    cursor.execute(f"SELECT username FROM user_info;")
    result = cursor.fetchall()
    for i in result:
        if username == i[0]:
            uname_cond = True
    
    cursor.close()
    db.close()

    if uname_cond:
        return(True)
    else:
        return(False)

# creating new acc with uname and passw
def registration(username, password, fn, ln):
    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )

    cursor = db.cursor()

    cond_u = False
    cond_p = False

    sql1 = (f"INSERT INTO user_info (`username`, `password`, `f_name`, `l_name`) VALUES (%s, %s, %s, %s);")
    
    # checking for orginal username
    try:
        cursor.execute(sql1, (username, password, fn, ln))
        db.commit()
        cursor.close()
        db.close()
        return(f"Account successfully created!")

    except IntegrityError as err:
        # Step 5: Handle the integrity error
        cursor.close()
        db.close()
        return(f"Username already taken")
    # result = cursor.fetchall()
    # print(result)
    # if not len(result) == 0:
    #     print("wrong username")

# change the password
def change_pw(username, password):
    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )

    cursor = db.cursor()
    cursor.execute((f"UPDATE user_info SET `password` = '{password}' WHERE (`username` = '{username}');"))
    db.commit()
    cursor.close()
    db.close()
    print("Password changed successfully")

# add values for other fields in login_info

# search for names
def searchName(username):
    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )

    cursor = db.cursor()
    cursor.execute((f"SELECT FirstName, LastName FROM user_info WHERE username = %s;"), (username,))
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return(f"{result[0][0]} {result[0][1]}")

# get information for profile page
def get_info(username):
    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )

    cursor = db.cursor()
    cursor.execute((f"SELECT * FROM user_info WHERE username = %s;"), (username,))
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return(result)

# delete an entire account
def delete_my_account(username):
    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )

    cursor = db.cursor()
    cursor.execute((f"DELETE FROM user_info WHERE username = %s;"), (username,))
    db.commit()
    cursor.close()
    db.close()
    return("Account deleted successfully")


# testing:
# print(delete_account("root"))
# print(get_info("rohansohan"))
# print(searchName("aadivivi"))
# change_pw("premkhan", "janani")
# registration("jeffb", "alexaislove", "Jeff", "Bezos", "NYC", "USA")
# print(verify("tatyasawant"))
# authenticate("tatyasawant")