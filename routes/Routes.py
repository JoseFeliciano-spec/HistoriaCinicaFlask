from re import I
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
    regInformationUser(app);

def registerUser(app):
    @app.route("/api/registerUser", methods=["POST"])
    def function():
        if request.method == "POST":
            data = request.json;
            expression = ("id" and "phone" and "email" and "type" and "pass");

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

            isLogin, maps = UsersDB.loginUserInDb(arr);

            if isLogin:
                session["username"] = maps;
                response = {"response": "Estás logueado"};
                return jsonify([response]);
            else:
                response = {"response": "No se puedo iniciar sesión, revise si los campos está correctos o estás verificado"};
                return jsonify([response]);

def regInformationUser(app):
    @app.route("/api/regInfoUser", methods=["POST"])
    def functionRegU():
        if request.method == "POST":
            data = request.json;
            if "username" in session:
                if "hospital" in session["username"]["type"]:
                    #
                    # Proceso para los usuarios del hopsital
                    #
                    if regInformationHospital(data, session):
                        response = {"response" : "Se ha agregado los respectivos datos correspondientes del usuario tipo hospital"}
                        return jsonify([response]);
                    else: 
                        response = {"response" : "Ha ocurrido un error al agregar los datos faltantes"}
                        return jsonify([response]);
                if "paciente" in session["username"]["type"]:
                    if(regInformationPaciente(data, session)):
                        response = {"response" : "Se ha agregado los respectivos datos correspondientes del usuario tipo paciente"}
                        return jsonify([response]);
                    else:
                        response = {"response" : "Ha ocurrido un error al agregar los datos faltantes"}
                        return jsonify([response]);
                return jsonify({"response" : "No es ningún tipo de los usuarios que se admiten"});
            else:
                response = {"response" : "No estás logueado"};
                return jsonify([response]);

###
### No es un endpoint va directamente ligado a 
### regInformationUse
###
def regInformationHospital(data, session):
    map = {};
    
    expType = (not "name" in data.keys()) or ( not "address" in data.keys()) or (not "serviceMedical" in data.keys());
    
    if expType:
        return False;
    map = {
        "name" : data["name"],
        "address": data["address"],
        "serviceMedical" : data["serviceMedical"] 
    }
    if UsersDB.regBasicInfoHospital(map, session["username"]):
        return True;
    else: 
        return False;

###
### No es un endpoint va directamente ligado a 
### regInformationUse
###
def regInformationPaciente(data, session):
    map = {};
    exptType = (not "name" in data.keys()) or (not "address" in data.keys());

    if exptType:
        return False;

    map = {
        "name" : data["name"],
        "address" : data["address"]
    }


    if UsersDB.regBasicInfoUser(map, session["username"]):
        return True;
    else:
        return False;