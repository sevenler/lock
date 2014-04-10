from mongoengine import *
from flask import Flask
from flask import request
import json

app = Flask(__name__)
connect('test',host='localhost', port=27017, username = 'root', password = '123456')

class Employee(Document):
    username = StringField(max_length=50)
    age = IntField(required=False)
    email = StringField(max_length=50)
    password = StringField(max_length=50)
    introdution = StringField(max_length=200)
    
    def to_json(self):
        result = {
                  'username':self.username,
                  'age':self.age,
                  'email':self.email,
                  'introdution':self.introdution,
                 }
        return json.dumps(result)
        
@app.route('/regester', methods=['GET', 'POST'])
def regester():
    if request.method == 'POST':
        Email= request.form['email']
        if(uniqueness(Email)) == True:
            employ = Employee(username=request.form['username'], password=request.form['password'], 
                          email= Email, age=0, introdution=request.form['introdution'])
            employ.save()
            return employ.to_json()
        else:
            return response_error('exsit email address ')
    else:
        return response_error("error request")
        
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        Email = request.form['email']
        Password = request.form['password']
        e = Employee.objects.__call__(email=Email, password=Password).first()
        if e is None:
            return response_error('user not exsit')
        else: 
            print e["id"], e["username"], e["age"]
            return e["username"]
    else:
        return response_error("error request")
    
def uniqueness(Email):
    e = Employee.objects.__call__(email=Email).first()
    if e is None:
        return True
    else:
        return False
    
def response_error(Message):
    result = {
                  'message':Message,
                  'code':400
                 }
    return json.dumps(result)
        
def update():
    Email = "johnnyxyz@gmail.com"
    e = Employee.objects.__call__(email=Email).first()
    e["username"]="johnnyxyz"
    e.save()
    print e["id"], e["username"], e["age"]
    
if __name__ == '__main__':
    for e in Employee.objects:
        print e["username"]
    app.run(debug=True, host='localhost', port=8888)
