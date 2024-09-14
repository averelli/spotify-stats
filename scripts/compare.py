from database.operations import fetch_chart_document
from logs import logger
from datetime import datetime, timedelta

def compare_charts(chart_type: str, time_frame: str, date1: datetime = None, date2: datetime = None) -> dict:
    """
    Compares charts (tracks or artists) between two specified dates.
    If no document is found for the exact dates, it will find the closest available one.

    Args:
        chart_type (str): The type of chart to compare ("tracks" or "artists").
        time_frame (str): The time frame to compare (e.g., "short_term", "medium_term", "long_term").
        date1 (datetime): The first date to compare (defaults to today).
        date2 (datetime): The second date to compare (defaults to yesterday).

    Returns:
        dict: Dictionary with chart comparison data.
    """
    try:
        # Default to today's date if date1 is not provided
        if date1 is None:
            date1 = datetime.today()
        # Default to yesterday if date2 is not provided
        if date2 is None:
            date2 = datetime.today() - timedelta(days=1)

        # Fetch the chart data for both dates
        today_chart_doc = fetch_chart_document(chart_type, time_frame, date1)
        past_chart_doc = fetch_chart_document(chart_type, time_frame, date2)

        if not today_chart_doc or not past_chart_doc:
            logger.warning("Comparison cannot be performed due to missing data.")
            return {"title": "Data Missing", "chart": []}

        # Create a dictionary for the past chart with IDs as keys
        past_chart = {item[f"{chart_type[:-1]}_id"]: item for item in past_chart_doc[f"{chart_type}_data"]}

        comparison_items = []

        # Analyze differences between today's chart and the past chart
        for i, item in enumerate(today_chart_doc[f"{chart_type}_data"]):
            item_id = item[f"{chart_type[:-1]}_id"]

            if item_id in past_chart:
                change_in_position = past_chart[item_id]["chart_position"] - item["chart_position"]
                change_text = f"({change_in_position:+d})" if change_in_position != 0 else "(=)"
            else:
                change_text = "(new)"

            comparison_items.append({
                "chart_position": i + 1,
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
            "title": f"{time_frame.replace('_', ' ').capitalize()} comparison \n"
                     f"({today_chart_doc['timestamp'].strftime('%Y-%m-%d')} vs {past_chart_doc['timestamp'].strftime('%Y-%m-%d')})",
            "chart": comparison_items
        }

    except Exception as e:
        logger.error(f"Error comparing {chart_type}: {e}")
        return {"title": "Error occurred", "items": []}
