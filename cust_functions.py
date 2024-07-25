import mysql.connector
from mysql.connector import IntegrityError

def registration(pno, fn, mn, ln, mail):
    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )
    cursor = db.cursor()
    sql1 = (f"INSERT INTO customer_info (`ph_no`, `cust_fname`, `cust_mname`, `cust_lname`, `email`) VALUES (%s, %s, %s, %s, %s);")
    try:
        cursor.execute(sql1, (pno, fn, mn, ln, mail))
        db.commit()
        cursor.close()
        db.close()
        return(f"Account already exists!")

    except IntegrityError as err:
        # Step 5: Handle the integrity error
        cursor.close()
        db.close()
        return(f"Username already taken")
    
def getInfo(phno):
    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )

    cursor = db.cursor()
    
    sql = (f"SELECT * FROM customer_info WHERE ph_no = {int(phno)};")
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return(result)

def userHistory(phno):
    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )
    cursor = db.cursor()
    sql = f"SELECT b.date, b.PHNO, b.amt, b.type FROM bill_table as b WHERE b.PHNO={int(phno)};"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return(result)

def update(pno, fn, mn, ln, mail):
    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )
    cursor = db.cursor()
    sql1 = (f"INSERT INTO customer_info (`ph_no`, `cust_fname`, `cust_mname`, `cust_lname`, `email`) VALUES (%s, %s, %s, %s, %s);")
    try:
        cursor.execute(sql1, (pno, fn, mn, ln, mail))
        db.commit()
        cursor.close()
        db.close()
        return(f"Account already exists!")

    except IntegrityError as err:
        # Step 5: Handle the integrity error
        cursor.close()
        db.close()
        return(f"Username already taken")

print(userHistory(phno=8169987004))