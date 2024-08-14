import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from openai import OpenAI
recongnizer = sr.Recognizer()
ttsx = pyttsx3.init()
newsapi = "__YOUT_API__"

#spotify api

SPOTIPY_CLIENT_ID = '__YOUR_API__'
SPOTIPY_CLIENT_SECRET = '__YOUT__API__'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="user-library-read user-read-playback-state user-modify-playback-state"))


def speak(text):
    ttsx.say(text)
    ttsx.runAndWait()


def ai_process(command):
    client = OpenAI(api_key="__YOUR_API__",
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named helium skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content


def play_track(track_name):
    results = sp.search(q = track_name, type= 'track', limit = 1)
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        sp.start_playback(uris= [track_uri])
        speak(f'playing {track_name} on spotify')
    else:
        speak('sorry, i couldnt find the track on spotify')
def pause_playback():
    sp.pause_playback()
    speak('music paused ')


def processcommand(c):
    if 'open google' in c.lower():
        webbrowser.open('https://google.com')
    elif 'open youtube' in c.lower():
        webbrowser.open('https://youtube.com')
    elif 'open linkdin' in c.lower():
        webbrowser.open('https://linkedin.com')
    elif 'open reddit' in c.lower():
        webbrowser.open('https://reddit.com')
    elif "news" in c.lower():
        r = requests.get("https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=a9054c16659c4df68424c4666740b26d")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for articles in articles:
                speak(articles['title'])


    elif 'play' in c.lower():
        track_name = c.lower().replace('play', "").strip()
        play_track(track_name)
    elif 'pause' in c.lower():
        pause_playback()

    else:
        output = ai_process(c)
        speak(output) 

if __name__ == '__main__':
    speak('initializing Helium...')
    while True:
        print('Recognizing')
        try:
            with sr.Microphone() as source:
                print('Say Something')
                audio =  recongnizer.listen(source,timeout=3, phrase_time_limit= 4)
            word = recongnizer.recognize_google(audio)

            if(word.lower() == 'helium'):
                speak('Hello Sir')

                with sr.Microphone() as source:
                    audio = recongnizer.listen(source, timeout= 3, phrase_time_limit= 4)
                    cmd = recongnizer.recognize_google(audio)

                    processcommand(cmd)

            elif(word.lower() == 'stop'):
                break

            print('Helium thinks you said ' + recongnizer.recognize_google(audio))
            
        except:
            print('Helium faild to understand ur words')