from flask import Flask, request,send_file, redirect,flash,session
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
import secrets
import json
import io
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date
from textblob import TextBlob


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

@app.route("/stats")
def stats():
    return render_template('stats.html')
@app.route("/stats1")
def stats1():
    data = pd.read_csv('data.csv')
    category_column = 'SEVERE_MENTAL_DISORDER_(SMD)'

    # Set the Seaborn style
    sns.set(style='whitegrid')

    # Create a horizontal bar chart using Seaborn
    plt.figure(figsize=(14, 6))
    colors = ["#FF5733", "#FFC300", "#36D7B7", "#3498DB", "#9B59B6", "#E74C3C", 
    "#2ECC71", "#1ABC9C", "#F39C12", "#E67E22", "#27AE60", "#2980B9", 
    "#8E44AD", "#D35400", "#16A085", "#C0392B", "#2C3E50", "#F39C12", 
    "#D35400", "#8E44AD", "#2980B9", "#3498DB", "#1ABC9C", "#E74C3C", 
    "#27AE60", "#FF5733", "#FFC300", "#36D7B7", "#9B59B6", "#2ECC71", 
    "#E67E22", "#16A085", "#C0392B", "#2C3E50"]
    sns.barplot(x=data[category_column], y=data['DISTRICT '], palette=colors)
    plt.xlabel('Severe Mental Disorder Cases')
    plt.ylabel('')
    plt.title('Severe Mental Disorder Cases by District')

    # Adding data labels on right side of bars
    for i, value in enumerate(data[category_column]):
        plt.text(value + 20, i, str(value), va='center', fontsize=5)
    # Save the chart to a BytesIO object
    image_stream = io.BytesIO()
    plt.tight_layout()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    plt.close()

    return send_file(image_stream, mimetype='image/png')

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