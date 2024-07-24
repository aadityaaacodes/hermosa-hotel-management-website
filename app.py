from flask import Flask, render_template, request, session, url_for, redirect
from mysql_accessor import verify, authenticate, searchName, get_info, delete_my_account
from admin_functions import add_product, rem_product, show_products, filter_products, show_product, edit_products
from cust_functions import registration
from order_functions import makeBill, histBill
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = "keylogger69"


# Client-side routes


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        #collecting values from the form
        uname = request.form["username"]
        passw = request.form["password"]
        if not uname == '':
            if verify(uname):   #checking username
                if authenticate(uname) == passw:    #checking password
                    return redirect (url_for('show_data', username=uname))  #redirecting to homepage
                else:
                    return (render_template('login.html', login_message = "Incorrect password"))
            else:
                return (render_template('login.html', login_message = "Username doesn't exist")) 
        else:
            return (render_template('login.html', login_message = "Enter valid username")) 
    else:
        return (render_template(('login.html')))

@app.route('/homepage/<string:username>')
def show_data(username):
    user = searchName(username)
    return(render_template('homepage.html', nameofUser=user, username=username))


# customer-side routes
@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if session["admin"] == "True":
        if request.method == 'POST':
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
        else:
            return(render_template('user-register.html'))
    else:
        return(redirect(url_for('admin_homepage')))

@app.route('/profile/<username>')
def profile_page(username):
    pass

@app.route('/profile/<username>/delete')
def delete_account(username):
    msg = (delete_my_account(username))
    msg = msg[0]
    return(redirect(url_for('login', page_title="Admin")))


# Admin-side routes 

# using a dynamic json file to store changes to admin credentials
admin_info_path = 'admin_login_info.json'
def provide():
    with open(admin_info_path, 'r') as file:
        return json.load(file)
def put(log_info):
    with open(admin_info_path, 'w') as file:
        return json.dump(log_info, file)

@app.route('/', methods=['GET', 'POST'], endpoint='Logout')
def admin_authenticate():
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

@app.route('/authenticate/change', methods=['GET', 'POST'], endpoint='Change Credentials')
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

@app.route('/home', methods=['GET', 'POST'], endpoint="Home")
def admin_homepage():
    if session["admin"] == "True":
        if request.method=='POST':
            action = request.form.get("action")
            if action == "Logout":
                session["admin"] = "False"
            return(redirect(url_for(f"{action}")))
            # return(action)
        else:
            return(render_template('admin-home.html'))
    else:
        return(redirect(url_for('Logout')))

@app.route('/add', methods=['GET', 'POST'], endpoint='Add Products')
def add_product_page(messg="Item deleted successfully!"):
    if session["admin"] == "True":
        if request.method=='POST':
            if request.form.get('action')=='Home':
                return(redirect(url_for('admin_homepage')))
            else:
                P_details = request.form.to_dict()
                o_p = add_product(P_details["name"], P_details["price"], P_details["description"], P_details["veg"], P_details["type"], P_details["image_link"])
                return(render_template('admin-home.html', welcome_message=o_p))

        else:
            return render_template(f'admin-add.html', welcome_message="Welcome!")
    else:
        return(redirect(url_for('Logout')))

@app.route('/view', methods=['GET', 'POST'], endpoint='Manage Products')
def view_page(messg="Welcome"):
    if session["admin"] == "True":
        if request.method=='POST':
            P_id = request.form.get("product_id")
            action = request.form.get("action")
            if action == 'delete':
                return(redirect(url_for('del_product', pid=P_id)))
            elif action == 'edit':
                return(redirect(url_for('edit_product', pid=P_id)))
            elif action=='Home':
                return(redirect(url_for('admin_homepage')))
            elif action == 'apply':
                # F_veg = request.form.get("isVeg")
                # F_type = request.form.get("type")
                res = filter_products(c1=request.form.get("c1"), c2=request.form.get("c2"), c3=request.form.get("c3"), c4=request.form.get("c4"), c5=request.form.get("c5"), c6=request.form.get("isVeg"), c7=request.form.get("type"))
                # return(f"{F_veg}, {F_type}")
                return render_template(f'admin-view.html', P_table=res, msg="Welcome!")        
            
        else:
            x = show_products()
            return render_template(f'admin-view.html', P_table=x, msg=messg)
    else:
        return(redirect(url_for('Logout')))

@app.route('/delete/<string:pid>')
def del_product(pid):
    # return(render_template('test.html', message=pid))
    rem_product(pid)
    return(redirect((url_for('view_page', messg='Product removed successfully'))))

@app.route('/edit/<string:pid>', methods=["POST", "GET"])
def edit_product(pid):
    if request.method=='POST':
        if request.form.get('action')=='Back':
            return(redirect(url_for('view_page')))
        else:
            product_meta = request.form.to_dict()
            db_message = edit_products(p_id=pid, p_name=product_meta["Product Name"], price=product_meta["Price"], desc=product_meta["Description"], veg=product_meta["Ingridient Information"], type=product_meta["Product Type"], imgL=product_meta["Image Link"])
            # return(request.form.to_dict())
            return(redirect(url_for('view_page', messg=db_message)))
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
        if request.form.get("send")=='APPLY':
            a = histBill(date=request.form.get("date"), 
                         phno=request.form.get("phno"), 
                         amt=request.form.get("amt"),
                         type=request.form.get("type"))
            return(render_template('admin-billing-history.html', P_table=a))
        if request.form.get("send")=='CLEAR':
            a = histBill()
            return(render_template('admin-billing-history.html', P_table=a))
    elif request.method=='GET':
        return(render_template('admin-billing-history.html', P_table=histBill()))


@app.route('/customer-history', methods=['GET', 'POST'])
def view_customers():
    pass

#taking orders
@app.route('/admin/order', methods=["POST", "GET"], endpoint='Order Taking') 
def take_order():
    if session["admin"] == "True":
        return(render_template('admin-order.html'))
    else:
        return(redirect(url_for('Logout')))

# testing purposes
@app.route('/test/<func>', methods=['GET', 'POST'])
def test_forms(func):
    if request.method=='POST':
        PName = request.form["name"]
        return(render_template('test.html', message=PName))
        # return(render_template('test.html', message=PName))
    else:
        return(render_template(f'admin-{func}.html'))


@app.route('/order-management/<tid>/<uid>')
def order_taking(uid, tid):
    return(render_template('order.html', uid=uid, tid=tid))


if __name__ == '__main__':
    app.run(debug=True, port=9000)