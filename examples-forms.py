from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import Form
from datetime import datetime
import requests

import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'our very hard to guess secretfir'

@app.route('/')
def index():
    return render_template('index.html')


 # Simple form handling using raw HTML forms
@app.route('/data-retrieve', methods=['GET', 'POST'])
def data_retrieve():
    mydata= {'lst' : []}
    error = ""
    if request.method == 'POST':
        ticker = request.form['ticker']
        datedeb = request.form['datedeb']
        dateEnd = request.form['dateend']
        xperiod = int(request.form['xperiod'])
        print(xperiod)
    #TODO can test if data are
        mydata = getData(ticker,xperiod, datedeb,dateEnd)
      #  print(mydata)
    #render the data retrieve page
    return render_template('data-retrieve.html', message=error,data=mydata['lst'])
   

def getData(ticker,xperiod,dateDeb,dateFin):
    api_url = "https://www.sikafinance.com/api/general/GetHistos"
    payload = {
        "ticker": ticker,
        "xperiod": xperiod,
        "datefin": dateFin,
        "datedeb" : dateDeb
    }

    #print(payload)
    headers = {
        "accept": "*/*",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "no-cache",
        "content-type": "application/json;charset=UTF-8",
        "cookie": "_ga=GA1.2.803303644.1660530733; __gads=ID=4ebb5b4b4bc3835e:T=1660530733:S=ALNI_MYFKapHKqM5T0wn5xOUyezL5xFUHA; _gid=GA1.2.2040239953.1661115998; __gpi=UID=00000a839193b21b:T=1660530733:RT=1661115997:S=ALNI_MZzCOONMVTB12hYB66TJDO1paWuqQ; _gat=1",
        "pragma": "no-cache",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36"
    }
    response = requests.request(
        "POST", api_url, json=payload, headers=headers)
    response = response.json()
    
    response1 = response['lst']
    print(response1)
    df = pd.DataFrame(response1)
    return response



# Run the application
app.run(debug=True)


