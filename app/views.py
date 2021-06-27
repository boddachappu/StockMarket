from django.shortcuts import render
from django.http import HttpResponse
from email.message import EmailMessage
import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib, ssl
from email.mime.text import MIMEText


# Create your views here.


def home():
    return HttpResponse('<h1>Welcome to Stocks Page</h1>')


def bulkDeals():
    url = 'https://www.moneycontrol.com/stocks/marketstats/bulk-deals/nse/'
    try:
        getBulkDeal(url)
    except Exception as e:
        return HttpResponse('<h1>There is some exception</h1>')
    else:
        return HttpResponse('<h1>Check you email please for the Bulk Deals</h1>')


def getBulkDeal(url):
    response = requests.get(url)

    data = BeautifulSoup(response.text, 'html.parser')
    # To get the division class where the table entries are present
    div = data.find('div', {'class': 'fidi_tbl MB20 bulkdls1 CTR'})
    # with open('data.html', 'w') as fp:
    #     fp.write(str(div))

    stock_dict = {}
    # Read the thead element in the data element 'div'
    tr = div.find_all('thead')
    # Find all the elements in which has the 'th' tag in the thead tag and return the list of all the elements with th tag
    th = tr[0].find_all('th')
    for i in th:
        # creates the dictionary with the table head tags
        stock_dict[i.text] = []

    # keep the keys in the list so that we can form the dataframe
    columns = list(stock_dict.keys())
    # Append one more element which stores the stock price end on that day
    columns.append('Price End')
    stock_dict.update({'Price End': []})

    # Find the tbody element tag
    tbody = div.find_all('tbody')

    # Find the tr element tag from the result of tbody
    tbodytr = tbody[0].find_all('tr')
    for i in range(len(tbodytr)):
        td = tbodytr[i].find_all('td')
        i = 0
        for j in td:
            stock_dict[columns[i]].append(j.text)
            i += 1

    df = pd.DataFrame(stock_dict)

    # To display all the columns in the data frame
    pd.set_option('display.max_columns', None)

    # Setting Email service
    smtp_server = 'smtp.gmail.com'
    sender = 'vinod.akaveeti04@gmail.com'
    # receiver = 'vinodcharan6@gmail.com'
    receiver = ['rashmi.prabhu94@gmail.com', 'vinodcharan6@gmail.com']
    port = 587
    password = 'Vinod@123'
    data = df.to_html(index=False)
    body = """<h1>Hi Welcome, below list shows the List of Bulk order for Yesterday</h1><br>{}""".format(data)
    body = MIMEText(body, 'html')
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = 'BULK DEALS NSE'
    msg['From'] = sender
    msg['To'] = receiver

    context = ssl.create_default_context()
    server = smtplib.SMTP(smtp_server, port)
    server.starttls(context=context)
    server.login(sender, password)
    server.send_message(msg)
    server.quit()
    return
