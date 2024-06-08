from flask import Flask, render_template, request, session, url_for

app = Flask(__name__)

@app.route('/')
def welcomePage():
    return("Welcome")

if __name__ == '__main__':
    app.run(debug=True, port=8050)