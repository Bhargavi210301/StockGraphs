import requests
import schedule
import time
import json
import plotly.graph_objects as go

def get_stock_data(ticker, graph_type, period, interval):
    try:
        url = f"http://localhost:5000/stock_data?ticker={ticker}&graph_type={graph_type}&period={period}&interval={interval}"
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        print("Data received from backend:", data)  # Debug statement
        plot_graph(data, graph_type, period)
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")

def plot_graph(data, graph_type, period):
    dates = data['Date']
    layout = {
        'title': f"{data['Ticker']} {graph_type} Plot for {period}",
        'xaxis': {'title': 'Date'},
        'yaxis': {'title': 'Price'}
    }
    plot_data = []
    if graph_type == 'candlestick':
        plot_data = [go.Candlestick(
            x=dates,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            increasing_line_color='green',
            decreasing_line_color='red'
        )]
    elif graph_type == 'linegraph':
        plot_data = [go.Scatter(
            x=dates,
            y=data['Close'],
            mode='lines',
            line={'color': 'blue'}
        )]
    fig = go.Figure(data=plot_data, layout=layout)
    fig.show()

def fetch_and_plot():
    ticker = "MSFT"  # Example ticker
    graph_type = "candlestick"  # Example graph type
    period = "1mo"  # Example period
    interval = '1d' if graph_type == 'candlestick' and period in ['1mo', '3mo', '6mo', '1y', '5y'] else '1m'
    get_stock_data(ticker, graph_type, period, interval)

# Schedule the task to run every 30 seconds
schedule.every(30).seconds.do(fetch_and_plot)

print("Starting scheduled task...")

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
