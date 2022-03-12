# hemhaw API
# Tyler Weston, March 2022

from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="tylerweston",
    password="297jMLkG!cjfdPf",
    hostname="tylerweston.mysql.pythonanywhere-services.com",
    databasename="tylerweston$hemhaw",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/hello')
def hello_world():
    return 'Hello from Flask!'

@app.route('/score', methods=['GET', 'POST'])
def score():
    #return f"{username} scored {word}"
    if request.method == 'GET':
        # return our list of words
        return {'JarLapris': ['flamboyant'], 'tylerweston': ['zugzwanging']}
    if request.method == 'POST':
        # # extract username and submitted word
        # data = request.form
        print(request.args)
        username = request.args.get('username')
        word = request.args.get('word')
        return f"{username} scored {word}"