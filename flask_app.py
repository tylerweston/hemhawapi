# hemhaw API
# Tyler Weston, March 2022

# Database should store:
#   - User hash
#   - User name
#   - high easy score
#   - high medium score
#   - high hard score
#   - high blitz score

from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
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
    name = db.Column(db.String(32), nullable=False)
    total_score = db.Column(db.Integer)
    easy_score = db.Column(db.Integer)
    medium_score = db.Column(db.Integer)
    hard_score = db.Column(db.Integer)
    blitz_score = db.Column(db.Integer)

    def __repr__(self):
        #return '<User {}>'.format(self.username)
        return f'{self.username} - {self.total_score}'


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
        user = User(name=request.args.get('name'), hash=request.args.get('hash'), total_score=0,
                    easy_score=0, medium_score=0, hard_score=0, blitz_score=0)
        db.session.add(user)
        db.session.commit()
        return 'Posted user'

@app.route('/score', methods=['GET', 'POST'])
@cross_origin()
def score():
    #return f"{username} scored {word}"
    if request.method == 'GET':
        # Return a list of the top 50 scores in database
        scores = User.query.order_by(User.total_score.desc()).limit(50)
        return '\n'.join([str(score) for score in scores])

    if request.method == 'POST':
        print("Received POST request")
        print(request.args)
        # update the score of a user, we should take a hash and a score
        hash = request.args.get('hash')
        total_score = request.args.get('score')
        easy_score = request.args.get('easy_score')
        medium_score = request.args.get('medium_score')
        hard_score = request.args.get('hard_score')
        blitz_score = request.args.get('blitz_score')
        user = User.query.filter_by(hash=hash).first()

        if not user:
            return 'User not found'

        user.total_score += int(total_score)
        if easy_score:
            user.easy_score = int(easy_score)
        if medium_score:
            user.medium_score = int(medium_score)
        if hard_score:
            user.hard_score = int(hard_score)
        if blitz_score:
            user.blitz_score = int(blitz_score)
        
        db.session.commit()
        return 'Updated score'


@app.route('/globalposition', methods=['GET'])
@cross_origin()
def get_global_position():
    print("Getting user global position")
    # get the total number of users in the database
    hash = request.args.get('hash')
    user = User.query.filter_by(hash=hash).first()

    if not user:
        return 'User not found'

    # Order the users by score and get the position of user in that list
    users = User.query.order_by(User.total_score.desc()).all()

    # # SQL query to get rank of user sorted by their total score
    # TODO: Test this out and see if it works or not
    # query = """
    #     SELECT @rank := @rank + 1 AS rank, u.hash, u.name, u.score
    #     FROM users u, (SELECT @rank := 0) r
    #     ORDER BY u.score DESC
    # """

    # # Execute the query
    # result = db.engine.execute(query)

    # Get the first row of the result

    position = 1
    for user in users:
        if user.hash == hash:
            break
        position += 1

    # get the total number of users
    total_users = User.query.count()

    result = f'{str(position)}/{str(total_users)}'
    print(result)
    return result