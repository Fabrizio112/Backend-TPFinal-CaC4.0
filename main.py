from flask import Flask ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

app=Flask(__name__)  # crear el objeto app de la clase Flask
bcrypt=Bcrypt(app)
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend


# configuro la base de datos, con el nombre el usuario y la clave
app.config['SECRET_KEY']='FabrizioAvila1'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:1234@localhost/users'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow


# defino las tablas
class User(db.Model):   # la clase Usuario hereda de db.Model    
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    name=db.Column(db.String(100))
    username=db.Column(db.String(100))
    email=db.Column(db.String(200))
    avatar=db.Column(db.String(400))
    def __init__(self,name,username,email,avatar):   #crea el  constructor de la clase
        self.name=name   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.username=username
        self.email=email
        self.avatar=avatar

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

with app.app_context():
    db.create_all()  # aqui crea todas las tablas
#  ************************************************************
class UsuarioSchema(ma.Schema):
    class Meta:
        fields=('id','name','username','email','avatar')

user_schema=UsuarioSchema()            # El objeto usuario_schema es para traer un producto
users_schema=UsuarioSchema(many=True)  # El objeto usuarios_schema es para traer multiples registros de producto


# crea los endpoint o rutas (json)
# ///////////////////////////////////////USERS////////////////////////////////////
@app.route('/users',methods=['GET'])
def get_users():
    all_users=User.query.all()         # el metodo query.all() lo hereda de db.Model
    result=users_schema.dump(all_users)  # el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los registros de la tabla
    return jsonify(result)                       # retorna un JSON de todos los registros de la tabla

@app.route('/users/<id>',methods=['GET'])
def get_user(id):
    usuario=User.query.get(id)
    return user_schema.jsonify(usuario)   # retorna el JSON de un producto recibido como parametro

@app.route('/users/<id>',methods=['DELETE'])
def delete_users(id):
    user=User.query.get(id)
    db.session.delete(user)
    db.session.commit()                     # confirma el delete
    return user_schema.jsonify(user) # me devuelve un json con el registro eliminado

@app.route('/users', methods=['POST']) # crea ruta o endpoint
def create_user():
    #print(request.json)  # request.json contiene el json que envio el cliente
    name=request.json['name']
    username=request.json['username']
    email=request.json['email']
    avatar=request.json['avatar']
    new_user=User(name,username,email,avatar)
    db.session.add(new_user)
    db.session.commit() # confirma el alta
    return user_schema.jsonify(new_user)

@app.route('/users/<id>' ,methods=['PUT'])
def update_user(id):
    user=User.query.get(id)
 
    user.name=request.json['name']
    user.username=request.json['username']
    user.email=request.json['email']
    user.avatar=request.json['avatar']


    db.session.commit()    # confirma el cambio
    return user_schema.jsonify(user)    # y retorna un json con el producto
 
#///////////////////////////////////////////LOGIN/SIGNUP/////////////////////////////////////////////
 
@app.route('/signup', methods=["POST"])
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

@app.route("/login",methods=["POST"])
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

# programa principal *******************************
if __name__=='__main__':  
    app.run(debug=True, port=5000)    # ejecuta el servidor Flask en el puerto 5000


