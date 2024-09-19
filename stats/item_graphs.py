import plotly
import plotly.graph_objs as go
import json
from database import fetch_item_positions

def filter_data(dates: list, positions: list):
    if not dates or not positions or len(dates) != len(positions):
        raise ValueError("Dates and positions must be non-empty and of the same length.")

    filtered_dates = [dates[0]]  # Always include the first element
    filtered_positions = [positions[0]]

    for i in range(1, len(dates) - 1):
        if positions[i] != positions[i - 1] or positions[i] != positions[i + 1]:
            filtered_dates.append(dates[i])
            filtered_positions.append(positions[i])

    if len(dates) > 1:
        # Always include the last element if there are more than 1 element
        filtered_dates.append(dates[-1])
        filtered_positions.append(positions[-1])

    return filtered_dates, filtered_positions


def plot_chart_position(item_id, chart_type, time_frame):
    dates, positions = fetch_item_positions(chart_type, item_id, time_frame)
    dates, positions = filter_data(dates, positions)
    

    # Create a Plotly graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=positions,
        mode='lines+markers',
        name='Chart Position',
        line=dict(color='#E74C3C'),
        marker=dict(size=8)
    ))

    # Customize the layout
    fig.update_layout(
        title=f'Position of {chart_type.capitalize()} "{item_id}" Over Time ({time_frame.capitalize()})',
        xaxis_title='Date',
        yaxis_title='Chart Position',
        yaxis=dict(
            autorange=False,  # Correctly invert Y-axis (1 at the top, 50 at the bottom)
            range=[51, 0],  # Ensure range stays between 1 and 50
            fixedrange=True,  # Disable zooming on Y-axis
            tickvals=[1] + list(range(10, 51, 10)),
            zeroline = False
        ),
        xaxis=dict(
            fixedrange=True,
            zeroline = False),  # Disable zooming on X-axis
        template='none',
        hovermode='closest',
        plot_bgcolor='#f9f9f9',
        paper_bgcolor='#f9f9f9',
        font=dict(color='#333')
    )

    # Return the figure as JSON
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)