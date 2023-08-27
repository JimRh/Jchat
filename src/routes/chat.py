from flask import request,jsonify,render_template
from src import app,db
from src.models import User,Friend
import json
from bson.json_util import dumps
from flask_jwt_extended import jwt_required,get_jwt_identity
from src import socketio
from flask_socketio import join_room, leave_room, send, SocketIO

rooms=[]

@app.get('/profile')
@jwt_required()
def getprofile():
    userid=get_jwt_identity()
    user_data=db.user.find({
        "_id":userid
    })
    user_data_json=json.loads(dumps(user_data))
    if len(user_data_json) !=0:
        return jsonify(
            {
                "success":True,
                "message":{
                "data":{
                    "userid":user_data_json[0]['_id'],
                    "username":user_data_json[0]['username']
                }
                }
            }
        )
    else:
        return jsonify(
            {
                "success":False,
                "message":'user is not found'
            }
        )

@app.post('/addfriend')
@jwt_required()
def addfreind():
    request_data=request.get_json()
    if request_data and 'friendname' in request_data:
        userid=get_jwt_identity()
        friendname=request.json['friendname']
        friend_data=db.user.find({
            "username":friendname
        })
        user_data_json=json.loads(dumps(friend_data))
        if len(user_data_json)!=0:
             friend_exist=db.friendlist.find({
                "userid":userid,
                "friendname":friendname
            })
             friend_exist_json=json.loads(dumps(friend_exist))
             if len(friend_exist_json)==0:
                friend=Friend()
                friend.create_friend(friendname,userid)

                return jsonify(
                    {
                        "success":True,
                        "message":
                        f'{friendname} has been added as friend successfully'
                        
                    }
                )
             else:
                 return jsonify(
                    {
                        "success":False,
                        "message":
                        f'{friendname} is alreay in friendlist'
                        
                    }
                )
        else:
            return jsonify(
                {
                    "success":False,
                        "message":
                        f'{friendname} doesn\'t exists'
                        
                }
            )

    else:
        return jsonify(
            {
                "success":False,
                "message":'Please Give friendname'
            }
        )


@app.get('/join')

def join():
    username='jim'
    friendname='anas'
    roomname= f'room _{friendname}_{username}'
    rooms.append(roomname)
    return render_template('room.html')



@socketio.on('joinroom')
def join_room():

    '''username=data['username']
    friendname=data['friendname']'''
    username='jim'
    friendname='anas'
    roomname= f'room _{friendname}{username}'
    join_room(roomname)
    send('joined', {'message': 'You joined the chat room'})
    print('user has joined')



