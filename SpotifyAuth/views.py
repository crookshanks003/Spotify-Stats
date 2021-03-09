from Spotify.settings import CLIENT_SECRET,REDIRECT_URI,CLIENT_ID
from django.shortcuts import render,redirect
from django.conf import settings
from django.http import HttpResponse
from .SpotifyAPI import SpotifyAPI
import datetime
from .forms import Dropdown
import json



client_id = CLIENT_ID
client_secret = CLIENT_SECRET
redirect_uri = REDIRECT_URI 
spotify = SpotifyAPI(client_id,client_secret,redirect_uri)

def refresh_session(request):
    if datetime.datetime.now() > datetime.datetime.strptime(request.session.get('expires_in'),'%Y-%m-%d %H:%M:%S.%f'):
        data = spotify.get_refreshed_token(request.session.get('refresh_token'))
        request.session['access_token'] = data.get('access_token')
        request.session['expires_in'] = str(datetime.datetime.now() + datetime.timedelta(seconds=3600))

def log_in(request):
    if not request.session.exists(request.COOKIES.get('sessionid')):
        request.session.create()
        url = spotify.get_access_url()
        return render(request, 'login.html', {'site': url})
    elif not request.session.get('access_token'):
        url = spotify.get_access_url()
        print(request.session.get('access_token'))
        return render(request, 'login.html', {'site': url})
    else:
        return redirect('home')

def callback(request):
    code = request.GET.get('code')
    error = request.GET.get('error')
    if error: return redirect('login')
    data = spotify.get_access_data(code)
    request.session['access_token'] = data.get('access_token')
    request.session['refresh_token'] = data.get('refresh_token')
    request.session['expires_in'] = str(datetime.datetime.now() + datetime.timedelta(seconds=3600))    
    print(request.session.get('expires_in'))
    return redirect('home')


def home(request):
    if request.session.get('access_token') == None:
        return redirect('login')
    refresh_session(request)
    token = request.session.get('access_token')
    user = spotify.get_user(token)
    if user.get('error'):
        print(user.get('error'))
        return redirect('login')
    top_artist = spotify.get_top_artist(token, time_range='long_term', limit=3).get('items')
    top_track = spotify.get_top_tracks(token, time_range='long_term', limit=3) .get('items')
    return render(request, 'home.html', {'user':user,'tracks':top_track,'artists':top_artist})


def log_out(request):
    request.session.delete()
    return redirect('login')


def artist(request):
    if request.session.get('access_token') == None:
        return redirect('login')
    refresh_session(request)
    token = request.session.get('access_token')
    time_range = request.GET.get('time_range')
    data = spotify.get_top_artist(token,time_range=time_range,limit=15).get('items')
    return render(request, 'artist.html',{'artists':data,'form': Dropdown(request.GET)})


def tracks(request):
    if request.session.get('access_token') == None:
        return redirect('login')
    refresh_session(request)
    token = request.session.get('access_token')
    time_range = request.GET.get('time_range')
    data = spotify.get_top_tracks(token,time_range=time_range,limit=50).get('items')
    track_ids = ','.join(track.get('id') for track in data)
    liked = spotify.check_saved_song(track_ids, token)
    return render(request, 'track.html',{'tracks':zip(data,liked),'form': Dropdown(request.GET)})


def recent(request):
    if request.session.get('access_token') == None:
        return redirect('login')
    refresh_session(request)
    token = request.session.get('access_token')
    data = spotify.get_recent(token).get('items')
    return render(request, 'recent.html',{'tracks':data,'form':Dropdown(request.GET)})