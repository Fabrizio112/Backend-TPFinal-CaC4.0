from flask import Blueprint,jsonify,request
from ..models.User import User,user_schema,users_schema
from ..utils.extensions import db


user_router=Blueprint('user_router',__name__)


@user_router.route('/users',methods=['GET'])
def get_users():
    all_users=User.query.all()         
    result=users_schema.dump(all_users)                                            
    return jsonify(result)                      

@user_router.route('/users/<id>',methods=['GET'])
def get_user(id):
    usuario=User.query.get(id)
    return user_schema.jsonify(usuario)  

@user_router.route('/users/<id>',methods=['DELETE'])
def delete_users(id):
    user=User.query.get(id)
    db.session.delete(user)
    db.session.commit()                    
    return user_schema.jsonify(user) 

@user_router.route('/users', methods=['POST']) 
def create_user():
    name=request.json['name']
    username=request.json['username']
    email=request.json['email']
    avatar=request.json['avatar']
    new_user=User(name,username,email,avatar)
    db.session.add(new_user)
    db.session.commit() 
    return user_schema.jsonify(new_user)

@user_router.route('/users/<id>' ,methods=['PUT'])
def update_user(id):
    user=User.query.get(id)
    user.name=request.json['name']
    user.username=request.json['username']
    user.email=request.json['email']
    user.avatar=request.json['avatar']
    db.session.commit()   
    return user_schema.jsonify(user)  
 