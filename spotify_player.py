import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

# Initialize sp as None. It will be configured later.
sp = None

def initialize_spotify():
    """
    Initializes the Spotipy client. 
    This must be called after loading environment variables.
    """
    global sp
    try:
        auth_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(auth_manager=auth_manager)
    except spotipy.exceptions.SpotifyOauthError as e:
        print(f"Error initializing Spotify. Make sure your .env file is correct. Details: {e}")
        sp = None


def get_playlist(mood):
    """
    Searches for a Spotify playlist based on the mood and returns
    an embeddable URL for the first result.
    """
    if not sp:
        print("Spotify client is not initialized. Cannot get playlist.")
        return None

    # UPDATED: The keys now exactly match the labels from the dima806 model.
    # e.g., 'fearful' instead of 'fear', 'disgusted' instead of 'disgust'.
    search_queries = {
        'happy': 'happy vibes',
        'sad': 'sad songs',
        'angry': 'angry metal',
        'fearful': 'calming instrumental',
        'surprised': 'upbeat party',
        'neutral': 'lo-fi beats',
        'disgusted': 'alternative rock'
    }

    # .lower() makes our mapping case-insensitive, which is good practice.
    query = search_queries.get(mood.lower(), 'lo-fi beats') # Default to lo-fi

    try:
        results = sp.search(q=query, type='playlist', limit=1)
        if results and results['playlists']['items']:
            playlist_uri = results['playlists']['items'][0]['uri']
            # Convert URI to embeddable URL format
            embed_url = playlist_uri.replace("spotify:playlist:", "https://open.spotify.com/embed/playlist/")
            return embed_url
        return None

    except spotipy.exceptions.SpotifyException as e:
        print(f"Error searching for playlist on Spotify: {e}")
        return None