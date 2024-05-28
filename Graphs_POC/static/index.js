    // DOMContentLoaded :- script runs after html page is loaded
    // Submit :- on submit event on form

    document.addEventListener('DOMContentLoaded', function() {
        document.getElementById('stockForm').addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent default form submission
            getStockData();
            setInterval(getStockData, 30000); // Fetch data every 30 seconds
        });
        async function getStockData() {
            var ticker = document.getElementById("tickerSelect").value;
            var graphType = document.getElementById("graphTypeSelect").value;
            var period = document.getElementById("periodSelect").value; 

            console.log("Fetching data for ticker:", ticker, "and graph type:", graphType);  // Debug statement
            
            let interval = '1m'; // Default interval

            // Adjust the period if necessary
            if (graphType === 'candlestick' && (period === '1mo' ||period === '3mo' ||period === '6mo' ||period === '1y' ||period === '5y')) {
                interval = '1d'; // Change to 7 days if the period is 1 month for candlestick

                console.log("Period adjusted to 7d for candlestick graph type.");
            }
            try {
                const response = await fetch(`/stock_data?ticker=${ticker}&graph_type=${graphType}&period=${period}&interval=${interval}`);
                const data = await response.json();
                console.log("Data received from backend:", data);  // Debug statement
                plotGraph(data, graphType, period); // Calling function plotGraph()
            } catch (error) {
                console.error('Error:', error);
            }
        }

        function plotGraph(data, graphType,period) {
            var dates = data.Date;
            var layout = {
                title: `${data.Ticker} ${graphType} Plot for ${period}`,
                xaxis: { title: 'Date' },
                yaxis: { title: 'Price' }
            };
            var plotData;
            if (graphType === 'candlestick') {
                plotData = [{
                    x: dates,
                    close: data.Close,
                    decreasing: {line: {color: 'red'}},
                    high: data.High,
                    increasing: {line: {color: 'green'}},
                    low: data.Low,
                    open: data.Open,
                    type: 'candlestick',
                    xaxis: 'x',
                    yaxis: 'y'
                }];
            } else if (graphType === 'linegraph') {
                plotData = [{
                    x: dates,
                    y: data.Close,
                    type: 'scatter',
                    mode: 'lines',
                    line: { color: 'blue' }
                }];
            }
            console.log("Plotting data:", plotData);  // Debug statement
            Plotly.newPlot('graph-container', plotData, layout);
        }
    });