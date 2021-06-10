from flask import request, jsonify;

def Routes(app):
    registerUser(app);

def registerUser(app):
    @app.route("/api/registerUser", methods=["POST"])
    def registerUser():
        if request.method == "POST":
            data = request.json;
            print("holaasdad");
            return jsonify([data]);

