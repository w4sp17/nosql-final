from flask import Flask, request, make_response, jsonify
from flask_mongoengine import MongoEngine

# ========================================[ Config ]========================================

DB_URI = "mongodb+srv://w4sp_17:1234ABCD@cluster0.0uaoxe7.mongodb.net/?retryWrites=true&w=majority"

app = Flask(__name__)
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
    "103" : "No se puede eliminar un rol que el usuario no tiene. Toda la operación fue cancelada, no se efectuaron cambios.",
    "104" : "Combinación incorrecta de correo y contraseña.",
}

# ========================================[ Utilidades ]========================================

def buildMsg(msg):
    return jsonify({"msg": msg})

def buildErrorMsg(code, **extra):
    if extra:
        return jsonify({"error_msg": error_codes[code], "extra": extra})
    else:
        return jsonify({"error_msg": error_codes[code]})

def contraseniasCoinciden(usuarioContrasenia, contraseniaIngresada):
    if usuarioContrasenia == contraseniaIngresada:
        return True
    else:
        return False

# ========================================[ Requerimientos Obligatorios ]========================================

@app.get('/api/error_codes')
def api_error_codes():   
    return make_response(jsonify({"error_codes": error_codes}), 201)

@app.post('/api/users')
def api_user_create():
    body = request.json
    correo = body["correo"]
    
    user_document = Usuario.objects(correo=correo).first()
    if user_document:
       return make_response(buildErrorMsg(code="101"), 200)

    contrasenia = body["contrasenia"]
    nombre = body["nombre"]
    apellido = body["apellido"]

    user = Usuario(correo=correo, contrasenia=contrasenia, nombre=nombre, apellido=apellido)
    user.save()

    return make_response(buildMsg("Usuario creado!"), 201)

@app.put('/api/users/<correo>')
def api_user_update(correo):
    body = request.json
    queryParms = request.args
    roles = body["roles"].split(",")

    user_document = Usuario.objects(correo=correo).first()
    if user_document:
        if not contraseniasCoinciden(user_document.contrasenia, body["contrasenia"]):
            return make_response(buildErrorMsg(code="104"), 403)
        
        eliminarRoles = []
        user_document_roles = user_document.roles

        if queryParms["eliminar"] == "si":
            for rol in roles:
                existe = False
                for user_document_rol in user_document.roles:
                    if user_document_rol == rol:
                        existe = True
                        eliminarRoles.append(rol)
                
                if not existe:
                    return make_response(buildErrorMsg(code="103", extra="Nombre del rol inexistente: " + rol), 200)

            if len(eliminarRoles) == 0:
                mensaje = 'El usuario no tenia ninguno de esos roles!'
            else:
                for eliminarRol in eliminarRoles:
                    user_document_roles.remove(eliminarRol)
                user_document.update(roles=user_document_roles)
                mensaje = f"Usuario modificado! Roles eliminados: " + ','.join(eliminarRoles)

        else:
            nuevoRoles = []
            for rol in roles:
                existe = False

                for user_document_rol in user_document.roles:
                    if user_document_rol == rol:
                        existe = True
                
                if not existe:
                    nuevoRoles.append(rol)

            if len(nuevoRoles) == 0:
                mensaje = 'El usuario ya tenia todos esos roles!'
            else:
                user_document_roles = user_document_roles + nuevoRoles
                user_document.update(roles=user_document_roles)
                mensaje = f"Usuario modificado! Roles agregados: " + ','.join(nuevoRoles)
            
        return make_response(buildMsg(mensaje), 200)
    else:
        return make_response(buildErrorMsg(code="102"), 200)

@app.post('/api/login')
def api_iniciar_sesion():
    body = request.json
    user_ok = False

    user_document = Usuario.objects(correo=body["correo"]).first()
    if user_document:
        if contraseniasCoinciden(user_document.contrasenia, body["contrasenia"]):
            user_ok = True

    return make_response(jsonify({"conectado": user_ok}), 200 if user_ok else 403)

# ========================================[ Otros Endpoints ]========================================

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
        return make_response(buildErrorMsg(code="102"), 200)

@app.delete('/api/users/<correo>')
def api_user_delete(correo):
    user_document = Usuario.objects(correo=correo).first()
    if user_document:
        user_document.delete()
        return make_response("", 204)
    else:
        return make_response(buildErrorMsg(code="102"), 200)

@app.get('/')
def api_home():
    return '''<h1>NOSQL API REST ENDPOINTS</h1>
        <p><b>Ver códigos de errores                    </b><br> (GET)     /api/error_codes</p>
        <p><b>Agregar nuevo usuario                     </b><br> (POST)    /api/users</p>
        <p><b>Modificar usuario - Agregar Rol           </b><br> (PUT)     /api/users/<correo>?eliminar=no</p>
        <p><b>Modificar usuario - Eliminar Rol          </b><br> (PUT)     /api/users/<correo>?eliminar=si</p>
        <p><b>Iniciar Sesion                            </b><br> (POST)    /api/login</p>
        <p><b>Cargar datos de usuarios predeterminados  </b><br> (POST)    /api/db_populate</p>
        <p><b>Mostrar datos de todos los usuarios       </b><br> (GET)     /api/users</p>
        <p><b>Mostrar datos de un usuario               </b><br> (GET)     /api/users/<correo></p>
        <p><b>Eliminar un usuario                       </b><br> (DELETE)  /api/users/<correo></p>'''

# ========================================[ Main ]========================================

if __name__ == '__main__':
    app.run(host='0.0.0.0')
