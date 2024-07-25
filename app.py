from flask import Flask, render_template, request, session, url_for, redirect
from admin_functions import add_product, rem_product, show_products, show_product, edit_products
from cust_functions import registration, getInfo, userHistory, update
from order_functions import makeBill, histBill
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = "keylogger69"


# Admin-side routes 

# using a dynamic json file to store changes to admin credentials
admin_info_path = 'admin_login_info.json'
def provide():
    with open(admin_info_path, 'r') as file:
        return json.load(file)
def put(log_info):
    with open(admin_info_path, 'w') as file:
        return json.dump(log_info, file)


@app.route('/', methods = ['GET', 'POST'], endpoint = 'Logout')
def admin_authenticate():
    if session:
        if session["admin"]=="True":
            return( redirect (url_for("Home")))
    else:        
        if request.method=='POST':
            admin_log_info = provide()
            action = request.form.get("action")
            if action=='Login':
                u = request.form.get("usrname")
                p = request.form.get("passw")
                if u == admin_log_info["username"]:
                    if p == admin_log_info["password"]:
                        session["admin"] = "True"
                        return (redirect(url_for('Home')))
                    else:
                        return(render_template('admin-auth.html', log_message="Incorrect Password"))
                else:
                        return(render_template('admin-auth.html', log_message="Incorrect Username"))
            elif action=='Change Credentials':
                return(redirect(url_for('admin_change')))         
        else:
            return(render_template('admin-auth.html', log_message="Welcome! Please enter credentials"))
   
@app.route('/authenticate/change', methods = ['GET', 'POST'], endpoint = 'Change Credentials')
def admin_change():
    if request.method=='POST':
        if request.form.get('action')=='Home':
            return(redirect(url_for('admin_homepage')))
        else:
            admin_log_info=provide()
            admin_log_info["username"] = request.form.get("usrname")
            admin_log_info["password"] = request.form.get("passw")
            put(admin_log_info)
            return(redirect(url_for('admin_authenticate')))
    else:
        return(render_template('admin-change.html'))

@app.route('/home', methods = ['GET' , 'POST'], endpoint = "Home")
def admin_homepage():
    session["phno"] = ""
    if session["admin"] == "True":
        if request.method=='POST':
            action = request.form.get("action")
            if action == "Logout":
                session["admin"] = "False"
            return(redirect(url_for(f"{action}")))
        else:
            if request.args.get("messg") is None:
                return(render_template('admin-home.html', messg = "Greetings!"))
            else:
                return(render_template('admin-home.html', messg = request.args.get("messg")))
    else:
        return(redirect(url_for('Logout')))

@app.route('/add', methods = ['GET', 'POST'], endpoint= 'Add Products')
def add_product_page():
    if session["admin"] == "True":
        if request.method=='POST':
            if request.form.get('action')=='Home':
                return(redirect(url_for('Home')))
            else:
                P_details = request.form.to_dict()
                o_p = add_product(P_details["name"], P_details["price"], P_details["description"], P_details["veg"], P_details["type"], P_details["image_link"])
                return(redirect(url_for("Home", messg=o_p)))

        else:
            return render_template(f'admin-add.html')
    else:
        return(redirect(url_for('Logout')))

@app.route('/view', methods = ['GET', 'POST'], endpoint = 'Manage Products')
def view_page(messg="Welcome"):
    if session["admin"] == "True":
        if request.method =='POST':

            P_id = request.form.get("product_id")
            send = request.form.get("send")
            action = request.form.get("action")

            if send == 'delete':
                return(redirect(url_for('Delete', pid=P_id)))
            elif send == 'edit':
                return(redirect(url_for('Edit', pid=P_id)))
            elif send=='Home':
                return(redirect(url_for('Home')))

            elif action == 'APPLY':
                res = show_products(p_name=request.form.get("pname"), 
                                    price=request.form.get("price"), 
                                    rating=request.form.get("rating"), 
                                    frequency=request.form.get("frequency"), 
                                    isVeg=request.form.get("isVeg"), 
                                    type=request.form.get("type"))
                return(render_template('admin-view.html', P_table=res))
            
            elif action=='CLEAR':
                res = show_products()
                return render_template(f'admin-view.html', P_table=res)        
            
            # View Page
            else:
              return (redirect (url_for ('product_details', pid = send)))
                
        else:
            if request.args.get("messg") is None:
                return render_template(f'admin-view.html', P_table=show_products(), msg = "Greetings!")
            else:
                return render_template(f'admin-view.html', P_table=show_products(), msg = request.args.get("messg"))
    else:
        return(redirect(url_for('Logout')))

@app.route('/product-details/<string:pid>', methods = ["GET", "POST"])
def product_details(pid):
    if request.method == 'POST':
        x = pid
        if  request.form.get("page") == "Catalogue":
            return(redirect(url_for("Manage Products"))) 
        elif request.form.get("action") == 'EDIT':
            return (redirect (url_for("Edit", pid = x )))   
        elif request.form.get("action") == 'DELETE':
            return (redirect (url_for('Delete', pid = x)))
    else:
        x = show_product(pid=pid)
        return(render_template('admin-product.html', Product_Name = x))
    
@app.route('/delete/<string:pid>', endpoint='Delete')
def del_product(pid):
    rem_product(pid)
    return(redirect((url_for('Manage Products', messg='Product removed successfully'))))

@app.route('/edit/<string:pid>', methods=["POST", "GET"], endpoint='Edit')
def edit_product(pid):
    if request.method=='POST':
        if request.form.get('action')=='Back':
            return(redirect(url_for('view_page')))
        else:
            product_meta = request.form.to_dict()
            db_message = edit_products(p_id=pid, p_name=product_meta["Product Name"], price=product_meta["Price"], desc=product_meta["Description"], veg=product_meta["Ingridient Information"], type=product_meta["Product Type"], imgL=product_meta["Image Link"])
            # return(request.form.to_dict())
            return(redirect(url_for('Manage Products', messg=db_message)))
    else:
        x = show_product(pid)
        field_names = ['Product Name', 'Price', 'Ingridient Information', 'Product Type', 'Description', 'Image Link']
        product_dict = dict(zip(field_names, x))
        return(render_template('admin-edit.html', pid=pid, msg=product_dict))

@app.route('/billing', methods=['GET', 'POST'], endpoint='Billing')
def billing():
    if request.method=='POST':
        if request.form.get("send")=='Submit':
            date = request.form.get("date")
            phno = request.form.get("phno")
            amt = request.form.get("amt")
            type = request.form.get("type")
            res = makeBill(phno=phno, amt=amt, type=type, date=date)
            return(redirect(url_for('Billing')))
        else:
            page = request.form.get("pages")
            return(redirect(url_for(f'{page}')))

    elif request.method=='GET':
        return(render_template('admin-billing.html'))

@app.route('/billing/history', methods=['GET', 'POST'], endpoint='Billing History')
def billHistory():
    if request.method=='POST':
        send = request.form.get("send")
        if request.form.get("page") == "HOME":
            return(redirect(url_for("Home")))
        
        if send == 'APPLY':
            a = histBill(date=request.form.get("date"), 
                         phno=request.form.get("phno"), 
                         amt=request.form.get("amt"),
                         type=request.form.get("type"))
            return(render_template('admin-billing-history.html', P_table=a))
        elif send == 'CLEAR':
            a = histBill()
            return(render_template('admin-billing-history.html', P_table=a))
        elif send == "Add":
            return(redirect(url_for('Customer Registration')))
        else:
            session["phno"] = send
            return(redirect(url_for('Customer')))
    
    elif request.method=='GET':
        if request.args.get("messg") is not None:
            return(render_template('admin-billing-history.html', P_table=histBill(), messg=request.args.get("messg")))
        else:
            return(render_template('admin-billing-history.html', P_table=histBill()))


# Customer-side routes

@app.route('/customer/register', methods=['GET', 'POST'], endpoint="Customer Registration")
def user_register():
    if request.method == 'POST':
        if request.form.get("Register")=="Register":
            pno = (int)(request.form["Phone Number"])
            fn = request.form["First Name"]
            mn = request.form["Middle Name"]
            ln = request.form["Last Name"]
            mail = request.form["Email"]
            if pno == '' or fn == '' or ln == '':
                msg = "Fill all the values"
            else:
                msg = registration(pno=pno, fn=fn, mn=mn, ln=ln, mail=mail)
            return(render_template('user-register.html', reg_message=msg))
        elif request.form.get("Register")=="HOME":
            return(redirect(url_for("Home")))
    else:
        if session["phno"]:
            return(render_template('user-register.html', cond="True", phNo=session["phno"]))
        else:
            return(render_template('user-register.html', cond="False"))

@app.route('/customer/information', methods = ['POST', 'GET'], endpoint="Customer")
def customer_info():
    if request.method == 'POST':
        page = request.form.get("page")
        if page == "BACK":
            return(redirect(url_for("Billing History")))
        elif page == "EDIT":
            return(redirect(url_for('Customer Edit')))
        elif page == "HISTORY":
            return(redirect(url_for("History")))

    else:
        cust = getInfo(phno=session["phno"])
        if cust is not None:
            return(render_template('customer-info.html', Cust_Info=cust))
        else:
            return(redirect(url_for("Billing History", messg="Account not created!")))

@app.route('/customer/history', methods=['GET', 'POST'], endpoint = 'History')
def view_customer():
    if request.method == 'POST':
        if request.form.get("page") == 'BACK':
            return(redirect(url_for('Customer')))
    else:
        return(render_template('customer-history.html', phno=session["phno"],  P_table=userHistory(session["phno"])))

@app.route('/customer/edit', methods=['GET', 'POST'], endpoint="Customer Edit")
def customerEdit():
    if request.method == 'POST':
        if request.form.get("Register")=="Confirm":
            pno = (int)(request.form["Phone Number"])
            fn = request.form["First Name"]
            mn = request.form["Middle Name"]
            ln = request.form["Last Name"]
            mail = request.form["Email"]
            msg = update(pno=pno, fn=fn, mn=mn, ln=ln, mail=mail)
            return(redirect(url_for('Customer')))
        elif request.form.get("Register")=="BACK":
            return(redirect(url_for("Customer")))
    else:
        return(render_template('customer-edit.html', pack=getInfo(session["phno"])))


if __name__ == '__main__':
    app.run(debug=True, port=9000)