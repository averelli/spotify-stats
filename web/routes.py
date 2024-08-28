from flask import Blueprint, render_template, request, redirect, url_for, abort
from scripts.compare import compare_charts
from database import fetch_chart_document, get_track_details, get_artist_details
from utils import fetch_artist_details

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return render_template("home.html")

@main_bp.route("/compare_form")
def compare_form():
    return render_template("compare-form.html")

@main_bp.route("/compare_charts", methods=["POST"])
def search():
    chart_type = request.form.get("type")
    time_frame = request.form.get("range")
    days_ago = request.form.get("days")

    return redirect(url_for("main.compare", chart_type=chart_type, time_frame=time_frame, days_ago=int(days_ago)))

@main_bp.route("/top_tracks")
def top_tracks():
    short_term_chart = fetch_chart_document("tracks", "short_term")["tracks_data"]
    medium_term_chart = fetch_chart_document("tracks", "medium_term")["tracks_data"]
    long_term_chart = fetch_chart_document("tracks", "long_term")["tracks_data"]

    return render_template("top_tracks.html", 
                           short_term_chart=short_term_chart, 
                           medium_term_chart=medium_term_chart, 
                           long_term_chart=long_term_chart,
                           chart_type = "tracks")

@main_bp.route("/compare/<chart_type>/<time_frame>/<int:days_ago>")
def compare(chart_type, time_frame, days_ago):
    comparison_data = compare_charts(chart_type, time_frame, days_ago)

    return render_template("compare.html", 
                           title=f"Comparison for {chart_type.capitalize()} - {time_frame.replace('_', ' ').capitalize()} ({days_ago} days ago):",
                           chart=comparison_data["chart"],
                           chart_type = "tracks")

@main_bp.route("/tracks/<track_id>")
def track(track_id):
    track_data = get_track_details(track_id)
    if track_data is None:
        abort(404)

    return render_template("track_page.html", track_data = track_data)

@main_bp.route("/artists/<artist_id>")
def artist(artist_id):
    artist_data = get_artist_details(artist_id)
    # if artist is not in the db, call spotify api
    if artist_data is None:
        artist_data = fetch_artist_details(artist_id)
    # artist is not found by id
    if artist_data is None:
        abort(404)

    return render_template("artist_page.html", artist_data = artist_data)
