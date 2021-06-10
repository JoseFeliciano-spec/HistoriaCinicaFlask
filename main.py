from flask import Flask, jsonify, request;
from database.connectDb import connectDb;
from routes.Routes import Routes;

app = Flask(__name__);

Routes(app);

print(connectDb());
app.run(debug=True);