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
    sql = f"INSERT INTO product_info (`name`, `price`, `description`, `isVeg`, `type`, `imageLink`) VALUES (%s, %s, %s, %s, %s, %s)"
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
    

# add_product("Biryani", 98, "BKL Chutiya", "Vegetarian", "www.google.com")
# rem_product(3)
