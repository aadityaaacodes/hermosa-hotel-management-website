import mysql.connector

def add_product(p_name, price, desc, veg, imgL):

    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )

    cursor = db.cursor()
    sql = f"INSERT INTO product_info (`name`, `price`, `description`, `isVeg`, `imageLink`) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (p_name, price, desc, veg, imgL))
    result = cursor.fetchall()
    print(result)
    db.commit()
    cursor.close()
    db.close()

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
