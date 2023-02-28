from flask import Flask, url_for, redirect, render_template, request, flash, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.sqlite3'
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


class books(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    author = db.Column(db.String(100))
    title = db.Column(db.String(100))

    def __init__(self, author, title):
        self.author = author
        self.title = title


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/view')
def view():
    return render_template('view.html', values=users.query.all())


@app.route('/bk_view')
def bk_view():
    return render_template("book_view.html", values=books.query.all())

@app.route("/book", methods=["GET", "POST"])
def book_list():
    if request.method == "POST":
        author = request.form['author']
        title = request.form['title']
        bk = books(author, title)
        db.session.add(bk)
        db.session.commit()
        flash('Book Saved!')
        return redirect(url_for('book_list'))

    else:
        return render_template("books.html")

@app.route('/delete_user', methods=["GET", "POST"])
def delete_user():
    if request.method == "POST":
        session.permanent = True
        email = request.form['email']
        password = request.form['password']
        user = users.query.filter_by(email=email, password=password).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            flash('User deleted!')
            return redirect(url_for('register'))
        else:
            flash('User not found!')

    return render_template("reg.html")

@app.route('/delete_book', methods=["GET", "POST"])
def delete_book():
    if request.method == "POST":
        author = request.form['author']
        title = request.form['title']
        book = books.query.filter_by(author=author, title=title).first()
        if book:
            db.session.delete(book)
            db.session.commit()
            flash('Book deleted!')
            return redirect(url_for('book_list'))
        else:
            flash('Book not found!')
    
    return render_template("books.html")

@app.route("/reg", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        session.permanent = True
        email = request.form['email']
        password = request.form['password']
        usr = users(email, password)
        db.session.add(usr)
        db.session.commit()
        flash('User Saved!')
        return redirect(url_for('register'))

    else:
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
