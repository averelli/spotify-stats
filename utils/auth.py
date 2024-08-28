import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

sp = None

def authenticate_spotify(scope: str) -> spotipy.client.Spotify:
    """
        Handles authentication based on the scope provided.
        Args:
            scope (str): Scope of the access
        Returns:
            sp(spotipy.client.Spotify): Spotify client
    """
    global sp
    if sp is None:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                    client_secret=CLIENT_SECRET,
                                                    redirect_uri=REDIRECT_URI,
                                                    scope=scope,
                                                    cache_path="config/.cache"))
    return sp