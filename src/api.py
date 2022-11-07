from flask import Flask, request, make_response, jsonify
from flask_mongoengine import MongoEngine

# ========================================[ Config ]========================================

app = Flask(__name__)

DB_URI = "mongodb+srv://w4sp_17:1234ABCD@cluster0.0uaoxe7.mongodb.net/?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI
db = MongoEngine()
db.init_app(app)

# ========================================[ Modelos ]========================================

class Usuario(db.Document):
    correo = db.StringField(max_length=200, required=True, min_length=3, unique=True)
    contrasenia = db.StringField(max_length=200, required=True, min_length=3)
    nombre = db.StringField(max_length=100)
    apellido = db.StringField(max_length=100)
    roles = db.ListField()

    def to_json(self):
        return {
            "correo" : self.correo,
            "nombre" : self.nombre,
            "apellido" : self.apellido,
            "roles": self.roles
        }

# ========================================[ Variables Globales ]========================================

error_codes = {
    "101" : "El usuario ya existe.",
    "102" : "El usuario no existe.",
    "103" : "El rol ingresado es incorrecto.",
    "104" : "Combinación incorrecta de correo y contraseña.",
}

# ========================================[ Utilidades ]========================================

def buildMsg(msg):
    return jsonify({"msg": msg})

def buildErrorMsg(code):
    return jsonify({"error_msg": error_codes[code]})

# ========================================[ Requerimientos Obligatorios ]========================================

@app.get('/api/error_codes')
def api_error_codes():   
    return make_response(jsonify({"error_codes": error_codes}), 201)

@app.post('/api/db_populate')
def api_db_populate():
    algunoCreado = False

    user_document = Usuario.objects(correo="martin@gmail.com").first()
    if not user_document:
        user = Usuario(correo="martin@gmail.com", contrasenia="holam", nombre="Martín", apellido="Boiwko")
        user.save()
        algunoCreado = True
    
    user_document = Usuario.objects(correo="nestor@gmail.com").first()
    if not user_document:
        user = Usuario(correo="nestor@gmail.com", contrasenia="holan", nombre="Néstor", apellido="Pérez")
        user.save()
        algunoCreado = True

    user_document = Usuario.objects(correo="joaquin@gmail.com").first()
    if not user_document:
        user = Usuario(correo="joaquin@gmail.com", contrasenia="holaj", nombre="Joaquin", apellido="Bandini")
        user.save()
        algunoCreado = True
    
    return make_response(buildMsg("Los datos por defecto fueron cargados."), 201 if algunoCreado else 200)

@app.post('/api/users')
def api_user_create():
    body = request.json
    correo = body["correo"]
    
    user_document = Usuario.objects(correo=correo).first()
    if user_document:
       return make_response(buildErrorMsg("101"), 200)

    contrasenia = body["contrasenia"]
    nombre = body["nombre"]
    apellido = body["apellido"]

    user = Usuario(correo=correo, contrasenia=contrasenia, nombre=nombre, apellido=apellido)
    user.save()

    return make_response(buildMsg("Usuario creado!"), 201)

@app.post('/api/login')
def api_iniciar_sesion():
    body = request.json

    user_ok = False
    user_document = Usuario.objects(correo=body["correo"]).first()

    if user_document:
        if user_document.contrasenia == body["contrasenia"]:
            user_ok = True

    return make_response(jsonify({"conectado": user_ok}), 200 if user_ok else 403)

# @app.put('/api/users/<correo>/roles')
# def update_user(correo):
    # user_document = Usuario.objects(correo=correo).first()
    # if user_document:
    #     roles = user_document.roles
    #     roles.append("testRol1")
    #     user_document.update(roles=roles)
    #     return make_response(buildMsg("Usuario modificado!"), 200)
    # else:
    #     return make_response(buildErrorMsg("102"), 200)

# ========================================[ Otros Endpoints ]========================================

@app.get('/api/users')
def api_user_list():
    users = []
    for user_document in Usuario.objects:
        users.append(user_document.to_json())
    return make_response(jsonify(users), 200)

@app.get('/api/users/<correo>')
def api_user_find(correo):
    user_document = Usuario.objects(correo=correo).first()
    if user_document:
        return make_response(jsonify(user_document.to_json()), 200)
    else:
        return make_response(buildErrorMsg("102"), 200)

@app.delete('/api/users/<correo>')
def api_user_delete(correo):
    user_document = Usuario.objects(correo=correo).first()
    if user_document:
        user_document.delete()
        return make_response("", 204)
    else:
        return make_response(buildErrorMsg("102"), 200)

# ========================================[ Main ]========================================

if __name__ == '__main__':
    app.run()
