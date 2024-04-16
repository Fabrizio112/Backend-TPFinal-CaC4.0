from flask import Blueprint,jsonify,request
from ..models.User_Login import User_Login
from ..utils.extensions import db,bcrypt

login_routes=Blueprint('login_routes',__name__)


@login_routes.route('/signup', methods=["POST"])
def signup_user():
    name=request.json["name"]
    username=request.json["username"]
    email=request.json["email"]
    password=request.json["password"]

    username_exists=User_Login.query.filter_by(username=username).first()
    email_exists= User_Login.query.filter_by(email=email).first()

    if username_exists:
        return jsonify({"error":"Username Already Exist"})
    if email_exists:
        return jsonify({"error":"Email Already Exist"})


    hashed_password=bcrypt.generate_password_hash(password)
    new_user=User_Login(name=name,username=username,email=email,password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id":new_user.id,
        "name":new_user.name,
        "username":new_user.username,
        "email":new_user.email,
    })

@login_routes.route("/login",methods=["POST"])
def login_user():
    email=request.json["email"]
    password=request.json["password"]

    user=User_Login.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error":"Unauthorized Access"}),401
    
    if not bcrypt.check_password_hash(user.password,password):
        return jsonify({"error":"Unauthorized"}),401

    return jsonify({
        "id":user.id,
        "email":email
    })
