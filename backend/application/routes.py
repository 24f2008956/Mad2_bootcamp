from flask import current_app as app
from flask_security import verify_password,auth_required,roles_required,hash_password
from flask import request,render_template
from .models import db
from datetime import datetime
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login" , methods=["GET" , "POST"])
def login():
    if request.method =="POST":
        email = request.json.get("email")
        print(email)
        pws = request.json.get("password")
        try:
            datastore = app.security.datastore
            user= datastore.find_user(email = email)
            if user:
                if verify_password(  pws , user.password):
                    roles = [role.name for role in user.roles]
                    return {"token" : user.get_auth_token() ,"role": roles[0] if roles else "user", "message" : "login successful"} ,200
                else:
                    return {"message" : "incorrect password"} , 401
            else:
                return {"message" : "user not found"} , 404
        except Exception as e:
            db.session.rollback()
            return {"message" : "internal server error"} , 500
  
@app.route("/register" , methods=["GET" , "POST"])
def register():
    if request.method =="POST":
        name = request.json.get("name")
        email = request.json.get("email")
        password = request.json.get("password")
       
        try:
            datastore = app.security.datastore
            user = datastore.find_user(email=email)
            if not user:
                datastore.create_user(name=name ,email = email,password = hash_password(password), roles = ['user'] )
                db.session.commit()
                return {"message":"Registration successful"} , 200
            else:
                return {"message":"User already exists"} , 409
        except Exception as e:
            db.session.rollback()
            return {"message" : "internal server error"} , 500

@app.route("/dashboard/admin")
@auth_required('token')
@roles_required('admin')
def admin_route():
    return "welcome to admin dashboard"