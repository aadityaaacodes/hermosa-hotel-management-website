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
    
def show_products():
    res = []

    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )

    cursor = db.cursor()
    sql1 = "SELECT product_id, p_name, price, rating, frequency, isVeg, type FROM product_info;"
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
    
def filter_products(c1="ASC", c2="None", c3="None", c4="None", c5="None", c6="None", c7="None"):
    db = mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "cincy@2024",
        database = "banerjee_kitchen"
    )

    cursor = db.cursor()
    cond2=""
    cond3=""
    cond4=""
    cond5=""
    cond1 = f"product_id {c1}"

    if c2 !=  "None":
        cond2 = f", p_name {c2}"
    if c3 !=  "None":
        cond3 = f", price {c3}"
    if c4 != "None":
        cond4 = f", rating {c4}"
    if c5 != "None": 
        cond5 = f", frequency {c5}"
    order_sql = f"ORDER BY {cond1} {cond2} {cond3} {cond4} {cond5}"

    cond6 = "isVeg IS NOT NULL"
    cond7 = "type IS NOT NULL"
    if c6 !=  "None":
        cond6 = f"isVeg = '{c6}'"
    if c7 != "None":
        cond7 = f"type = '{c7}'"
    cond_sql = f" WHERE {cond6} AND {cond7}"

    sql = f"SELECT product_id, p_name, price, rating, frequency, isVeg, type FROM product_info {cond_sql} {order_sql};"
    cursor.execute(sql)
    result1 = cursor.fetchall()
    cursor.close()
    db.close()
    return(result1)

# for i in filter_products(c1="DESC", c2="ASC", c6="Vegetarian", c7="Beverage"):
#     print(i[1])
# x = show_products()
# print(x)
# add_product("Biryani", 98, "BKL Chutiya", "Vegetarian", "www.google.com")
# rem_product(3)
