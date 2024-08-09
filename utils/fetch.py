from spotipy import Spotify
from logs import logger

logger.name = "UTILS-FETCH"

def fetch_top_tracks(sp: Spotify, limit:int = 10) -> dict:
    """
        Fetches top tracks. By default top 10.
        Args:
            sp (spotipy.client.Spotify): Spotify client
            limit (int): How many top tracks to fetch
        Returns:
            A dictionary of top tracks
    """
    try:
        top_tracks = {
            "short_term": sp.current_user_top_tracks(limit=limit, time_range="short_term"),
            "medium_term": sp.current_user_top_tracks(limit=limit, time_range="medium_term"),
            "long_term": sp.current_user_top_tracks(limit=limit, time_range="long_term")
        }
        logger.info("Top tracks fetched successfully.")
        return top_tracks
    
    except Exception as e:
        logger.error(f"Error fetching top tracks: {e}")
        return {}

def fetch_top_artists(sp: Spotify, limit: int = 10) -> dict:
    """
    Fetches top artists. By default top 10.

    Args:
        sp (spotipy.client.Spotify): Spotify client
        limit (int): How many top artists to fetch

    Returns:
        dict: A dictionary of top artists for different time ranges.
    """
    try:
        top_artists = {
            "short_term": sp.current_user_top_artists(limit=limit, time_range="short_term"),
            "medium_term": sp.current_user_top_artists(limit=limit, time_range="medium_term"),
            "long_term": sp.current_user_top_artists(limit=limit, time_range="long_term")
        }
        logger.info("Top artists fetched successfully.")
        return top_artists
    except Exception as e:
        logger.error(f"Error fetching top artists: {e}")
        return {}
    
def fetch_audio_features(sp: Spotify, track_ids: list) -> list:
    """
    Fetches audio features for a list of track IDs.

    Args:
        sp (spotipy.client.Spotify): Spotify client
        track_ids (list): A list of track IDs

    Returns:
        list: A list of dictionaries containing audio features for each track.
    """
    try:
        audio_features = sp.audio_features(track_ids)
        logger.info("Audio features fetched successfully.")
        return audio_features
    except Exception as e:
        logger.error(f"Error fetching audio features: {e}")
        return []