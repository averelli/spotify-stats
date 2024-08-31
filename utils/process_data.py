from spotipy import Spotify
from utils import fetch_audio_features
from logs import logger

logger.name = "UTILS-PROCESS"

def process_top_tracks(sp: Spotify, top_tracks: dict) -> list:
    """
    Processes top tracks data to extract relevant information.

    Args:
        sp (spotipy.client.Spotify): Spotify client.
        top_tracks (dict): A dictionary of top tracks data returned from fetch_top_tracks()

    Returns:
        list: A list of dictionaries, each containing the processed track information.
    """
    processed_tracks = []
    
    try:
        for term, tracks in top_tracks.items():

            track_ids = [track["id"] for track in tracks["items"]]
            audio_features_list = fetch_audio_features(sp, track_ids)

            term_data = {
                "time_frame": term,
                "tracks_data": []
            }
            
            # track position in the chart, 1 is highest
            track_position = 1

            for track, audio_features in zip(tracks["items"], audio_features_list):
                track_info = {
                    "track_id": track["id"],
                    "title": track["name"],
                    "album_id": track["album"]["id"],
                    "album_name": track["album"]["name"],
                    "artist_id": track["artists"][0]["id"],
                    "artist_name": track["artists"][0]["name"],
                    "release_date": track["album"]["release_date"],
                    "cover_art_url": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
                    "duration_ms": track["duration_ms"],
                    "popularity": track["popularity"],
                    "uri": track["uri"],
                    "audio_features": {
                        "danceability": audio_features["danceability"],
                        "energy": audio_features["energy"],
                        "valence": audio_features["valence"],
                        "tempo": audio_features["tempo"]
                    },
                    "chart_position": track_position
                }
                term_data["tracks_data"].append(track_info)

                track_position += 1
            
            processed_tracks.append(term_data)
        
        logger.info("Top tracks processed successfully.")
    
    except Exception as e:
        logger.error(f"Error processing top tracks: {e}")
    
    return processed_tracks

def process_top_artists(top_artists: dict) -> list:
    """
    Processes top artists data to extract relevant information.

    Args:
        top_artists (dict): A dictionary of top artists data returned from fetch_top_artists()

    Returns:
        list: A list of dictionaries, each containing the processed artist information.
    """
    processed_artists = []
    
    try:
        for time_frame, artists in top_artists.items():
            time_frame_data = {
                "time_frame": time_frame,
                "artists_data": []
            }

            artist_position = 1
            
            # Process each artist in the time frame
            for artist in artists["items"]:
                artist_info = {
                    "artist_id": artist["id"],
                    "name": artist["name"],
                    "genres": artist["genres"],
                    "followers": artist["followers"]["total"],
                    "uri": artist["uri"],
                    "image_url": artist["images"][0]["url"] if artist["images"] else None,
                    "chart_position": artist_position
                }
                time_frame_data["artists_data"].append(artist_info)
                artist_position += 1
            
            processed_artists.append(time_frame_data)
            
            
        logger.info("Top artists processed successfully.")
    
    except Exception as e:
        logger.error(f"Error processing top artists: {e}")
    
    return processed_artists