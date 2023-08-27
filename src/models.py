from src import db
import uuid
class User:

    def create_user(self,username,password):

        userdata={
            "_id":uuid.uuid4().hex,
            "username":username,
            "password":password

        }

        db.user.insert_one(userdata)


class Friend:

    def create_friend(self,friendname,userid):
        frienddata={
            "_id":uuid.uuid4().hex,
            "friendname":friendname,
            "userid":userid
        }
        db.friendlist.insert_one(frienddata)

class Chat:

    def create_chat(self,chathistory,userid,room,friendname):

        chatdata={
            "_id":uuid.uuid4().hex,
            "chat":chathistory,
            "userid":userid,
            "room":room,
            "friendid":friendname
        }
        db.chat.insert_one(chatdata)
