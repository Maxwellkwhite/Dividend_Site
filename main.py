import requests
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from wtforms import StringField, SubmitField, RadioField, SelectField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
import json

API = "2e3b70ef81msh075bd5e7a78e0d1p1cb0e0jsncaa0e3da7283"

app = Flask(__name__)
ckeditor = CKEditor(app)
Bootstrap5(app)
app.config['SECRET_KEY'] = 'abc'

class StockInput(FlaskForm):
    stock = StringField("", validators=[DataRequired()], render_kw={'placeholder': 'Enter Stock Symbol', 'class':'input_stock'})
    # submit = SubmitField("Search", render_kw={'class':'submit_button'})

@app.route('/', methods=["GET", "POST"])
def dividends():
    form = StockInput()
    stock_input = 'jnj'
    with open('jnj_summary.json', 'r') as file:
        jnj_sum = json.load(file)
    divYieldFwd = round(jnj_sum['data'][0]['attributes']['divYieldFwd'], 2)
    divYieldTtm = round(jnj_sum['data'][0]['attributes']['divYieldTtm'], 2)
    payoutRatio = round(jnj_sum['data'][0]['attributes']['payoutRatio'], 2)
    dividendGrowth = round(jnj_sum['data'][0]['attributes']['dividendGrowth'], 2)
    leveredFreeCashFlowYoy = round(jnj_sum['data'][0]['attributes']['leveredFreeCashFlowYoy'], 2)
    ltDebtEquity = round(jnj_sum['data'][0]['attributes']['ltDebtEquity'], 2)
    estimateEps = round(jnj_sum['data'][0]['attributes']['estimateEps'], 2)
    divRate = round(jnj_sum['data'][0]['attributes']['divRate'], 2)
    companyName = (jnj_sum['data'][0]['attributes']['companyName'])
    sectorname = (jnj_sum['data'][0]['attributes']['sectorname'])

    if form.validate_on_submit():
        stock_input = (form.stock.data).lower()
        try:
            querystring = {"symbols":f"{stock_input}"}
            headers = {
                "x-rapidapi-key": API,
                "x-rapidapi-host": "seeking-alpha.p.rapidapi.com"
            }
            response = requests.get("https://seeking-alpha.p.rapidapi.com/symbols/get-summary", headers=headers, params=querystring)
            jnj_sum = response.json()
            divYieldFwd = round(jnj_sum['data'][0]['attributes']['divYieldFwd'], 2)
            divYieldTtm = round(jnj_sum['data'][0]['attributes']['divYieldTtm'], 2)
            payoutRatio = round(jnj_sum['data'][0]['attributes']['payoutRatio'], 2)
            dividendGrowth = round(jnj_sum['data'][0]['attributes']['dividendGrowth'], 2)
            leveredFreeCashFlowYoy = round(jnj_sum['data'][0]['attributes']['leveredFreeCashFlowYoy'], 2)
            ltDebtEquity = round(jnj_sum['data'][0]['attributes']['ltDebtEquity'], 2)
            estimateEps = round(jnj_sum['data'][0]['attributes']['estimateEps'], 2)
            divRate = round(jnj_sum['data'][0]['attributes']['divRate'], 2)
            companyName = (jnj_sum['data'][0]['attributes']['companyName'])
            sectorname = (jnj_sum['data'][0]['attributes']['sectorname'])
        except TypeError:
            stock_input = 'Symbol not found'
            divYieldFwd = 'NA'
            divYieldTtm = 'NA'
            payoutRatio = 'NA'
            dividendGrowth = 'NA'
            leveredFreeCashFlowYoy = 'NA'
            ltDebtEquity = 'NA'
            estimateEps = 'NA'
            divRate = 'NA'
            companyName = 'NA'
            sectorname = 'NA'
    return render_template("index.html", 
                           form=form, 
                           stock_input=stock_input.upper(), 
                           divYieldFwd = divYieldFwd,
                           divYieldTtm = divYieldTtm,
                           payoutRatio = payoutRatio,
                           dividendGrowth = dividendGrowth,
                           leveredFreeCashFlowYoy = leveredFreeCashFlowYoy,
                           ltDebtEquity = ltDebtEquity,
                           estimateEps = estimateEps,
                           divRate = divRate,
                           companyName = companyName,
                           sectorname = sectorname,)


#metrics I want
    # P/E Ratio: Is the stock over or under-valued?
    # Dividend Yield: What percentage return is the dividend providing?
    # Growing Cash Flow: Is the company's cash flow increasing over time?
    # Cash Flow Per Share: How much cash flow is generated per share?
    # Dividend Growth Rate: Is the dividend growing consistently?
    # Shares Outstanding: How many shares are available and are they increasing or decreasing?
    # Free Cash Flow: Is there enough free cash flow to cover dividends?


# querystring = {"symbol":"jnj","years":"5","group_by":"month"}

# headers = {
# 	"x-rapidapi-key": API,
# 	"x-rapidapi-host": "seeking-alpha.p.rapidapi.com"
# }

# response = requests.get("https://seeking-alpha.p.rapidapi.com/symbols/get-dividend-history", headers=headers, params=querystring)

# print(response.json())


# querystring = {"symbols":"jnj"}

# headers = {
# 	"x-rapidapi-key": API,
# 	"x-rapidapi-host": "seeking-alpha.p.rapidapi.com"
# }

# response = requests.get("https://seeking-alpha.p.rapidapi.com/symbols/get-summary", headers=headers, params=querystring)

# print(response.json())

if __name__ == "__main__":
    app.run(debug=True, port=5002)