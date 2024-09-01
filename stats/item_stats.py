from database import get_db

def get_track_chart_stats(track_id):
    # Connect to MongoDB
    db = get_db()
    collection = db["top_tracks"]
    pipeline = [
        # Match documents containing the specified track_id
        {"$match": {"tracks_data.track_id": track_id}},
        
        # Unwind the tracks_data array
        {"$unwind": "$tracks_data"},
        
        # Match the specific track_id again in the unwound array
        {"$match": {"tracks_data.track_id": track_id}},
        
        # Sort by timestamp in descending order
        {"$sort": {"timestamp": -1}},
        
        # Group by track_id and time_frame, aggregating statistics
        {
            "$group": {
                "_id": {
                    "track_id": "$tracks_data.track_id",
                    "time_frame": "$time_frame"
                },
                "max_position": {"$min": "$tracks_data.chart_position"},  
                "min_position": {"$max": "$tracks_data.chart_position"},
                "duration": {"$sum": 1},  # Count how many times the track appeared
                "latest_chart_position": {"$first": "$tracks_data.chart_position"}  # Latest chart position
            }
        },
        
        # Sort the results by time_frame (optional)
        {"$sort": {"_id.time_frame": 1}}
    ]
    
    # Run the aggregation pipeline
    results = collection.aggregate(pipeline)
    
    # Convert the results to a more readable format
    track_stats = []
    for result in results:
        track_stats.append({
            "time_frame": result["_id"]["time_frame"],
            "max_position": result["max_position"],
            "min_position": result["min_position"],
            "duration": result["duration"],
            "chart_position": result["latest_chart_position"]
        })
    
    return track_stats

def get_artist_chart_stats(artist_id):
    db  = get_db()
    collection = db["top_artists"]
    pipeline = [
        {"$match": {"artists_data.artist_id": artist_id}},

        {"$unwind": "$artists_data"},

        {"$match": {"artists_data.artist_id": artist_id}},

        {"$sort": {"timestamp": -1}},

        {
            "$group": {
                "_id": {
                    "artist_id": "$artists_data.artist_id",
                    "time_frame": "$time_frame"
                },
                "max_position": {"$min": "$artists_data.chart_position"},
                "min_position": {"$max": "$artists_data.chart_position"},
                "duration": {"$sum": 1},
                "latest_chart_position": {"$first": "$artists_data.chart_position"}
            }
        },

        {"$sort": {"_id.time_frame": 1}}
    ]
    results = list(collection.aggregate(pipeline))
    artist_stats = []
    for result in results:
        artist_stats.append({
            "time_frame": result["_id"]["time_frame"],
            "max_position": result["max_position"],
            "min_position": result["min_position"],
            "duration": result["duration"],
            "chart_position": result["latest_chart_position"]
        })

    return artist_stats
