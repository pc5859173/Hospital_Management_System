from flask import Flask, render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, logout_user, login_manager,LoginManager
from flask_login import login_required,current_user


app = Flask(__name__)
app.secret_key = "priyachoudhary"

# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# database connection
app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://priya01:Priya#8789@pc-test.database.windows.net/hmsdb?driver=SQL+Server"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# user class
class User(UserMixin, db.Model):
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

# route for home 
@app.route('/')
def home():
    return render_template("home.html")

# route for doctors 
@app.route('/doctors')
def doctors():
    return render_template("doctor.html")    

# route for patients
@app.route('/patients', methods = ["POST", "GET"])
@login_required
def patients():
     if request.method == "POST":
       
        email = request.form['email']
        name = request.form['name']
        gender = request.form['gender']
        slot = request.form['slot']
        time = request.form['time']
        date = request.form['date']
        disease =request.form['disease'] 
        dept = request.form['dept']
        number = request.form['number']
        
        
        # method to save data in db
        entry = Patients(email = email, name = name, gender = gender, slot = slot  ,time =time ,date =date ,disease =disease ,dept =dept, number = number)
        db.session.add(entry)
        db.session.commit()
        flash("Booking Confirmed", "info")
     return render_template("patient.html") 

# route for bookings
@app.route('/bookings')
@login_required
def bookings(): 
    em=current_user.email
    query=db.engine.execute(f"SELECT * FROM [dbo].[patients] WHERE email='{em}'")
    return render_template('booking.html', query=query)

# route for edit in booking page
@app.route("/edit/<string:pid>",methods=['POST','GET'])
@login_required
def edit(pid):
    posts = Patients.query.filter_by(pid=pid).first()
    if request.method=="POST":
        email=request.form.get('email')
        name=request.form.get('name')
        gender=request.form.get('gender')
        slot=request.form.get('slot')
        disease=request.form.get('disease')
        time=request.form.get('time')
        date=request.form.get('date')
        dept=request.form.get('dept')  
        number=request.form.get('number')
        db.engine.execute(f"UPDATE patients SET email = '{email}', name = '{name}', gender = '{gender}', slot = '{slot}', disease = '{disease}', time = '{time}', date = '{date}', dept = '{dept}', number = '{number}' WHERE patients.pid = '{pid}'") 
        flash("Slot is Updated", "success")
        return redirect(url_for('bookings'))
    return render_template('edit.html', posts=posts)  

# route for delete in booking page
@app.route("/delete/<string:pid>",methods=['POST','GET'])
@login_required
def delete(pid):  
    db.engine.execute(f"DELETE FROM [dbo].[patients] WHERE patients.pid={pid}")
    flash("slot Deleted Successfully", "danger") 
    return redirect(url_for('bookings'))   

# route for login
@app.route('/login', methods = ["POST", "GET"])
def login():
     if request.method=="POST":
        email = request.form.get('email')
        password = request.form.get('password')
        
        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Successfull", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid Credentials" , "danger") 
            return redirect(url_for('login'))   
     return render_template("login.html") 

# route for signup
@app.route('/signup',methods = ["POST","GET"])
def signup():
    if request.method=="POST":
        username =request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user  = User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exists", "warning")
            return render_template('signup.html')
        encpassword = generate_password_hash(password)

        #  1 insert query to insert data in db
        # new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")
        
        # 2 method to save data in db
        entry = User(username=username, email=email, password=encpassword)   
        db.session.add(entry)
        db.session.commit() 
        flash("Signup Successfull Please Login","primary")
        return render_template('login.html') 
    return render_template("signup.html") 

# route for logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("logout Successfull", "warning")
    return redirect(url_for("login"))  



if __name__ == '__main__':
    app.run(debug=True)