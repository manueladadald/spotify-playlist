from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import data

date_to_scrape = input("Which date do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{date_to_scrape}"
year = date_to_scrape.split("-")[0]
response = requests.get(URL)
songs_list = response.text

soup = BeautifulSoup(songs_list, "html.parser")
song_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_spans]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=data.client_id,
        client_secret=data.client_secret,
        show_dialog=True,
        cache_path="token.txt"
    ))

user_id = sp.current_user()["id"]
search_years = f"{int(year)-1}-{year}"
song_uris = []
for song in song_names:
    result = sp.search(q=f"track:{song} year:{search_years}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

new_playlist = sp.user_playlist_create(user=user_id, name=f"{date_to_scrape} Top 100 Billboard", public=False)
print(new_playlist)

sp.playlist_add_items(playlist_id=new_playlist["id"], items=song_uris, position=None)
