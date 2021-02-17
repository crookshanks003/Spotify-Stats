import requests,datetime,base64,json

class SpotifyAPI():
    client_id = None
    redirect_uri=""
    client_secret = None

    def __init__(self,client_id,client_secret,redirect_uri=""):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def get_access_url(self):
        param = {
            'client_id': self.client_id,
            'response_type':'code',
            'redirect_uri': self.redirect_uri,
            'scope': 'user-top-read user-read-private user-read-recently-played user-library-read playlist-modify-private',
            'show_dialog': 'true'
        }
        url = 'https://accounts.spotify.com/authorize'
        access_url = requests.Request('GET',url, params=param).prepare().url
        return access_url
    
    def get_access_data(self,code):
        client_cred_64 = base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode())
        token_url = 'https://accounts.spotify.com/api/token'
        token_data = {'grant_type': 'authorization_code','code':code, 'redirect_uri':self.redirect_uri}
        token_header = {'Authorization': f'Basic {client_cred_64.decode()}'}
        r = requests.post(token_url, data=token_data, headers=token_header).json()
        return r

    def get_user(self,token):
        url = 'https://api.spotify.com/v1/me'
        header = {'Authorization': f'Bearer {token}'}
        r = requests.get(url, headers=header)
        return r.json()
    
    def get_refreshed_token(self,code):
        client_cred_64 = base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode())
        token_url = 'https://accounts.spotify.com/api/token'
        token_data = {'grant_type': 'refresh_token','refresh_token':code, 'redirect_uri':self.redirect_uri}
        token_header = {'Authorization': f'Basic {client_cred_64.decode()}'}
        r = requests.post(token_url, data=token_data, headers=token_header).json()
        return r

    def get_top_artist(self,token,time_range,limit):
        url = 'https://api.spotify.com/v1/me/top/artists'
        header = {'Authorization': f'Bearer {token}'}
        param = {'time_range': time_range,'limit':limit}
        r = requests.get(url, headers=header, params=param)
        return r.json()

    def get_top_tracks(self,token,time_range,limit):
        url = 'https://api.spotify.com/v1/me/top/tracks'
        header = {'Authorization': f'Bearer {token}'}
        param = {'time_range': time_range,'limit':limit}
        r = requests.get(url, headers=header, params=param)
        return r.json()

    def get_recent(self,token):
        url = 'https://api.spotify.com/v1/me/player/recently-played'
        header = {'Authorization': f'Bearer {token}'}
        param = {'limit':30}
        r = requests.get(url, headers=header, params=param)
        return r.json()

    def check_saved_song(self,ids,token):
        url = 'https://api.spotify.com/v1/me/tracks/contains'
        header = {'Authorization': f'Bearer {token}'}
        param = {'ids':ids}
        r = requests.get(url, headers=header, params=param)
        return r.json()

    def create_playlist(self,token,user_id):
        url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
        header = {'Authorization': f'Bearer {token}'}
        data = {
            "name": f"Top Tracks ({datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')})",
            "description": "Your top tracks from Spotify Stats",
            "public": False
        }
        r = requests.post(url, headers=header, data=json.dumps(data))
        return r.json().get('id')