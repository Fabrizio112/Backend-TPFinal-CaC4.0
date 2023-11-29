from flask import Flask ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend


# configuro la base de datos, con el nombre el usuario y la clave
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




    #  si hay que crear mas tablas , se hace aqui




with app.app_context():
    db.create_all()  # aqui crea todas las tablas
#  ************************************************************
class UsuarioSchema(ma.Schema):
    class Meta:
        fields=('id','name','username','email','avatar')




user_schema=UsuarioSchema()            # El objeto usuario_schema es para traer un producto
users_schema=UsuarioSchema(many=True)  # El objeto usuarios_schema es para traer multiples registros de producto




# crea los endpoint o rutas (json)
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
 


# programa principal *******************************
if __name__=='__main__':  
    app.run(debug=True, port=5000)    # ejecuta el servidor Flask en el puerto 5000


