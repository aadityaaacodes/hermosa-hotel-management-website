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
    
def show_products():
    res = []

    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )

    cursor = db.cursor()
    sql1 = "SELECT product_id, name, price, rating, frequency, isVeg, type FROM product_info;"
    sql2 = "SELECT COUNT(*) FROM product_info;"
    cursor.execute(sql1)
    result1 = cursor.fetchall()
    cursor.close()
    db.close()
    return(result1)

    # db = mysql.connector.connect(
    #     host = "localhost", 
    #     user = "root", 
    #     password = "cincy@2024",
    #     database = "banerjee_kitchen"
    # # )

    # # cursor = db.cursor()
    # # sql2 = "SELECT COUNT(*) FROM product_info;"
    # # cursor.execute(sql2)
    # # result2 = cursor.fetchall()
    # # result2 = sum(result2, ())
    # # cursor.close()
    # # db.close()

    # # res = result1+result2
    # return(res)
    
def filter_products(veg_info="None", type="None"):
    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )

    cursor = db.cursor()
    cond1 = ""
    cond2 = ""
    cond3 = ""
    cond4 = ""
    cond5 = ""
    cond6 = "isVeg IS NOT NULL"
    cond7 = "type IS NOT NULL"
    if veg_info !=  "None":
        cond6 = f"isVeg = '{veg_info}'"
    if type != "None":
        cond7 = f"type = '{type}'"
    cond_sql = f" WHERE {cond6} AND {cond7}"
    sql = f"SELECT product_id, name, price, rating, frequency, isVeg, type FROM product_info {cond_sql};"
    cursor.execute(sql)
    result1 = cursor.fetchall()
    cursor.close()
    db.close()
    return(result1)

# filter_products(veg_info="Vegetarian")

# x = show_products()
# print(x)
# add_product("Biryani", 98, "BKL Chutiya", "Vegetarian", "www.google.com")
# rem_product(3)
