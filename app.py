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
def index():
    user = ""
    if request.args:
        user = request.args['user']
    return render_template('index.html', user = user)
'''
@app.route('/login')
def loginrender():
    return render_template('login.html')
'''

@app.route('/login', methods = ['POST', 'GET'])
def login():
    error = ""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["passw"]
        fetchedUser = Users.query.filter_by(email = email, password = password).first()
        print(fetchedUser)
        if fetchedUser:
            user = fetchedUser.fullname
            return redirect(url_for('index', user = user, **request.args))
        else:
            error = "Invalid credentials!"
    return render_template('login.html', error = error)

@app.route('/register', methods = ['POST', 'GET'])
def register():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        fullname = request.form['fullname']
        address = request.form['address']
        password = request.form['passw']
        
        new_user = Users(email = email, fullname = fullname, address = address, password = password)
        if new_user:
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))
            except:
                error = "Couldn't register! User may already exist"
    return render_template('register.html', error = error)

if __name__ == '__main__':
    app.run(debug = True)