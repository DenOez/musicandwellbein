import requests
import json
import time

#first part is exchanging the authorization code with an access and refresh token
#second part is refreshing the access token

def auth_refresh():
    from app import user
    from app import db

    while 1:

        # list of objects where acces_token is 0
        userEntries = user.query.filter_by(access_token='0')

        for userEntry in userEntries:

            #first part:
            Auth_code_data = userEntry.auth_code
            Auth_ID_code = userEntry.ID_code

            url = "https://accounts.spotify.com/api/token"

            payload = {
                "grant_type": "authorization_code",
                "code": "{}".format(Auth_code_data),
                "redirect_uri": "https://musicandwellbeing2021.herokuapp.com/callback"
                #"redirect_uri": "http://localhost:8888/callback"
            }

            headers = {
                "Authorization": "Basic ... "
            }

            response_auth = requests.post(url, headers=headers, data=payload)
            data_exchange = json.loads(response_auth.text)

            if response_auth.status_code == 200:

                access_token_new = data_exchange["access_token"]
                refresh_token = data_exchange["refresh_token"]

                userEntry.access_token = access_token_new
                userEntry.refresh_token = refresh_token
                db.session.commit()

                print('Auth Code wurde ausgetauscht für user mit dem ID Code:' + Auth_ID_code)
                print('Acces Token:' + userEntry.access_token)
                print('Refresh Token:' + userEntry.refresh_token)
            else:
                #print('Fehler aufgetreten:' + response_auth.text)
                db.session.delete(userEntry)
                db.session.commit()

        time.sleep(30)

        userEntries_all = user.query.all()

        #second part:
        for userEntry in userEntries_all:
            url = "https://accounts.spotify.com/api/token"
            payload = {
                "grant_type": "refresh_token",
                "refresh_token": "{}".format(userEntry.refresh_token)
            }
            headers = {
                "Authorization": "Basic ... "
            }

            response_refresh = requests.post(url, headers=headers, data=payload)
            print('xxxxxxxxx REFRESH DONE xxxxxxxxx')
            data_refresh = json.loads(response_refresh.text)
            if response_refresh.status_code == 200:
                access_token_after_refresh = data_refresh["access_token"]
                userEntry.access_token = access_token_after_refresh
                db.session.commit()
            else:
                print('ERROR creating refresh_token')


#connection management
while 1:
    try:
        auth_refresh()
    except Exception as e:
        print('The error message: ' + str(e))
        time.sleep(30)

        #cant reconnect until invalid transaction is rolled back
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!! F E H L E R !!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!! F E H L E R !!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    finally:
        print('Finally here')
