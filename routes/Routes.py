from re import I
from flask import json, request, jsonify, session;
from database.users.usersQuerys import UsersDB;
from database.medics.medicQuery import MedicDB; 
from utils.verifyEmail import verifyEmail; 
from utils.createSecret import createSecret;


def Routes(app):
    """ Crear la secret key """
    app.secret_key = createSecret();

    """ Las rutas. """
    #Registrar usuarios en general
    registerUser(app);
    #Verificar ese susodicho usuario
    verifyUser(app);
    #Logear el usuario
    loginUser(app);
    #Registrar información adicional dependiendo el tipo de usuario ya sea hospital o paciente
    regInformationUser(app);
    #Registrar un médico, (solamente los usuarios tipo hospital)
    registerMedic(app);
    #Loguear al médico.
    loginMedic(app);
    #Cambiar contraseña primera vez (sólo médico)
    changePassMedic(app);
    #Introducir las observaciones (sólo los médicos)
    regObservationP(app)
    #Imprimir la información
    printInformation(app)

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

#Método que se utilizará por una sola vez (después de loguearse por primera vez);
def changePassMedic(app):
    @app.route("/api/changePassMedic", methods=["PUT"])
    def functionChangeM():
        if request.method == "PUT":
            data = request.json;
            if "medico" in session:
                newPass = data["newPass"];
                if MedicDB.firtTime(session["medico"]["id"]):
                    arr = [newPass, session["medico"]["id"]]
                    if MedicDB.changePasswordM(arr):
                        response = {"response" : "Se ha cambiado la contraseña de manera satisfactoria"};

                        return jsonify([response]);
                    response =  {"response" : "Ha ocurrido un error y no se ha podido cambiar la contraseña"};
                    return jsonify([response]);
                else:
                    response = {"response": "Ya expiró la primera vez para cambiar la contraseña"};
                    return jsonify([response]);
            else:
                response = {"response": "Necesita loguearse para ejecutar esta función"};
                return jsonify([response]);

def loginMedic(app):
    @app.route("/api/loginMedic", methods=["POST"])
    def functionLogM():
        if request.method == "POST":
            data = request.json;
            expressionR = (
                not "id" in data.keys() or not "pass" in data.keys()
            );

            if expressionR:
                response = {"response" : "Faltan aún datos"};
                return jsonify([response]);

            arr = [data["id"], data["pass"]]
            
            isLoginMedico, map = MedicDB.loginMedicInDb(arr);

            if isLoginMedico: 
                session["medico"] = map;
                
                if "medico" in session:
                    print(session["medico"]);

                response = {"response": "Se ha logueado el médico correctamente"}
                return jsonify([response]);
            else:
                response = {"response" : "Ha ocurrido un error al momento de loguearse"}
                return jsonify([response]);

def registerMedic(app):
    @app.route("/api/registerMedic", methods=["POST"])
    def functionRegM():
        if request.method == "POST":
            data = request.json;
            if "username" in session:
                if "hospital" in session["username"]["type"]:
                    expression = (not "email" in data.keys()) or (not "id" in data.keys()) or (not "name" in data.keys()) or (not "pass" in data.keys()) or (not "spec" in data.keys());

                    if expression:
                        response = {"response" : "Faltan datos por recopilar"}
                        return jsonify([response]);

                    if(UsersDB.registerMedic(data, session["username"])):
                        response = {"response" : "Se ha registrado el médico."}
                        return jsonify([response]);
                    else:
                        response = {"response" : "Ha ocurrido un error al momento de registrar el médico. Revisar la base de datos o los campos sin están vacíos."}
                        return jsonify([response]);
                else:
                    response = {"response" : "No tiene los permisos suficientes cómo para realizar esta acción"}
                    return jsonify([response]);
            else:
                response = {"response" : "No estás logueado"};
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


"""
    Insertar observaciones por parte del médico al paciente.
"""
def regObservationP(app):
    @app.route("/api/regObservationP", methods=["POST"])
    def obserPacient():
        if request.method == "POST":
            data = request.json;
            if "medico" in session:
                if expressionPacient(data):
                    response = {"response" : "Faltan datos por ingresar"};
                    return jsonify([response]);
                if MedicDB.insertObservation(data, session["medico"]):
                    response = {"response" : "El registro de la observación ha sido exitoso"};
                    return jsonify([response]);
                else:
                    response = {"response" : "Ha ocurrido un error al guardar los datos"};
                    return jsonify([response]);
                    
            else:
                response = {"response" : "No está logueado para ejecutar esta acción"};
                return jsonify([response]);
    
    def expressionPacient(data):
        expression = (not "idPaciente" in data.keys()) or (not "healthco" in data.keys()) or (not "observation" in data.keys())
        if expression:
            return True;

"""
    Imprimir todo (Octavo requisito)
"""
def printInformation(app):
    @app.route("/api/printInformation", methods=["POST"])
    def printInfos():
        if request.method == "POST":
            if "username" in session:
                if "paciente" in session["username"]["type"]:
                    id = session["username"]["id"];
                    iPrint, data =UsersDB.printObservationUser(id);

                    if iPrint:
                        response  = data;
                        return jsonify(response);

                    response = {"response": "No se ha podido traer de la base de datos los archivos"};
                    return jsonify([response]);
                if "hospital" in session["username"]["type"]:
                    print("Hospital");                    
            if "medico" in session:
                id = session["medico"]["id"];
                print(id);
                iPrint, data = MedicDB.printObservationMedic(id);
                
                if iPrint:
                    response  = data;
                    return jsonify(response);

                response = {"response": "No se ha podido traer de la base de datos los archivos"};
                return jsonify([response]);
            response = {"response" : "No estás logueado, por favor inicie sesión"};

            return jsonify([response]);
