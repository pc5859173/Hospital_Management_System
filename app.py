from flask import Flask, render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, logout_user, login_manager,LoginManager
from flask_login import login_required,current_user
import json


# read config.json file
with open('config.json','r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
app.secret_key = "priyachoudhary"

# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'




@login_manager.user_loader
def load_user(user_id):
    return User_p.query.get(int(user_id))

# @login_manager.user_loader
# def load_user(user_id):
#     return User_d.query.get(int(user_id))


# database connection
app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://priya01:Priya#8789@pc-test.database.windows.net/hmsdb?driver=SQL+Server"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# user class
class User_p(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username =  db.Column(db.String(100))  
    email = db.Column(db.String(100))
    password = db.Column(db.String(1000))

# Doctor class
class User_d(UserMixin, db.Model):
    did = db.Column(db.Integer,primary_key = True)
    username =  db.Column(db.String(100))  
    email = db.Column(db.String(100))
    password = db.Column(db.String(1000))    

# patient form class
class Patients_book(db.Model):
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

# Doctors department booking Class
class Doctors_dept(db.Model):
    ddid = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(1000))  
    doctorname = db.Column(db.String(100))
    dept = db.Column(db.String(100))    
    
# here we will pass endpoints and run the function

# route for home 
@app.route('/')
def home():
    # return render_template("Patient_login.html")
    return render_template("home.html")

# route for doctors 
@app.route('/doctors')
def doctors():
    return render_template("doctors.html")    

# route for patients
@app.route('/patientsbook')
def patientsbook():
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
        entry = Patients_book(email = email, name = name, gender = gender, slot = slot  ,time =time ,date =date ,disease =disease ,dept =dept, number = number)
        db.session.add(entry)
        db.session.commit()
        flash("Booking Confirmed", "info")
     return render_template('Patients_book.html')

# route for bookings
@app.route('/bookings')
def bookings(): 
    # em=current_user.email
    # query=db.engine.execute(f"SELECT * FROM [dbo].[patients] WHERE email='{em}'")
    return redirect(url_for('/bookings'))

# route for edit in booking page
@app.route("/edit/<string:pid>",methods=['POST','GET'])
@login_required
def edit(pid):
    posts = Patients_book.query.filter_by(pid=pid).first()
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
# @app.route('/login', methods = ["POST", "GET"])
# def login():
    #  if request.method=="POST":
    #     email = request.form.get('email')
    #     password = request.form.get('password')
        
    #     user=User.query.filter_by(email=email).first()

    #     if user and check_password_hash(user.password,password):
    #         login_user(user)
    #         flash("Login Successfull", "success")
    #         return redirect(url_for('home'))
    #     else:
    #         flash("Invalid Credentials" , "danger") 
    #         return redirect(url_for('home'))   
    #  return render_template("home.html") 

# route for signup
# @app.route('/signup',methods = ["POST","GET"])
# def signup():
#     if request.method=="POST":
#         username =request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')
        
#         user  = User.query.filter_by(email=email).first()
#         if user:
#             flash("Email Already Exists", "warning")
#             return render_template('signup.html')
#         encpassword = generate_password_hash(password)

#         #  1 insert query to insert data in db
#         # new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")
        
#         # 2 method to save data in db
#         entry = User(username=username, email=email, password=encpassword)   
#         db.session.add(entry)
#         db.session.commit() 
#         flash("Signup Successfull Please Login","primary")
#         return render_template('login.html') 
#     return render_template("signup.html") 

# route for logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("logout Successfull", "warning")
    return redirect(url_for("/"))  


# route for admin
@app.route('/admin')
def admin():
    return render_template('admin.html')    

#route for admin panel
@app.route('/apanel', methods=['GET', 'POST'])
def apanel():
    if request.method == 'POST':
        name =request.form.get('username')
        pwd = request.form.get('password')
        # print(name, pwd)
        # if( params['username']==name and params['password']==pwd):
        if(name==params["username"] and pwd==params["password"]):

            session['user']=name
            
            flash("Successfully login")
            return render_template('apanel.html')
        else:
            flash("Invalid credentials" )
    return redirect( url_for('admin') )


# route for patients page
@app.route('/ppanel')
def ppanel():
    return render_template('ppanel.html')     

# route for patient_signup
@app.route('/psignup',methods = ["POST","GET"])
def psignup():
    if request.method=="POST":
    #     print("This is post method")
    # print("this is get method")    
        username =request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user  = User_p.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exists", "warning")
            return render_template('Patient_signup.html')
        encpassword = generate_password_hash(password)

        #  1 insert query to insert data in db
        # new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")
        
        # 2 method to save data in db
        entry = User_p(username=username, email=email, password=encpassword)   
        db.session.add(entry)
        db.session.commit() 
        flash("Signup Successfull Please Login","primary")
        return redirect(url_for('plogin')) 
    return render_template("Patient_signup.html") 


# route for patient_login
@app.route('/plogin',methods = ['GET','POST'])
def plogin():
    if request.method=="POST":
        email = request.form.get('email')
        password = request.form.get('password')
        
        user=User_p.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Successfull", "success")
            return redirect(url_for('ppanel'))
        else:
            flash("Invalid Credentials" , "danger") 
            return redirect(url_for('plogin'))   
    return render_template("Patient_login.html")


# route for Doctors page
@app.route('/dpanel')
def dpanel():
    return render_template('dpanel.html')     

# route for doctors_signup
@app.route('/dsignup',methods = ["POST","GET"])
def dsignup():
    if request.method=="POST":
    #     print("This is post method")
    # print("this is get method")    
        username =request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user  = User_d.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exists", "warning")
            return render_template('Doctor_signup.html')
        encpassword = generate_password_hash(password)

        #  1 insert query to insert data in db
        # new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")
        
        # 2 method to save data in db
        entry = User_d(username=username, email=email, password=encpassword)   
        db.session.add(entry)
        db.session.commit() 
        flash("Signup Successfull Please Login","primary")
        return redirect(url_for('dlogin')) 
    return render_template("Doctor_signup.html") 


# route for doctors_login
@app.route('/dlogin',methods = ['GET','POST'])
def dlogin():
    if request.method=="POST":
        email = request.form.get('email')
        password = request.form.get('password')
        
        user=User_d.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Successfull", "success")
            return redirect(url_for('dpanel'))
        else:
            flash("Invalid Credentials" , "danger") 
            return redirect(url_for('dlogin'))   
    return render_template("Doctor_login.html")     

if __name__ == '__main__':
    app.run(debug=True)