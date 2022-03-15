# hemhaw API
# Tyler Weston, March 2022

from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request
from flask_sqlalchemy import SQLAlchemy


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

#CORS(app, resources={r"/*": {"origins": "*"}})
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    hash = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    score = db.Column(db.Integer)

    def __repr__(self):
        #return '<User {}>'.format(self.username)
        return f'{self.username} - {self.score}'


@app.route('/hello')
@cross_origin()
def hello_world():
    return 'Hello from Flask!'

@app.route('/user', methods=['GET', 'POST'])
@cross_origin()
def user():
    if request.method == 'GET':
        # Return a specific user based on its hash, otherwise return nothing
        hash = request.args.get('hash')
        if hash:
            user = User.query.filter_by(hash=hash).first()
            if user:
                return user.__repr__()
            else:
                return 'User not found'
        return 'No hash provided'
    elif request.method == 'POST':
        # Create a new user via user with the supplied username and hash, and empty asides from that
        user = User(username=request.form['name'], hash=request.form['hash'], score=0)
        db.session.add(user)
        db.session.commit()
        return 'Posted user'

@app.route('/score', methods=['GET', 'POST'])
@cross_origin()
def score():
    #return f"{username} scored {word}"
    if request.method == 'GET':
        # Return a list of the top 50 scores in database
        scores = User.query.order_by(User.score.desc()).limit(50)
        return '\n'.join([str(score) for score in scores])

    if request.method == 'POST':
        # update the score of a user, we should take a hash and a score
        hash = request.form['hash']
        score = request.form['score']
        user = User.query.filter_by(hash=hash).first()
        if user:
            user.score += score
            db.session.commit()
            return 'Updated score'
        else:
            return 'User not found'