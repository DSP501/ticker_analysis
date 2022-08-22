
from flask import Flask, request, render_template
# from flask_cors import CORS

import pandas_datareader as web
import pandas as pd
import datetime as dt

app = Flask(__name__)

# CORS(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    
    data = {}
    
    if request.method == 'GET':
        pass
    
    if request.method == "POST":
        ticker = request.form.get('ticker')
        data = getData(ticker)
        print(data)
        

    return render_template('index.html', data=data)        



def getData(ticker):
    
    ticker = ticker + ".NS"
    print(ticker)
    
    st = dt.datetime.now() - dt.timedelta(days=1825)
    et = dt.datetime.now()
    
    try:
        df = web.DataReader(ticker, 'yahoo', st, et)
        # print(df.head)
    except web._utils.RemoteDataError as e:
        data = {'error' : "Wrong Ticker Name"}
        return data
    except Exception as e:
        data = {'error' :  "Some Error Occured Try Later"}
        return data
            
    data = {

    "Stock Name" : ticker,
    "Current Price" : round(df['Close'][-1], 2),
    "Day Change" : round(((df['Close'][-1] - df['Close'][-2]) / df['Close'][-2]) * 100, 2),
    "Week Change" : round(((df['Close'][-1] - df['Close'][-5]) / df['Close'][-5]) * 100, 2),
    "Month Change" : round(((df['Close'][-1] - df['Close'][-27]) / df['Close'][-27]) * 100, 2),
    "ytd" : round(((df['Close'][-1] - df['Close']['2022-01-03']) / df['Close']['2022-01-03']) * 100, 2),
    "six" : round(((df['Close'][-1] - df['Close'][-124]) / df['Close'][-124]) * 100, 2),
    "One Year" : round(((df['Close'][-1] - df['Close'][-248]) / df['Close'][-248]) * 100, 2),
    "Three Year" : round(((df['Close'][-1] - df['Close'][-742]) / df['Close'][-742]) * 100, 2),
    "Five Year" : round(((df['Close'][-1] - df['Close'][-1234]) / df['Close'][-1234]) * 100, 2)
    
    }
    
    return data
    
    
if __name__ == '__main__':
    app.run(debug=True);