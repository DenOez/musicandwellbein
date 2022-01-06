from flask import Flask
import requests
import json
from flask_sqlalchemy import SQLAlchemy
import time

#this script is pulling favorite tracks of spotify users
#Application-Initializing
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:// ... '
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']=' Enter here the secret key '
db = SQLAlchemy(app)


from app import db
from app import playlist_favorite_tracks
from app import user
from app import limit_top_tracks


userEntries = user.query.all()

for userEntry in userEntries:

    Access_token_fetch = userEntry.access_token

    url = "https://api.spotify.com/v1/me/player/recently-played?limit={}&after=100".format(limit_top_tracks)
    payload = {}
    headers = {'Authorization': 'Bearer {}'.format(Access_token_fetch)}

    fetch_response = requests.get(url, headers=headers, data=payload)
    fetch_data = json.loads(fetch_response.text)

    if fetch_response.status_code == 200:

        i=0
        print("Favorite tracks from user "+ userEntry.ID_code+":")
        for i in range(i, len(fetch_data["items"])):
            track_id=fetch_data["items"][i]["track"]["id"]
            print(track_id)

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

            # saving track-ID in playlist table
            db.session.add(playlist_favorite_tracks(ID_code=userEntry.ID_code,
                                    track_id=fetch_data["items"][i]["track"]["id"],
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
        print("-----------------------")
    else:
        print("Error" + fetch_response.text)
