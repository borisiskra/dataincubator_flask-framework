from flask import Flask, render_template, request, redirect, Response
import pandas as pd
import requests
import io, glob
import simplejson as json
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)

df = pd.DataFrame()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/index', methods=("POST", ))
def graph():
    #print('v'*100)

    global df 
    #Welcome to Alpha Vantage! Here is your API key: 7ENJ7TOOUOLNE7W4. Please record this API key for future access to Alpha Vantage.
    #https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=IBM&apikey=demo
    
    #print(list(request.form.items()))    SYMBOL = request.form.get('ticker', str)
    FEATURES = request.form.getlist('features',str)
    feat2num = {'open': '1', 'close':'2', 'low': '3', 'high': '4', 'volume': '5'}
    feat2plot = ''
    for feat in FEATURES:
        feat2plot += feat2num[feat]
    #print(FEATURES, feat2plot)

    df = get_data(SYMBOL)
    return render_template('index.html', feat2plot=feat2plot, ticker=SYMBOL)



@app.route('/plot/<features>')
def plot_png(features=''):
    #print("features:", features) 
    fig = create_figure(features)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure(features):
    global df 
    #print("features:", features) 
    if features == '':
        return 
    col_names = {'1': 'Open', '2': 'Close', '3': 'Low', '4': 'High', '5': 'Volume'}
    col_list = []
    for char in features:
        if char != '5':
            col_list.append(col_names[char])
    #print(col_list)
    
    fig = Figure()
    if '5' in features:
        fig.set_size_inches(12.8, 4.8)
        axis = fig.add_subplot(1, 2, 1)
        axis2 = fig.add_subplot(1, 2, 2)
        df[['Volume']].plot(ax=axis2)
    else:
        axis = fig.add_subplot(1, 1, 1)
    df[col_list].plot(ax=axis) # df.index.values,'1. open'
    return fig


def get_data(ticker):
    API_KEY = '7ENJ7TOOUOLNE7W4'
    #TIME_SERIES = 'TIME_SERIES_MONTHLY'
    TIME_SERIES = 'TIME_SERIES_DAILY'
    data_files = glob.glob("./*.data")
    #print(data_files)
    data_f = ".\\{}.data".format(ticker)
    #print(data_f)
    #print(data_f in data_files)
    data_dict = {}
    if data_f in data_files:
        with open(data_f, 'r') as fd:
            json_data = fd.readline()
        #print("     ====   got data from file   -------")
        #print(json_data)
        #print(type(json_data))
        #print("@"*60)
        data_dict = json.loads(json_data)
    else:
        if ticker != "":
            url = 'https://www.alphavantage.co/query?function=' + TIME_SERIES + '&symbol=' + ticker + '&apikey=' + API_KEY

            api_data = requests.get(url)
            json_page = api_data.text
            data_dict = json.loads(json_page)
        
        ####print("*"*50,"\nall keys")
        ####print( list(data_dict.keys()) )

        if data_dict == {}:
            return pd.DataFrame()

        for k in data_dict.keys():
            if "Time" in k:
                #print("_______",k)
                series_key = k
        #print(type(series_key))
        data_dict = data_dict[series_key]
        #print("     ====   got data from web   -------")

        with open(data_f, 'w') as fd:
             fd.write(json.dumps(data_dict))
        #print("     ====   wrote data to file   -------")

    col_names = {'1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. volume': 'Volume'}

    df = pd.DataFrame.from_dict(data_dict, orient='index')
    df.index = pd.to_datetime(df.index)
    df = df.astype('float64')
    df.rename(columns=col_names, inplace=True)
    return df


if __name__ == '__main__':
    app.run(port=33507)
