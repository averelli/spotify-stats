from database import fetch_tracks_document
from logs import logger

logger.name = "COMPARE"

def compare_tracks(time_frame: str, days_ago: int):
    """
    Compares tracks between today and a specified number of days ago.

    Args:
        time_frame (str): The time frame to compare (e.g., 'short_term', 'medium_term', 'long_term').
        days_ago (int): The number of days ago to compare against (e.g., 1 for yesterday, 7 for a week ago).

    Returns:
        None: Prints the comparison result to the console.
    """

    try:
        # Fetch today's tracks and tracks from `days_ago`
        today_tracks_doc = fetch_tracks_document(time_frame)
        past_tracks_doc = fetch_tracks_document(time_frame, days_ago=days_ago)

        if not today_tracks_doc or not past_tracks_doc:
            logger.warning("Comparison cannot be performed due to missing data.")
            return
        
        today_tracks = {track['track_id']: track for track in today_tracks_doc['tracks_data']}
        past_tracks = {track['track_id']: track for track in past_tracks_doc['tracks_data']}

        # Analyze differences
        print(f"Comparison for {time_frame.replace('_', ' ').capitalize()} ({days_ago} days ago):")
        for i, track in enumerate(today_tracks_doc['tracks_data']):
            track_id = track['track_id']
            track_title = track['title']
            artist_name = track['artist_name']

            if track_id in past_tracks:
                change_in_position = past_tracks[track_id]['chart_position'] - track['chart_position']
                change_text = f"({change_in_position:+d})" if change_in_position != 0 else "(=)"
            else:
                change_text = "(new)"

            print(f"{i+1}. {change_text} {track_title} by {artist_name}")

    except Exception as e:
        logger.error(f"Error comparing tracks: {e}")

compare_tracks("short_term", 2)
