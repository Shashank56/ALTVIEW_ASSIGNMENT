from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
# from instagram import getfollowedby, getname


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class User(db.Model):
    """ Create user table"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    fullname = db.Column(db.String(120))
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(80))
    about = db.Column(db.String(100))

    def __init__(self, username, password,fullname,email,about):
        self.username = username
        self.fullname = fullname
        self.email = email
        self.password = password
        self.about = about


@app.route('/', methods=['GET', 'POST'])
def home():
    """ Session control"""
    if not session.get('logged_in'):
        return render_template('main.html')
    else:
        if request.method == 'POST':
            # username = getname(request.form['username'])
            return render_template('user.html') #should change
        return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['log']
        passw = request.form['pwd']
        try:
            data = User.query.filter_by(username=name,password=passw).first()
            if data is not None:
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                return 'Dont Login'
        except:
            return "Dont Login"


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register Form"""
    if request.method == 'POST':
        new_user = User(
            username=request.form['signup_username'],
            fullname=request.form['field_1'],
            email=request.form['signup_email'],
            password=request.form['signup_password'],
            about=request.form['field_2'])
        print(new_user)
        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html')
    return render_template('register.html')


@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.secret_key = "123"
    app.run(host='0.0.0.0')
    
