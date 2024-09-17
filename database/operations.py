from datetime import datetime
from database import get_db
from logs import logger
from datetime import datetime
from pymongo import DESCENDING

def save_top_tracks(data: dict):
    """
    Saves the top tracks to the database with the specified time period.

    Args:
        data (dict): The top tracks data to save.
    """

    try:
        db = get_db()
        collection = db["top_tracks"]
        document = {
            "timestamp": datetime.now(),
            "time_frame": data["time_frame"],
            "tracks_data": data["tracks_data"]
        }
        collection.insert_one(document)
        logger.info("Top tracks saved successfully.")
    except Exception as e:
        logger.error(f"Error saving top tracks: {e}")

def save_top_artists(data: dict):
    """
    Saves the top artists to the database with the specified time period.

    Args:
        data (dict): The top artists data to save.
    """
    try:
        db = get_db()
        collection = db["top_artists"]
        document = {
            "timestamp": datetime.now(),
            "time_frame": data["time_frame"],
            "artists_data": data["artists_data"]
        }
        collection.insert_one(document)
        logger.info("Top artists saved successfully.")
    except Exception as e:
        logger.error(f"Error saving top artists: {e}")

def fetch_chart_document(chart_type: str, time_frame: str, date: datetime = None) -> dict:
    """
    Fetches the chart document for a specific time frame and date.
    If no exact document is found for the given date, fetches the closest one before that date.

    Args:
        chart_type (str): Which chart document to fetch ('tracks' or 'artists').
        time_frame (str): The time frame (e.g., 'short_term', 'medium_term', 'long_term').
        date (datetime): The date for which to fetch the data (in "YYYY-MM-DD" format). 
                         If None, fetches the latest available data.

    Returns:
        dict: The document containing chart data from the specified date or closest available date.
    """
    try:
        db = get_db()
        collection = db[f"top_{chart_type}"]

        if date is None:
            # If no date is provided, fetch the latest document
            document = list(collection.find({"time_frame": time_frame}).sort("timestamp", -1).limit(1))[0]
        else:
            # Parse the provided date and look for the closest document before the specified date
            target_date_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
            target_date_end = date.replace(hour=23, minute=59, second=59, microsecond=999999)

            # First try to find the exact match for the given date
            document = collection.find_one({
                "time_frame": time_frame,
                "timestamp": {"$gte": target_date_start, "$lt": target_date_end}
            })

            # If no document is found, get the closest one before the date
            if not document:
                document = list(collection.find({
                    "time_frame": time_frame,
                    "timestamp": {"$lt": target_date_start}
                }).sort("timestamp", DESCENDING).limit(1))

                if document:
                    document = document[0]

        if document:
            return document
        else:
            logger.error(f"No data found for date {date} or earlier in {time_frame}.")
            return None

    except Exception as e:
        logger.error(f"Error fetching chart data for time frame {time_frame} on {date}: {e}")
        return None

def get_track_details(track_id):
    """
    Retrieves the details of a specific track from the top_tracks collection.
    Args:
        track_id (str): The unique identifier for the track.
    Returns:
        dict: A dictionary containing the track details (title, artist, album, etc.)
              if the track is found. If no track is found, returns None.
    """
    db = get_db()
    # Find the first document where the track is present
    track_doc = db.top_tracks.find_one({"tracks_data.track_id": track_id}, {"tracks_data.$": 1})
    if track_doc and "tracks_data" in track_doc:
        return track_doc["tracks_data"][0]  # Return the first matching track
    return None

def get_artist_details(artist_id):
    """
    Retrieves the details of a specific artist from the top_tracks collection.
    Args:
        artist_id (str): The unique identifier for the artist.
    Returns:
        dict: A dictionary containing the artist details (artist name, tracks, etc.)
              if the artist is found. If no artist is found, returns None.
    """
    db = get_db()
    artist_result = db.top_artists.aggregate([
        {"$unwind": "$artists_data"},
        {"$match": {"artists_data.artist_id": artist_id}},
        {"$sort": {"timestamp": -1}},
        {"$limit": 1},
        {"$project": {
            "_id": 0,
            "artists_data": 1
        }}
    ])
    artist_doc = next(artist_result, None)
    if artist_doc:
        return artist_doc["artists_data"]  # Return the first matching artist data
    return None

def fetch_item_data(chart_type, item_id):
    """
    Fetches chart data for either tracks or artists, depending on the chart_type parameter.
    
    Args:
        chart_type (str): Either "tracks" or "artists" to determine which collection to query.
        item_id (str): The track_id or artist_id to filter the data.
    
    Returns:
        Cursor: The MongoDB cursor with the aggregated data.
    """

    db = get_db()
    collection = db[f"top_{chart_type}"]

    item_field = f"{chart_type}_data.{chart_type[:-1]}_id"  # 'tracks_data.track_id' or 'artists_data.artist_id'

    pipeline = [
        {"$match": {item_field: item_id}},  # Match documents containing the item_id
        {"$unwind": f"${chart_type}_data"},  # Unwind the tracks_data or artists_data array
        {"$match": {item_field: item_id}},  # Match the specific item_id again in the unwound array
        {"$sort": {"timestamp": -1}},  # Sort by timestamp in descending order
        {
            "$group": {
                "_id": {
                    f"{chart_type[:-1]}_id": f"${chart_type}_data.{chart_type[:-1]}_id",
                    "time_frame": "$time_frame"
                },
                "max_position": {"$min": f"${chart_type}_data.chart_position"},
                "min_position": {"$max": f"${chart_type}_data.chart_position"},
                "duration": {"$sum": 1},
                "latest_chart_position": {"$first": f"${chart_type}_data.chart_position"}
            }
        },
        {"$sort": {"_id.time_frame": 1}}  # Sort results by time_frame
    ]
    
    return collection.aggregate(pipeline)
