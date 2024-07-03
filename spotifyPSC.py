'''

Burak TÜZEL - 191805057

Talha Alper ASAV - 201805072

'''

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
import math
import time
from requests.exceptions import ReadTimeout

# Set up credentials
client_id = '3851cad810c64531b5a0afae3d22b3f9'
client_secret = 'e881bd74c38f41c78ab16e957d29f3ce'

# Authenticate with Spotify API
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Define the base keyword and additional terms
base_keyword = 'Türkçe'
additional_terms = ['Pop', 'Hareketli', 'Rock', 'Slow', 'Akustik', 'Klasik', 'Rap', 'Jazz', 'Efsane', 'En İyi']

# Generate similar keywords by combining the base keyword with additional terms
similar_keywords = [f"{base_keyword} {term}" for term in additional_terms]

# Total number of playlists to scrape
total_playlists = 1000

# Calculate the number of playlists to scrape for each keyword
num_keywords = len(similar_keywords)
playlists_per_keyword = math.ceil(total_playlists / num_keywords)

# Define a function to scrape playlists for a given keyword
def scrape_playlists(keyword, num_playlists):
    offset = 0
    playlists_scraped = 0
    playlist_data = []

    print(f"Scraping playlists for keyword '{keyword}'...")

    while playlists_scraped < num_playlists:
        try:
            playlists = sp.search(q=keyword, type='playlist', limit=50, offset=offset)
        except spotipy.SpotifyException as e:
            print("Error during search:", e)
            playlists = None

        if not playlists or len(playlists['playlists']['items']) == 0:
            print(f"No more playlists found for keyword '{keyword}'.")
            break

        for playlist in playlists['playlists']['items']:
            playlist_id = playlist['id']
            try:
                # Retry the request if a timeout occurs
                attempts = 0
                while attempts < 3:
                    try:
                        results = sp.playlist_tracks(playlist_id)
                        break
                    except ReadTimeout:
                        print("Timeout occurred. Retrying...")
                        attempts += 1
                        time.sleep(1)  # Wait for a short duration before retrying
                else:
                    print("Max retries reached. Skipping playlist.")
                    continue

                tracks = results.get('items', [])
                # Define a list to store tracks in the current playlist
                playlist_tracks = []
                # Iterate over tracks in the playlist
                for track in tracks:
                    # Check if track information is available
                    if track and track.get('track'):
                        track_name = track['track'].get('name')
                        if track_name:
                            playlist_tracks.append(track_name)
                # Append playlist tracks to the playlist_data list
                playlist_data.append({'tracks': playlist_tracks})
                playlists_scraped += 1

                print(f"\rProgress for '{keyword}': {playlists_scraped}/{num_playlists}", end='', flush=True)

                if playlists_scraped >= num_playlists:
                    break
            except Exception as ex:
                print(f"Error occurred while processing playlist: {ex}")

        offset += 50

    print()  # Print a new line after completion
    return playlist_data

# Scrape playlists for each keyword
all_playlist_data = []
remaining_playlists = total_playlists
for keyword in similar_keywords:
    num_playlists = min(remaining_playlists, playlists_per_keyword)
    playlist_data = scrape_playlists(keyword, num_playlists)
    all_playlist_data.extend(playlist_data)
    remaining_playlists -= num_playlists
    if remaining_playlists <= 0:
        break  # Stop scraping if the total number of playlists is reached

# Write all playlist data to CSV
csv_file = "scrapedSongs.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)

    # Write playlist data
    for playlist in all_playlist_data:
        writer.writerow(playlist['tracks'])