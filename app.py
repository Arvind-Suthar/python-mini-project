from flask import Flask, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#initialize a db
db = SQLAlchemy(app)

#create a db model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    fullname = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    #create func to return string when we create a entry
    def __repr__(self):
        return '<Name %r>' % self.id


@app.route('/')
def index(user):
    return render_template('index.html', currentUser = user)

@app.route('/login')
def loginrender():
    return render_template('login.html')


@app.route('/userlogon', methods = ['POST'])
def loginuser():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["passw"]
        fetchedUser = Users.query.filter_by(email = email).first()
        if fetchedUser:
            return redirect(url_for('index', fetchedUser))


@app.route('/register')
def registerrender():
    return render_template('register.html')


@app.route('/registerUser', methods = ['POST'])
def registerUser():
    if request.method == 'POST':
        email = request.form['email']
        fullname = request.form['fullname']
        address = request.form['address']
        password = request.form['passw']
        
        new_user = Users(email = email, fullname = fullname, address = address, password = password)
        print(new_user.id)
        if new_user:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('loginrender'))
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug = True)