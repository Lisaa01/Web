from flask import Flask, url_for, redirect, render_template, request, flash, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)


class users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, email, password):
        self.email = email
        self.password = password


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/view')
def view():
    return render_template('view.html', values=users.query.all())

@app.route("/reg", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        session.permanent = True
        email = request.form['email']
        session['email'] = email
        found_email = users.query.filter_by(email=email).first()

        if found_email:
            session['password'] = found_email.password

        else:
            usr = users(email, '')
            db.session.add(usr)
            db.session.commit()

        flash('User Saved!')
        return redirect(url_for('index'))

    else:
        if 'email' in session:
            flash('User alredy saved!')
            return redirect(url_for('index'))
        return render_template("reg.html")

@app.route('/logout')
def logout():
    flash('You have been logged out', 'info')
    session.pop('email', None)
    session.pop('password', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
