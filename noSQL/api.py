from flask import Flask, make_response, request, jsonify
from flask_mongoengine import MongoEngine

app = Flask(__name__)

database_name = "test"
DB_URI = "mongodb+srv://w4sp_17:1234ABCD@cluster0.0uaoxe7.mongodb.net/?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI
db = MongoEngine()
db.init_app(app)

class User(db.Document):
    user_id = db.IntField()
    nombre = db.StringField()
    edad = db.IntField()

    def to_json(self):
        return {
            "user_id" : self.user_id,
            "nombre" : self.nombre,
            "edad" : self.edad,
        }

@app.route('/api/db_populate', methods=['GET', 'POST'])
def db_populate():
    user4 = User(user_id=4, nombre="po", edad=42)
    user4.save()
    return make_response("", 201)

@app.route('/api/users', methods=['GET'])
def api_users():
    users = []
    for user in User.objects:
        users.append(user)
    return make_response(jsonify(users), 200)
    

@app.route('/api/findUser/<user_id>', methods=['GET'])
def find_user(user_id):
    user_obj = User.objects(user_id=user_id).first()
    if user_obj:
        return make_response(jsonify(user_obj.to_json()), 200)

@app.route('/api/updateUser/<user_id>', methods=['GET', 'PUT'])
def update_user(user_id):
    user_obj = User.objects(user_id=user_id).first()
    user_obj.update(nombre="lala", edad=24)
    return make_response("", 204)

@app.route('/api/deleteUser/<user_id>', methods=['GET', 'DELETE'])
def delete_user(user_id):
    user_obj = User.objects(user_id=user_id).first()
    user_obj.delete()
    return make_response("", 205)


if __name__ == '__main__':
    app.run()
