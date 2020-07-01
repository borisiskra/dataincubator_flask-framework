from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/index')
def graph(SYMBOL):
    API_KEY = '7ENJ7TOOUOLNE7W4'
    #Welcome to Alpha Vantage! Here is your API key: 7ENJ7TOOUOLNE7W4. Please record this API key for future access to Alpha Vantage.
    #https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=IBM&apikey=demo
        SYMBOL = request.form['ticker']
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=' + SYMBOL + '&apikey=' + API_KEY

    
    return url
    return render_template('about.html')



if __name__ == '__main__':
    app.run(port=33507)
