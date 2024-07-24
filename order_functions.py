import mysql.connector

def empty_cart():
    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )

    cursor = db.cursor()
    sql = "TRUNCATE TABLE temp_cart;"
    cursor.execute(sql)
    db.commit()
    result = cursor.fetchall()
    print(result)
    cursor.close()
    db.close()

def fill_cart(p_id, price, qty):
    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )
    cursor = db.cursor()
    sql1 = f"INSERT INTO temp_cart (`p_id`, `price`, `qty`) VALUES (%s, %s, %s)"
    cursor.execute(sql1, (p_id, price, qty))
    db.commit()
    sql2 = "SELECT * FROM temp_cart;"
    cursor.execute(sql2)
    result = cursor.fetchall()
    print(result)
    cursor.close()
    db.close()

def del_item(p_id):
    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )
    cursor = db.cursor()
    sql1 = f"DELETE FROM temp_cart WHERE (p_id = %s);"
    cursor.execute(sql1, (p_id,))
    db.commit()
    sql2 = "SELECT * FROM temp_cart;"
    cursor.execute(sql2)
    result = cursor.fetchall()
    print(result)
    cursor.close()
    db.close()


#Billing functions
def makeBill(phno, amt, type, date):
    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )
    cursor = db.cursor()
    sql = f"INSERT INTO bill_table (`PHNO`, `amt`, `type`, `date`) VALUES (%s, %s, %s, %s);"
    cursor.execute(sql, (phno, amt, type, date))
    db.commit()
    result = cursor.fetchall()
    cursor.close()
    db.close()
    if result == []:
        return("Successfully Recorded Bill")
    else: 
        return("Error")

def getBill():
    pass

def viewBill():
    pass

def histBill(date='', phno='', amt='', type=''):
    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )

    cursor = db.cursor()

    sequence = []
    q1="SELECT * FROM bill_table"
    # q2="ORDER BY"

    q2=""
    q3="WHERE type="
    
    if date:
        sequence.append(f"date {date}")
    if phno:
        sequence.append(f"PHNO {phno}")
    if amt:
        sequence.append(f"amt {amt}")

    if len(sequence)>0:
        for seq in sequence:
            q2 = q2+' '+seq+','
    else:
        q2="  "
    
    q2 = q2[:-1]
    print(q2)
    if q2[-1]=='C':
        q2 = "ORDER BY"+q2

    if type:
        q3 = q3+f"'{type}'"
    else:
        q3 = ""

    sql = q1+' '+q3+' '+q2+';'
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return(result)

# print(histBill(amt='DESC', type='UPI'))
# print(histBill())
# del_item(1)
# fill_cart(6, 100, 1)
# empty_cart()