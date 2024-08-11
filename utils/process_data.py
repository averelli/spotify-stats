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

            track_ids = [track['id'] for track in tracks['items']]
            audio_features_list = fetch_audio_features(sp, track_ids)

            term_data = {
                "time_frame": term,
                "tracks_data": []
            }
            
            # track position in the chart, 1 is highest
            track_position = 1

            for track, audio_features in zip(tracks['items'], audio_features_list):
                track_info = {
                    "track_id": track['id'],
                    "title": track['name'],
                    "album_id": track['album']['id'],
                    "album_name": track['album']['name'],
                    "artist_id": track['artists'][0]['id'],
                    "artist_name": track['artists'][0]['name'],
                    "release_date": track['album']['release_date'],
                    "cover_art_url": track['album']['images'][0]['url'] if track['album']['images'] else None,
                    "duration_ms": track['duration_ms'],
                    "popularity": track['popularity'],
                    "uri": track['uri'],
                    "audio_features": {
                        "danceability": audio_features['danceability'],
                        "energy": audio_features['energy'],
                        "valence": audio_features['valence'],
                        "tempo": audio_features['tempo']
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

