from flask import Flask, render_template, jsonify, request
import yfinance as yf
import os
from dotenv import load_dotenv,dotenv_values

app = Flask(__name__)

load_dotenv()

@app.route('/')
def home():
    ticker_options = {}
    env_vars = dotenv_values(".env")
    # print("Data of .env file:", env_vars)
    for key, value in env_vars.items():
        if key.isupper():
            ticker_options[key] = value
    # print("Ticker Options:", ticker_options)
    return render_template("index.html", ticker_options=ticker_options)

@app.route('/stock_data')
def stock_data():
    ticker = request.args.get('ticker')
    graph_type = request.args.get('graph_type')
    period = request.args.get('period')
    interval = request.args.get('interval', '1m')  # Default interval is 1 minute

    stock = yf.Ticker(ticker)
    
    data = None
    if graph_type == 'candlestick':
        data = stock.history(period=period,interval=interval)
    elif graph_type == 'linegraph':
        data = stock.history(period=period)['Close']
    
    # Prepare data for response
    if data is not None:
        data = data.reset_index().to_dict(orient='list')
        data['Ticker'] = ticker  # Add ticker to the response

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
