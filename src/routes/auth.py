from flask import request,jsonify
from src import app,db
from src.models import User
from src import bcrypt
import json
from bson.json_util import dumps
from flask_jwt_extended import create_access_token,create_refresh_token



@app.post('/auth/register')

def register():
    request_data = request.get_json()
    if request_data and 'username' in request_data and 'password' in request_data:
        username=request.json['username']
        password=request.json['password']
        
        userdata=db.user.find({
            "username":username
        })
        userdata_json=json.loads(dumps(userdata))
       
        if len(userdata_json)==0:
            hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
            user=User()
            user.create_user(username,hashed_password)
            return jsonify(
                {
                    "success":True,
                    "message":"user has been created successfully"
                }
            )
        else:
            return jsonify(
                {
                    "success":False,
                    "Message":"username already exists"
                }
            )



    else:
        return jsonify (
            {
                "success":False,
                "message":"username and password is not sent"
            }
        )
    

@app.post('/auth/login')

def login():
    request_data = request.get_json()
    if request_data and 'username' in request_data and 'password' in request_data:
        username=request.json['username']
        password=request.json['password']
        
        userdata=db.user.find({
            "username":username
        })
        userdata_json=json.loads(dumps(userdata))
        if len(userdata_json)!=0:
            userid=userdata_json[0]['_id']
            hashed_password=userdata_json[0]['password']
            
            check_password=bcrypt.check_password_hash(hashed_password, password)
            if check_password:
                access_token=create_access_token(userid)
                refresh_token=create_refresh_token(userid)
                return jsonify(
                    {
                        "success":True,
                        "message":"user logs in succesfully",
                        "access_token":access_token,
                        "refresh_token":refresh_token
                    }
                )
            else:
                return jsonify(
                {
                    "success":False,
                    "Message":"Wrong Credentials.Please Try again."
                }
            )
            


        else:
            return jsonify(
                {
                    "success":False,
                    "Message":"Wrong Credentials.Please Try again."
                }
            )



    else:
        return jsonify (
            {
                "success":False,
                "message":"username and password is not sent"
            }
        )
    

