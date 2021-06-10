from flask import request, jsonify, session;
from database.users.usersQuerys import UsersDB; 
from utils.verifyEmail import verifyEmail; 
from utils.createSecret import createSecret;

def Routes(app):
    """ Crear la secret key """
    app.secret_key = createSecret();

    """ Las rutas. """
    registerUser(app);
    verifyUser(app);
    loginUser(app);

def registerUser(app):
    @app.route("/api/registerUser", methods=["POST"])
    def function():
        if request.method == "POST":
            data = request.json;
            expression = ("id" and "name" and "phone" and "email" and "type" and "pass");

            if(not verifyEmail(data["email"])):
                response  = {"response" : "Email no válido"}
                return jsonify([response]);

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

def verifyUser(app):
    @app.route("/api/verifyUser", methods=["POST"])
    def functionVerify():
        if request.method == "POST":
            if "phone" in request.json.keys():
                print("phone");
            return jsonify("asdasd");

def loginUser(app):
    @app.route("/api/loginUser", methods=["POST"])
    def functionLogin():
        if request.method == "POST":
            data = request.json;
            expression  = "id" and "pass" in data.keys();
            if not expression:
                response  = {"response" : "No están los datos correspondientes"}
                return jsonify([response]);
            
            arr = [data["id"], data["pass"]];

            if UsersDB.loginUserInDb(arr):
                session["username"] = data["id"];
                response = {"response": "Estás logueado"};
                return jsonify([response]);
            else:
                response = {"response": "No se puedo iniciar sesión, revise si los campos está correctos o estás verificado"};
                return jsonify([response]);
            

