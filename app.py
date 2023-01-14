from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)



# database connection
app = app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://priya01:Priya#8789@pc-test.database.windows.net/hmsdb?driver=SQL+Server"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User:
    uid = db.Column(db.Integer,primary_key = True)
    username =  db.Column(db.String(100))  

@app.route('/')
def index():
    return ("test page")

