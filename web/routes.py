from flask import Blueprint, render_template, send_file, request, redirect, url_for, abort
from scripts.compare import compare_charts
from database import fetch_chart_document, get_track_details, get_artist_details
from utils import fetch_artist_details
from stats import get_track_chart_stats, get_artist_chart_stats
from datetime import datetime, timedelta
from stats import plot_chart_position

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return render_template("home.html")

@main_bp.route("/top_tracks")
def top_tracks():
    short_term_chart = fetch_chart_document("tracks", "short_term")["tracks_data"]
    medium_term_chart = fetch_chart_document("tracks", "medium_term")["tracks_data"]
    long_term_chart = fetch_chart_document("tracks", "long_term")["tracks_data"]

    return render_template("top_chart.html", 
                           short_term_chart=short_term_chart, 
                           medium_term_chart=medium_term_chart, 
                           long_term_chart=long_term_chart,
                           chart_type = "tracks")

@main_bp.route("/top_artists")
def top_artists():
    short_term_chart = fetch_chart_document("artists", "short_term")["artists_data"]
    medium_term_chart = fetch_chart_document("artists", "medium_term")["artists_data"]
    long_term_chart = fetch_chart_document("artists", "long_term")["artists_data"]

    return render_template("top_chart.html",
                           short_term_chart=short_term_chart, 
                           medium_term_chart=medium_term_chart, 
                           long_term_chart=long_term_chart,
                           chart_type = "artists")

@main_bp.route("/compare_form", methods=["GET", "POST"])
def compare_form():
    if request.method == "POST":
        # Get form data from POST request
        chart_type = request.form.get("type")
        date_option = request.form.get("date_option")
        custom_date_str = request.form.get("custom_date", None)

        # Calculate the date2 based on the selected option
        if date_option == "yesterday":
            date2 = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        elif date_option == "week_ago":
            date2 = (datetime.now() - timedelta(weeks=1)).strftime("%Y-%m-%d")
        elif date_option == "month_ago":
            date2 = (datetime.now() - timedelta(weeks=4)).strftime("%Y-%m-%d")
        elif custom_date_str:
            date2 = custom_date_str
        else:
            date2 = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")  # Default to yesterday if no option is selected

        # Redirect to the compare page with the selected options
        return redirect(url_for('main.compare', chart_type=chart_type, date2=date2))

    # For GET requests, simply render the form
    return render_template("compare_form.html")

@main_bp.route("/compare/<chart_type>", methods=["GET"])
def compare(chart_type):
    # Get the date2 from the request arguments (default to yesterday if not provided)
    date2_str = request.args.get("date2", (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"))

    # Parse the date2
    date2 = datetime.strptime(date2_str, "%Y-%m-%d")
    date1 = datetime.now()  # Default to today's date

    # Fetch comparison data for different terms
    short_term_chart = compare_charts(chart_type, "short_term", date1, date2)
    medium_term_chart = compare_charts(chart_type, "medium_term", date1, date2)
    long_term_chart = compare_charts(chart_type, "long_term", date1, date2)

    # Render the comparison page
    return render_template(
        "compare.html",
        short_term_chart=short_term_chart,
        medium_term_chart=medium_term_chart,
        long_term_chart=long_term_chart,
        chart_type=chart_type,
        date1=date1.strftime("%Y-%m-%d"),
        date2=date2.strftime("%Y-%m-%d")
    )

@main_bp.route("/tracks/<track_id>")
def track(track_id):
    track_data = get_track_details(track_id)

    if track_data is None:
        abort(404)
    
    user_stats = get_track_chart_stats(track_id)

    graph_info = {
        "item_id": track_id,
        "chart_type": "tracks"
    }

    return render_template("card_display.html", track_data = track_data, stats = user_stats, page_type="track_card.html", title = track_data["title"], graph_info = graph_info)

@main_bp.route("/artists/<artist_id>")
def artist(artist_id):
    artist_data = get_artist_details(artist_id)
    # if artist is not in the db, call spotify api
    if artist_data is None:
        artist_data = fetch_artist_details(artist_id)
    # artist is not found by id
    if artist_data is None:
        abort(404)

    user_stats = get_artist_chart_stats(artist_id)

    graph_info = {
        "item_id": artist_id,
        "chart_type": "artists"
    }

    return render_template("card_display.html", artist_data = artist_data, stats=user_stats, page_type="artist_card.html", title=artist_data["name"], graph_info = graph_info)

@main_bp.route('/plot_graph/<chart_type>/<item_id>/<time_frame>')
def plot_graph(chart_type, item_id, time_frame):
    """
    Route to generate and serve a Plotly chart of track or artist positions over time.
    """
    plot_data = plot_chart_position(item_id, chart_type, time_frame)
    return plot_data
