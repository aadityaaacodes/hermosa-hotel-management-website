import mysql.connector
from mysql.connector import Error

def add_product(p_name, price, desc, veg, type, imgL):

    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )

    cursor = db.cursor()
    sql = f"INSERT INTO product_info (`p_name`, `price`, `description`, `isVeg`, `type`, `imageLink`) VALUES (%s, %s, %s, %s, %s, %s)"
    try:
        cursor.execute(sql, (p_name, price, desc, veg, type, imgL))
        result = cursor.fetchall()
        print(result)
        db.commit()
        cursor.close()
        db.close()
        return("Product Added Successfully!")
    except Error as err:
        cursor.close()
        db.close()
        return(f"Error in Adding Product: {err}")

def rem_product(p_id):

    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )

    cursor = db.cursor()
    sql = f"DELETE FROM product_info WHERE (product_id = {p_id});"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    db.commit()
    cursor.close()
    db.close()
    
def show_products(pid='', p_name='', price='', rating='', frequency='', isVeg='', type=''):

    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )

    q1 = "SELECT * FROM product_info"
    q2 = ""
    q3 = ""

    sequences = []
    if pid:
        sequences.append(f"product_id {pid}")
    if p_name:
        sequences.append(f"p_name {p_name}")
    if price:
        sequences.append(f"price {price}")
    if rating:
        sequences.append(f"rating {rating}")
    if frequency:
        sequences.append(f"frequency {frequency}")
    
    if len(sequences)>0:
        for seq in sequences:
            q2 = q2+' '+seq+','
    else:
        q2="  "
    
    q2 = q2[:-1]
    if q2[-1]=='C':
        q2 = "ORDER BY"+q2

    conds = []
    if isVeg:
        conds.append(f"isVeg='{isVeg}' and ")
    if type:
        conds.append(f"type='{type}' and ")

    for c in conds:
        q3 += c 
    
    if len(q3)>0:
        q3 = q3[:-4]
        q3 = "WHERE "+q3
    else:
        q3 = ""
    
    sql = q1+' '+q3+' '+q2+';'
    print(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return(result)

def edit_products(p_id, p_name, price, desc, veg, type, imgL):
    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )

    cursor = db.cursor()
    sql = f"UPDATE product_info SET p_name = %s, price = %s, description = %s, isVeg = %s, type = %s, imageLink = %s WHERE product_id = {p_id};"
    try:
        cursor.execute(sql, (p_name, price, desc, veg, type, imgL))
        result = cursor.fetchall()
        print(result)
        db.commit()
        cursor.close()
        db.close()
        return("Product Edited Successfully!")
    except Error as err:
        cursor.close()
        db.close()
        return(f"Error in Adding Product: {err}")

def show_product(pid):
    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )

    cursor = db.cursor()
    sql = f"SELECT p_name, price, isVeg, type, description, imageLink FROM product_info WHERE product_id={pid};"
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return(result)
