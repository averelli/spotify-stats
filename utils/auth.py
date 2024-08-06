import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import config

def authenticate_spotify(scope: str) -> spotipy.client.Spotify:
    """
        Handles authentication based on the scope provided.
        Args:
            scope (str): Scope of the access
        Returns:
            sp(spotipy.client.Spotify): Spotify client
    """
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp