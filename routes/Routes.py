from flask import request, jsonify;
from database.users.usersQuerys import UsersDB; 

def Routes(app):
    registerUser(app);

def registerUser(app):
    @app.route("/api/registerUser", methods=["POST"])
    def function():
        if request.method == "POST":
            data = request.json;
            UsersDB.registerUserInDb(data);

            return jsonify([data]);

