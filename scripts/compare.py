from database import fetch_chart_document
from logs import logger

def compare_charts(chart_type: str, time_frame: str, days_ago: int) -> dict:
    """
    Compares charts (tracks or artists) between today and a specified number of days ago.

    Args:
        chart_type (str): The type of chart to compare ("tracks" or "artists").
        time_frame (str): The time frame to compare (e.g., "short_term", "medium_term", "long_term").
        days_ago (int): The number of days ago to compare against (e.g., 1 for yesterday, 7 for a week ago).

    Returns:
        Dict: Dictionary with chart data.
    """

    try:
        # Fetch today"s chart and chart from `days_ago`
        today_chart_doc = fetch_chart_document(chart_type, time_frame)
        past_chart_doc = fetch_chart_document(chart_type, time_frame, days_ago=days_ago)

        if not today_chart_doc or not past_chart_doc:
            logger.warning("Comparison cannot be performed due to missing data.")
            return

        # Create a dictionariy for the past chart with IDs as keys
        past_chart = {item[f"{chart_type[:-1]}_id"]: item for item in past_chart_doc[f"{chart_type}_data"]}

        comparison_items = []

        # Analyze differences
        for i, item in enumerate(today_chart_doc[f"{chart_type}_data"]):
            print(item)
            item_id = item[f"{chart_type[:-1]}_id"]

            if item_id in past_chart:
                change_in_position = past_chart[item_id]["chart_position"] - item["chart_position"]
                change_text = f"({change_in_position:+d})" if change_in_position != 0 else "(=)"
            else:
                change_text = "(new)"

            comparison_items.append({
                "chart_position": i+1,
                "title": item.get("title", ""),
                "name": item.get("name", ""),
                "artist_name": item.get("artist_name", ""),
                "change": change_text,
                "cover_art_url": item.get("cover_art_url", ""),
                "image_url": item.get("image_url", ""),
                "track_id": item.get("track_id", ""),
                "artist_id": item.get("artist_id", ""),
            })

        return {
            "title": f"Comparison for {chart_type.capitalize()} - {time_frame.replace('_', ' ').capitalize()} ({days_ago} days ago):",
            "chart": comparison_items
        }

    except Exception as e:
        logger.error(f"Error comparing {chart_type}: {e}")
        return {"title": "Error occurred", "items": []}
    
