from flask import Blueprint, render_template
from scripts.compare import compare_charts

main_bp = Blueprint("main", __name__)
@main_bp.route("/compare/<chart_type>/<time_frame>/<int:days_ago>")
def compare(chart_type, time_frame, days_ago):
    comparison_data = compare_charts(chart_type, time_frame, days_ago)
    print(comparison_data)
    return render_template("compare.html", comparison_data=comparison_data)


@main_bp.route("/hello")
def hello():
    return render_template("hello.html")