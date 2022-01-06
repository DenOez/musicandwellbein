from flask import Flask
import requests
import json
from flask_sqlalchemy import SQLAlchemy
import time

#this script is tracking the current playing track of spotify user and stores
#the data inclusive track features in table "playlist_current_playing"

#Application-Initializing
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:// ...'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']=' Enter here the secret key '
db = SQLAlchemy(app)

from app import db
from app import playlist_current_playing
from app import user
from app import tracking_time_interval

timer_fetch=0


while 1:
    time.sleep(1)
    timer_fetch=timer_fetch+1
    print('tik')

    userEntries = user.query.all()

    if timer_fetch==tracking_time_interval:

        for userEntry in userEntries:
            #in this part the application requests information about the current playing track of spotify user
            Access_token_fetch = userEntry.access_token
            url = "https://api.spotify.com/v1/me/player/currently-playing?access_token={}".format(Access_token_fetch)
            fetch_response = requests.get(url)

            if (fetch_response.status_code == 200):

                fetch_data = json.loads(fetch_response.text)

                if (fetch_data["is_playing"]) == True:

                    print('User mit Code:'+ userEntry.ID_code +' hört gerade TRACK: ' + fetch_data["item"]["id"])

                    track_id = fetch_data["item"]["id"]
                    url_features = "https://api.spotify.com/v1/audio-features/{}".format(track_id)

                    payload = {
                        "grant_type": "access_token",
                        "refresh_token": "{}".format(userEntry.refresh_token)
                    }

                    headers = {
                        "Authorization": "Bearer {}".format(userEntry.access_token)
                    }
                    feature_response = requests.request("GET", url_features, headers=headers)
                    feature_response_json = json.loads(feature_response.text)
                    feature_response_key = feature_response_json["key"]
                    feature_response_mode = feature_response_json["mode"]
                    feature_response_time_signature = feature_response_json["time_signature"]
                    feature_response_acousticness = feature_response_json["acousticness"]
                    feature_response_danceability = feature_response_json["danceability"]
                    feature_response_energy = feature_response_json["energy"]
                    feature_response_instrumentalness = feature_response_json["instrumentalness"]
                    feature_response_liveness = feature_response_json["liveness"]
                    feature_response_loudness = feature_response_json["loudness"]
                    feature_response_speechiness = feature_response_json["speechiness"]
                    feature_response_valence = feature_response_json["valence"]
                    feature_response_tempo = feature_response_json["tempo"]


                    #storing track ID in playlist_current_playing table
                    db.session.add(playlist_current_playing(ID_code=userEntry.ID_code,
                                            track_id=fetch_data["item"]["id"],
                                            key=feature_response_key,
                                            mode=feature_response_mode,
                                            time_signature=feature_response_time_signature,
                                            acousticness=feature_response_acousticness,
                                            danceability=feature_response_danceability,
                                            energy=feature_response_energy,
                                            instrumentalness=feature_response_instrumentalness,
                                            liveness=feature_response_liveness,
                                            loudness=feature_response_loudness,
                                            speechiness=feature_response_speechiness,
                                            valence=feature_response_valence,
                                            tempo=feature_response_tempo))
                    db.session.commit()


                else:
                    print('User mit Code:'+userEntry.ID_code +' hat Player gerade pausiert')
            else:
                print('User mit ID Code:'+userEntry.ID_code +' hat Gerät deaktiviert')
        print('---------------------------------------TRACKING DONE---------------------------------------')

        timer_fetch = 0
