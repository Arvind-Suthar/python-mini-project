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
        userid = request.args['userid']
    return render_template('index.html', user = user, userid = userid)
'''
@app.route('/login')
def loginrender():
    return render_template('login.html')
'''
@app.route('/checkout/<name>', methods = ['POST'])
def checkout(name):
    if request.method == 'POST':
        if name == "usernotexists":
            return redirect(url_for("login"))
        else:
            mask = int(request.form['mask'])
            gloves = int(request.form['gloves'])
            ppe = int(request.form['ppe'])
            sanitizer = int(request.form['sanitizer'])
            shield = int(request.form['shield'])
            vitamin = int(request.form['vitamin'])
            return render_template('checkout.html', user = name, mask = mask, gloves = gloves, ppe = ppe, sanitizer = sanitizer, shield = shield, vitamin = vitamin)

    return redirect(url_for('index'))



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
            userid = fetchedUser.id
            return redirect(url_for('index', user = user, userid = userid, **request.args))
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