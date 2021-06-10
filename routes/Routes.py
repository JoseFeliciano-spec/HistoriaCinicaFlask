from flask import request, jsonify;
from database.users.usersQuerys import UsersDB; 

def Routes(app):
    registerUser(app);

def registerUser(app):
    @app.route("/api/registerUser", methods=["POST"])
    def function():
        if request.method == "POST":
            data = request.json;
            expression = ("id" and "name" and "phone" and "email" and "type" and "pass");
            if(expression in data.keys()):
                expressionType = "hospital" == data["type"] or "paciente" == data["type"];
                if expressionType: 
                    if UsersDB.registerUserInDb(data):
                        response = {"response" : "Se registró el usuario"};
                        return jsonify([response]);
                    else:
                        response = {"response" : "No se registró el usuario"};
                        return jsonify([response]);
                else:
                    response ={"response" : "No corresponde a ningún tipo de usuario que se acepte"};
                    return jsonify([response]);
            else:
                response ={"response" : "Faltan datos"};
                return jsonify([response]);

