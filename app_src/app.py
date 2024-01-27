# Error Solution
import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']


"""
For windwos:
set FLASK_APP=app.py
set FLASK_ENV=development

Linux:
export FLASK_APP=app.py
export FLASK_ENV=development
"""

MONGODB_URI = "mongodb+srv://py-fsk-crud-usr:O20vFWeoJInYIgUw@mdbsrv01.qazfb9l.mongodb.net/?retryWrites=true&w=majority"

from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient

from bson.objectid import ObjectId



app = Flask(__name__)

client = MongoClient(MONGODB_URI)


db = client['mdb-py-fsk-crud'] #Assign Database

employees = db['emp'] #Assign Collection

#Start routing

@app.route('/')
def index():
    #return render_template('create.html')
    all_employees = employees.find().sort('_id',-1)
    return render_template('crud-python-flask-mongodb.html', emp=all_employees)

@app.route('/save/', methods=['GET', 'POST', 'PUT'])
def save():
    if request.method=='POST':
        print("Entered .....!!!!")
        print(request.form)

        e_name = request.form['emp_name']
        e_addr = request.form['emp_address']
        e_email = request.form['emp_email']
       
        employees.insert_one({'emp_name': e_name, 'emp_addr': e_addr, 'emp_email':e_email})
        return redirect(url_for('index'))
    elif request.method=='PUT':
        pass

    elif request.method=='GET':
        all_employees = employees.find().sort('_id',-1)
        return render_template('crud-python-flask-mongodb.html', emp=all_employees)
    else:
         return render_template('create.html')
   

upd_id=ObjectId()
@app.post('/upd_save/')
def upd_save():
        
        e_id = request.form['emp_id']
        #print("Form vale of obj:", e_id)
        e_name = request.form['emp_name']
        e_addr = request.form['emp_address']
        e_email = request.form['emp_email']
       
        upd_stat = employees.update_one({"_id": ObjectId(e_id)} ,  {"$set": {'emp_name': e_name, 'emp_addr': e_addr, 'emp_email':e_email}})
        print("update statud:", type(upd_stat))
       
        return redirect(url_for('index'))
    
# ...
@app.get('/create/')
def create_upd():
    return render_template('create.html')

@app.route('/update/<id>/', methods=['GET', 'POST'])
def upd(id):
        #print(id)
        upd_id=id
        employees_by_id = employees.find_one({"_id": ObjectId(id)})
        return render_template('update.html', emp=employees_by_id)


@app.post('/delete/<id>/')
def delete(id):
    employees.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))