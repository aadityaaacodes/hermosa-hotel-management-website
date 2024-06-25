from flask import Flask, render_template, request, session, url_for, redirect
from mysql_accessor import verify, authenticate, searchName, registration, get_info, delete_my_account
from admin_functions import add_product, rem_product, show_products

app = Flask(__name__)

# Client-side routes

@app.route('/')
def welcomePage():
    return(render_template('login.html', login_message="Welcome to Banerjee's Kitchen"))

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # if request.form['log'] == 'login':
        #     return (render_template('login.html'))
        uname = request.form["username"]
        passw = request.form["password"]
        fname = request.form["First Name"]
        lname = request.form["Last Name"]
        city = request.form["City"]
        country = request.form["Country"]
        if uname == '' or passw == '' or fname =='' or lname =='':
            msg = "Fill all the values"
        else:
            msg = registration(uname, passw, fname, lname, city, country)
        return(render_template('register.html', reg_message=msg))
    else:
        return(render_template('register.html'))
    
@app.route('/profile/<username>')
def profile_page(username):
    pass

@app.route('/profile/<username>/delete')
def delete_account(username):
    msg = (delete_my_account(username))
    msg = msg[0]
    return(redirect(url_for('login', page_title="Admin")))


# Admin-side routes 

@app.route('/admin/<func>', methods=['GET', 'POST'])
def admin_page(func):
    if func=="add":
        if request.method=='POST':
            P_details = request.form.to_dict()
            o_p = add_product(P_details["name"], P_details["price"], P_details["description"], P_details["veg"], P_details["type"], P_details["image_link"])
            return(render_template('admin-home.html', welcome_message=o_p))

        elif request.method=='GET':
            return render_template(f'admin-{func}.html')
    
    if func=='view':
        if request.method=='GET':
            x = show_products()
            return render_template(f'admin-{func}.html', P_table=x)







# testing purposes
@app.route('/test/<func>', methods=['GET', 'POST'])
def test_forms(func):
    if request.method=='POST':
        PName = request.form["name"]
        return(render_template('test.html', message=PName))
        # return(render_template('test.html', message=PName))
    else:
        return(render_template(f'admin-{func}.html'))

if __name__ == '__main__':
    app.run(debug=True, port=9000)