from flask import Blueprint, render_template, request, redirect, url_for
from scripts.compare import compare_charts

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return render_template("home.html")

@main_bp.route("/search", methods=["POST"])
def search():
    chart_type = request.form.get("type")
    time_frame = request.form.get("range")
    days_ago = request.form.get("days")
    print(time_frame)
    return redirect(url_for('main.compare', chart_type=chart_type, time_frame=time_frame, days_ago=int(days_ago)))



@main_bp.route("/compare/<chart_type>/<time_frame>/<int:days_ago>")
def compare(chart_type, time_frame, days_ago):
    comparison_data = compare_charts(chart_type, time_frame, days_ago)
    return render_template("compare.html", comparison_data=comparison_data)

