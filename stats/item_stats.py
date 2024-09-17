from database.operations import fetch_item_data

def get_item_stats(chart_type, item_id):
    """
    Get the chart statistics for either a track or an artist.

    Args:
        chart_type (str): Either "tracks" or "artists" to determine the type of chart
        item_id (str): The track_id or artist_id for which to fetch the stats

    Returns:
        list: A list of dictionaries containing the item stats
    """
    results = fetch_item_data(chart_type, item_id)
    
    chart_stats = []
    for result in results:
        chart_stats.append({
            "time_frame": result["_id"]["time_frame"],
            "max_position": result["max_position"],
            "min_position": result["min_position"],
            "duration": result["duration"],
            "chart_position": result["latest_chart_position"]
        })
    
    return chart_stats

# Wrapper functions 
def get_track_chart_stats(track_id):
    return get_item_stats("tracks", track_id)

def get_artist_chart_stats(artist_id):
    return get_item_stats("artists", artist_id)
