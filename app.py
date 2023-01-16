from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# database connection
app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://priya01:Priya#8789@pc-test.database.windows.net/hmsdb?driver=SQL+Server"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# user class
class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username =  db.Column(db.String(100))  
    email = db.Column(db.String(100))
    password = db.Column(db.String(1000))

# patient class
class Patients(db.Model):
    pid = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100))       
    name = db.Column(db.String(100))
    gender =db.Column(db.String(100)) 
    slot = db.Column(db.String(100))
    time =db.Column(db.String(100),nullable = "False") 
    date = db.Column(db.String(100),nullable = "False")
    disease =db.Column(db.String(100)) 
    dept = db.Column(db.String(100))
    number = db.Column(db.String(100))

# Doctors Class
class Doctors(db.Model):
    did = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(1000))  
    doctorname = db.Column(db.String(100))
    dept = db.Column(db.String(100))    
    
# here we will pass endpoints and run the function
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/doctors')
def doctors():
    return render_template("doctor.html")    

@app.route('/patients')
def patients():
    return render_template("patient.html") 

@app.route('/bookings')
def bookings():
    return render_template("booking.html") 

@app.route('/login')
def login():
    return render_template("login.html") 

@app.route('/signup',methods = ["POST","GET"])
def signup():
    if request.method=="POST":
        print("This is post method")
    print("This is get method")    
    return render_template("signup.html") 

@app.route('/logout')
def logout():
    return render_template("login.html")    



if __name__ == '__main__':
    app.run(debug=True)