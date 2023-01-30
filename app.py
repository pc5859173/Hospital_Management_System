from flask import Flask, render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, logout_user, login_manager,LoginManager
from flask_login import login_required,current_user
import json
# import MySQLdb

# read config.json file
with open('config.json','r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)

# secret key
app.secret_key = "u>+eWoZ@_fV2K.>"

# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='patient_login'
login_manager.login_view='doctor_login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# database connection
# app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://priya01:Priya#8789@pc-test.database.windows.net/hmsdb?driver=SQL+Server"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/hmsdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# CLASS
# patients and doctor class
class User(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username =  db.Column(db.String(100))  
    email = db.Column(db.String(100),unique = True)
    password = db.Column(db.String(1000))

  # patient slot booking class
class Patientsbook(db.Model):
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
class Doctorsdept(db.Model):
    ddid = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(1000),unique = True )  
    doctorname = db.Column(db.String(100))
    dept = db.Column(db.String(100))   

# trigr Class    
class Trigr(db.Model):
    tid=db.Column(db.Integer,primary_key=True)
    pid=db.Column(db.Integer)
    email=db.Column(db.String(50))
    name=db.Column(db.String(50))
    action=db.Column(db.String(50))
    timestamp=db.Column(db.String(50))   

# class Trigrdoct(db.Model):
#     tdid=db.Column(db.Integer,primary_key=True)    
#     ddid=db.Column(db.Integer)
#     email=db.Column(db.String(50))
#     doctorname=db.Column(db.String(50))
#     dept = db.Column(db.String(100))
#     action=db.Column(db.String(50))
#     timestamp=db.Column(db.String(50)) 

@app.route('/flash/test')
def f_test():
    flash("Flash is working" , "warning")
    flash("Flash is working" , "info")
    return render_template('adminlogin.html')

@app.route('/image/test')
def image_test():
    return render_template('patientbooking.html')
    
# here we will pass endpoints and run the function

# LOGIN ROUTE
#route for admin_login
@app.route('/admin/login')
def admin_login():
    return render_template('adminlogin.html')   

@app.route('/admin/verify')
def check():
    if session['user']=='Admin' :
        return  render_template('adminhome.html') 
    return redirect(url_for('admin_login'))

@app.route('/admin/home', methods=['GET', 'POST'])
def admin_home():
    if request.method == 'POST':
        name =request.form.get('username')
        email = request.form.get('email')
        pwd = request.form.get('password')
        if(name==params["username"] and email==params["email"] and pwd==params["password"] ):

            session['user']=name
            flash("Successfully login" , "info")
            return render_template('adminhome.html')
        else:
            flash("Invalid credentials" , "warning")
    return redirect(url_for('admin_login'))

# route for patient_login
@app.route('/patient/login',methods = ['GET','POST'])
def patient_login():
    if request.method=="POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Successfull", "info")
            return render_template('patienthome.html')
        else:
            flash("Invalid Credentials" , "warning") 
            # return redirect(url_for('patient_login'))   
    return render_template("patientlogin.html")    

# route for doctors_login
@app.route('/doctor/login',methods = ['GET','POST'])
def doctor_login():
    if request.method=="POST":
        email = request.form.get('email')
        password = request.form.get('password')
        print(email,password)
        user=User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Successfull", "info")
            return redirect(url_for('doctor_home'))
        else:
            flash("Invalid Credentials" , "warning") 
            # return redirect(url_for('doctor_login'))   
    return render_template("doctorlogin.html")     

# SIGNUP ROUTE
# route for patient_signup
@app.route('/patient/signup',methods = ["POST","GET"])
def patient_signup():
    if request.method=="POST":
        username =request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user  = User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exists", "warning")
            return render_template('patientsignup.html')
        encpassword = generate_password_hash(password)
        #  1 insert query to insert data in db
        # new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")
        # 2 method to insert data in user class
        entry = User(username=username, email=email, password=encpassword)   
        db.session.add(entry)
        db.session.commit() 
        flash("Signup Successfull Please Login","info")
        return redirect(url_for('patient_login')) 
    return render_template("patientsignup.html") 

# route for doctors_signup
@app.route('/doctor/signup',methods = ["POST","GET"])
def doctor_signup():
    if request.method=="POST":
        username =request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user  = User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exists", "warning")
            return render_template('doctorsignup.html')
        encpassword = generate_password_hash(password)
        #  1 insert query to insert data in db
        # new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")
        # 2 method to insert data in user class
        entry = User(username=username, email=email, password=encpassword)   
        db.session.add(entry)
        db.session.commit() 
        flash("Signup Successfull Please Login","info")
        return redirect(url_for('doctor_login')) 
    return render_template("doctorsignup.html") 

# LOGOUT ROUTE
# route for logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("logout Successfull", "warning")
    return render_template('home.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('user')
    flash("logout Successfull", "warning")
    return render_template('home.html')

#HOME ROUTE
# route for home 
@app.route('/')
def home():
    return render_template("home.html")

# route for trigr in patient page
@app.route('/appointment/details')
def appointment_details():
    posts=Trigr.query.all()
    return render_template('trigers.html',posts=posts) 

# route for patients page after login
@app.route('/patient/home')
def patient_home():
    return render_template('patienthome.html')    

# route for patients page after login booking details
@app.route('/getall/bookpatient')
def patient_getbooking():
    return render_template('patientbookdet.html') 

# route for patients page after login slot book
@app.route('/bookall/slot')
def patient_slotbook():
    return render_template('pbookslot.html')     


# route for Doctors page after login
@app.route('/doctor/home')
def doctor_home():
    return render_template('doctorhome.html')    

# route for Doctors page after login doctordept
@app.route('/getall/doctordept')
def doctor_getdept():
    return render_template('doctorhomedept.html')        

# route for Doctors page after login trigerdoct
# @app.route('/getall/trigerdoct')
# def doctor_trigerdoct():
#  posts=Trigrdoct.query.all()
#     return render_template('trigerdoct.html')      

# route for patients slot booking
@app.route('/patient/booking', methods= ['GET','POST'])
def patient_booking():
     doct=db.engine.execute("SELECT * FROM `doctorsdept` ")
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
        
        # method to insert data in patientbook class
        entry = Patientsbook(email = email, name = name, gender = gender, slot = slot  ,time =time ,date =date ,disease =disease ,dept =dept, number = number)
        db.session.add(entry)
        db.session.commit()
        flash("Booking Confirmed", "info")

        # insert query for trigr
        db.engine.execute("CREATE TRIGGER `patientinsertion` AFTER INSERT ON `patientsbook`FOR EACH ROW INSERT INTO trigr VALUES(null,NEW.pid,NEW.email,NEW.name,'PATIENT INSERTED',NOW());")
        # update query for trigr
        db.engine.execute("CREATE TRIGGER `patientupdated` AFTER UPDATE ON `patientsbook` FOR EACH ROW INSERT INTO trigr VALUES(null,NEW.pid,NEW.email,NEW.name,'PATIENT UPDATED',NOW());")
        # delete query for trigr
        db.engine.execute("CREATE TRIGGER `patientdeleted` BEFORE DELETE ON `patientsbook` FOR EACH ROW INSERT INTO trigr VALUES(null,OLD.pid,OLD.email,OLD.name,'PATIENT DELETED',NOW());")
     
     
     return render_template('patientbooking.html',doct=doct)    

# route for booking details page
@app.route('/booking/details')
# @login_required
def booking_details(): 
    # em=current_user.email
    em=params['email']
    # print(em)
    # em="priya@gmail.com"
    query=db.engine.execute(f"SELECT * FROM patientsbook WHERE email='{em}'")
    # query=db.engine.execute(f"SELECT * FROM [dbo].[patientsbook] WHERE email='{em}'")
    return render_template('bookingdetails.html', query=query)

# route for edit patient details page
@app.route("/edit/<string:pid>",methods=['POST','GET'])
# @login_required
def edit(pid):
    posts=Patientsbook.query.filter_by(pid=pid).first()
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

        # update query in patientbook class
        db.engine.execute(f"UPDATE Patientsbook SET email = '{email}', name = '{name}', gender = '{gender}', slot = '{slot}', disease = '{disease}', time = '{time}', date = '{date}', dept = '{dept}', number = '{number}' WHERE Patientsbook.pid = '{pid}'")       
        flash("Slot is Updates","info")
        return redirect('/booking/details')
    return render_template('edit.html',posts=posts)

# route for delete in booking details page
@app.route("/delete/<string:pid>",methods=['POST','GET'])
# @login_required
def delete(pid):  
    # delete query in patientbook class
    # db.engine.execute(f"DELETE FROM [dbo].[Patientsbook] WHERE Patientsbook.pid={pid}")
    db.engine.execute(f"DELETE FROM Patientsbook WHERE Patientsbook.pid={pid}")
    flash("slot Deleted Successfully", "warning") 
    return redirect(url_for('booking_details'))   

# route for doctors department booking
@app.route('/doctor/department', methods=['POST', 'GET'])
def doctor_department():
    if request.method=="POST":
        email=request.form.get('email')
        doctorname=request.form.get('doctorname')
        dept=request.form.get('dept')

        #method to insert data in doctordept class
        entry=Doctorsdept(email=email, doctorname = doctorname, dept=dept)
        db.session.add(entry)
        db.session.commit()
        flash("Information is Stored","info")

        #query for insert trigrdoct
        # db.engine.execute("CREATE TRIGGER `doctorsdeptinsertion` AFTER INSERT ON `doctorsdept` FOR EACH ROW INSERT INTO trigrdoct VALUES( NEW.ddid, NEW.email, NEW.doctorname, 'DOCTOR DEPARTMENT INSERTED',NOW());")
        
    return render_template("doctordepartment.html")    



if __name__ == '__main__':
    app.run(debug=True)