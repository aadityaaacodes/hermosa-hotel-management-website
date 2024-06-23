from flask import Flask, render_template, request, session, url_for, redirect
from mysql_accessor import verify, authenticate, searchName, registration, get_info, delete_my_account

app = Flask(__name__)

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
    return(redirect(url_for('login')))

if __name__ == '__main__':
    app.run(debug=True, port=9000)