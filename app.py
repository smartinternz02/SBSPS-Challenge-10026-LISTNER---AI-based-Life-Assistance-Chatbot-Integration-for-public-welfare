from flask import Flask, request, redirect,flash,session
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
import secrets
import json
from datetime import date
with open('config.json','r') as c:
    params = json.load(c)["params"]
local_server=True

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

class Signup(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(24), nullable=False)
    DoB = db.Column(db.String(8), nullable=False)
    email= db.Column(db.String(50),unique=True, nullable=False)
    password = db.Column(db.String(14), nullable=False)

    # A class method to check if an email already exists in the database
    @classmethod
    def email_exists(cls, email):
        return cls.query.filter_by(email=email).first() is not None
    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    

@app.route("/")
def main():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/faqs")
def faqs():
    return render_template("faqs.html")

@app.route("/foryou")
def foryou():
    return render_template("foryou.html")

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/emergency")
def emergency():
    return render_template("emergency.html")

@app.route('/login', methods=['GET','POST'])
def login():
    # If the request method is GET, render the login template
    if request.method == 'POST':
        # If the request method is POST, get the form data
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Get the user by email from the database
        user = Signup.get_by_email(email)
        # Check if the user exists and the password is correct
        
        if user and password==user.password:
            # Store the user id in the session
            session['user_id'] = user.Sno
            return redirect('/foryou')
        else:
            # Flash an error message and redirect to login page
            flash('Invalid email or password!', 'error')
            return redirect('/login')
    return render_template("login.html")

@app.route('/signup', methods=['GET','POST'])
def signup():
   
    if(request.method=='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        dob=request.form.get('dob')
        password=request.form.get('password')
        password_check=request.form.get('password_check')

        dob = date.fromisoformat(dob)

        if password != password_check:
            flash('Passwords do not match!', 'error')
            return redirect('/signup')
        
        if dob > date.today():
            flash('Date of birth is not valid!', 'error')
            return redirect('/signup')
        
        if Signup.email_exists(email):
            flash('Email already taken!', 'error')
            return redirect('/signup')
        
        if name =='':
            flash('Name field should not be empty', 'error')
            return redirect('/signup')

        entry =Signup(Name=name, DoB=dob,Email=email,Password=password)
        db.session.add(entry)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect('/login')    
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)