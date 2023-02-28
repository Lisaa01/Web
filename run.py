from flask import Flask, url_for, redirect, render_template, request
from data import users

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        users.append({'email': email, 'password': password})
        return render_template("index.html")
    return render_template("reg.html")
# Tesztet tesztelni jó!

if __name__ == '__main__':
    app.run(debug=True)
