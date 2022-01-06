from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from random import *
import psycopg2

#threading is not working so far:
#import threading
#from exchange_auth import auth_refresh

app = Flask(__name__)
global tracking_time_interval

#limit_top_tracks = the number of most listened tracks of spotify user (max=50)
limit_top_tracks = 50


#connect to local or postgreSQL database in standard convention
#[DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]
#ENV = dev set the application to development mode

ENV = 'prod'
if ENV == 'dev':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:DJ625ffpg!@localhost:1080/auth_codes'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://wcsjlzdafuaqjn:f41ee927192bf7489d25d75f89e5117b7f3e8b08691dcf66ee01223bf2310c2c@ec2-52-21-153-207.compute-1.amazonaws.com:5432/dbbigmbi6vhm7'

#settings for database and responsive web design
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'b49eeb10e86e4aa308d59ecde23d4c14'
db = SQLAlchemy(app)
bootstrap=Bootstrap(app)


#defining database models
class user(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, nullable=True, autoincrement=True)
    ID_code = db.Column(db.String(120), nullable=True)
    auth_code = db.Column(db.String(300), nullable=False)
    access_token = db.Column(db.String(300), nullable=True)
    refresh_token = db.Column(db.String(200), nullable=True)

    def __init__(self, ID_code, auth_code, access_token, refresh_token):
        self.ID_code = ID_code
        self.auth_code = auth_code
        self.access_token = access_token
        self.refresh_token = refresh_token


class playlist_current_playing(db.Model):
    __tablename__ = 'playlist_current_playing'
    id = db.Column(db.Integer, primary_key=True)
    ID_code = db.Column(db.String(120), nullable=True)
    track_id = db.Column(db.String(120), nullable=True)
    key = db.Column(db.Integer, nullable=True)
    mode = db.Column(db.Integer, nullable=True)
    time_signature = db.Column(db.Integer, nullable=True)
    acousticness = db.Column(db.Float, nullable=True)
    danceability = db.Column(db.Float, nullable=True)
    energy = db.Column(db.Float, nullable=True)
    instrumentalness = db.Column(db.Float, nullable=True)
    liveness = db.Column(db.Float, nullable=True)
    loudness = db.Column(db.Float, nullable=True)
    speechiness = db.Column(db.Float, nullable=True)
    valence = db.Column(db.Float, nullable=True)
    tempo = db.Column(db.Float, nullable=True)

    def __init__(self, ID_code, track_id, key, mode, time_signature, acousticness, danceability, energy,
                 instrumentalness, liveness, loudness, speechiness, valence, tempo):
        self.ID_code = ID_code
        self.track_id = track_id
        self.key = key
        self.mode = mode
        self.time_signature = time_signature
        self.acousticness = acousticness
        self.danceability = danceability
        self.energy = energy
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.loudness = loudness
        self.speechiness = speechiness
        self.valence = valence
        self.tempo = tempo


class playlist_favorite_tracks(db.Model):
    __tablename__ = 'playlist_favorite_tracks'
    id = db.Column(db.Integer, primary_key=True)
    ID_code = db.Column(db.String(120), nullable=True)
    track_id = db.Column(db.String(120), nullable=True)
    key = db.Column(db.Integer, nullable=True)
    mode = db.Column(db.Integer, nullable=True)
    time_signature = db.Column(db.Integer, nullable=True)
    acousticness = db.Column(db.Float, nullable=True)
    danceability = db.Column(db.Float, nullable=True)
    energy = db.Column(db.Float, nullable=True)
    instrumentalness = db.Column(db.Float, nullable=True)
    liveness = db.Column(db.Float, nullable=True)
    loudness = db.Column(db.Float, nullable=True)
    speechiness = db.Column(db.Float, nullable=True)
    valence = db.Column(db.Float, nullable=True)
    tempo = db.Column(db.Float, nullable=True)

    def __init__(self, ID_code, track_id, key, mode, time_signature, acousticness, danceability, energy,
                 instrumentalness, liveness, loudness, speechiness, valence, tempo):
        self.ID_code = ID_code
        self.track_id = track_id
        self.key = key
        self.mode = mode
        self.time_signature = time_signature
        self.acousticness = acousticness
        self.danceability = danceability
        self.energy = energy
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.loudness = loudness
        self.speechiness = speechiness
        self.valence = valence
        self.tempo = tempo



#index page routing
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

#login page routing
@app.route('/login')
def login():
    return render_template("login.html")

#callback page routing
@app.route('/callback')
def callback():
    x = request.args.get('code')
    new_ID = randint(1, 1000000)

    new_post = user(ID_code=new_ID, auth_code=x, access_token=0, refresh_token=0)
    db.session.add(new_post)
    db.session.commit()

    return render_template("callback.html",value=new_ID)


if __name__ == "__main__":

    #threading is not working so far
    #threading.Thread(target=auth_refresh).start()

    if ENV == 'dev':
        app.run(host='localhost', port=8888, debug=True, threaded=True)
    else:
        app.run(debug=False, threaded=True)
