from flask import Flask
from flask_cors import CORS  
from .utils.extensions import db,ma,bcrypt

def create_application():
    app=Flask(__name__) 
    CORS(app)

    app.config['SECRET_KEY']='FabrizioAvila1'
    app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:1234@localhost/users'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        db.create_all()
    