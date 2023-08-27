from flask import Flask
from flask_socketio import SocketIO
from pymongo import MongoClient
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
import os
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import datetime


load_dotenv()

app=Flask(__name__)



bcrypt=Bcrypt(app)



app.config['SECRET_KEY'] = 'secret!'
app.config['JWT_SECRET_KEY']=os.getenv('jwt_secret_key')
app.config['JWT_ACCESS_TOKEN_EXPIRES']=datetime.timedelta(days=1545)

JWTManager(app)

dbconnection=os.getenv('db_connection_string')

client=MongoClient(dbconnection)

db=client.jchat

socketio=SocketIO(app)
CORS(app,origins=["chrome-extension://ophmdkgfcjapomjdpfobjfbihojchbko", "*"])

from src.routes import auth
from src.routes import chat