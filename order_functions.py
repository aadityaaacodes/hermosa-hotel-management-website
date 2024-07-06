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




# del_item(1)

# fill_cart(6, 100, 1)
empty_cart()