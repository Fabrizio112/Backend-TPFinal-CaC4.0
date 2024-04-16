from ..utils.extensions import db
class User_Login(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    username=db.Column(db.String(100),unique=True)
    email=db.Column(db.String(200),unique=True)
    password=db.Column(db.String(100),nullable=False)
    def __init__(self,name,username,email,password):
        self.name=name
        self.username=username
        self.email=email
        self.password=password