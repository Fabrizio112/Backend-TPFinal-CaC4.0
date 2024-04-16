from ..utils.extensions import db,ma

class User(db.Model):   
    id=db.Column(db.Integer, primary_key=True)   
    name=db.Column(db.String(100))
    username=db.Column(db.String(100))
    email=db.Column(db.String(200))
    avatar=db.Column(db.String(400))
    def __init__(self,name,username,email,avatar):   
        self.name=name   
        self.username=username
        self.email=email
        self.avatar=avatar

class UsuarioSchema(ma.Schema):
    class Meta:
        fields=('id','name','username','email','avatar')

user_schema=UsuarioSchema()            
users_schema=UsuarioSchema(many=True)