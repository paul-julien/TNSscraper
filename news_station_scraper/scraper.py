#!/usr/bin/env python3
import pandas as pd
from datetime import date
import datetime
from GoogleNews import GoogleNews #https://github.com/HurinHu/GoogleNews
import itertools
import pprint
from pprint import pprint
import argparse
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from newsreader import articleReader


def getDate():
    #get day of year
    global dateToday
    dateToday = str(date.today().month) + '/' + str(date.today().day) + '/' + str(date.today().year)
    return dateToday

def getDateLastWeek():
    #get day of year
    my_dateweek = date.today() - datetime.timedelta(days=6)
    global dateLastWeek
    dateLastWeek = str(my_dateweek.month) + '/' + str(my_dateweek.day) + '/' + str(my_dateweek.year)
    return dateLastWeek


def run(start_date, end_date, keyword, file, mail, importance):

    #find relevant news articles within given timeframe
    googlenews = GoogleNews()
    googlenews = GoogleNews(lang='en')
    googlenews = GoogleNews(start=start_date, end=end_date)
    googlenews.search(keyword)
    res = googlenews.result()
    googlenews.result()
    headlines = googlenews.gettext()
    links = googlenews.get__links() #note that documentation has this as googlenews.getlinks() so it might change
    #get page url
    results = articleReader(links,headlines, keyword)
    run.df = pd.DataFrame(results)
    if run.df.shape[0] > importance:
        run.df = run.df.iloc[0:importance]

    return run.df

def htmlConvert(table):
    html = ''
    for index, row in table.iterrows():
        html += '<h2 style="color:DarkSlateBlue">' + row["Headline"] + '</h2>'
        html += '<h3>Topic: ' + row["News Topic"] + '</h3>'
        if row["Summary"] == '':
            html += '<h3><em>Summary Not available</em></h3>'
        else:
            html += '<h3>Summary: <em>' + row["Summary"] + '</em></h3>'
        html += '<a href=' + row["Link"] + '>Link</a>'
        html += '<p style="color:DimGray">Website Popularity Rank: ' + row["Rank"] + '</p><br>'
    return html

def send_email(start_date, end_date, file, mail, dfhtml):
    if start_date == end_date:
        dfhtmlFinal = '<html> <body> <h1>Headlines for ' + start_date + '. </h1> ' + dfhtml + ' </body> </html>'
    else:
        dfhtmlFinal = '<html> <body> <h1>Headlines for ' + start_date + '-' + end_date + '. </h1> ' + dfhtml + ' </body> </html>'

    #email ##########
    sender_email = 'newsstationscrapeproposal@gmail.com'
    receiver_email = mail
    password = 't1e2s3t4'
    message = MIMEMultipart("alternative")
    message["Subject"] = "The News Station scrape test"
    message["From"] = 'newsstationscrapeproposal@gmail.com'
    message["To"] =  mail

    # Create the plain-text and HTML version of your message
    if start_date == end_date:
        text = 'Headlines for ' + start_date + ':\n' + dfhtml
    else:
        text = 'Headlines for ' + start_date + '-' + end_date + ': \n' + dfhtml
    html = dfhtmlFinal
    print('html \n ', html)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

    #create file
    #with open(str(file) + '.txt', 'w') as out:
    #    pprint(results, stream=out)
    #create html file
    #with open(str(file) +".html", "w") as file:
    #    file.write(dfhtmlFinal)
    ###########

def parse_args():
    #Parse command line arguments
    parser = argparse.ArgumentParser(description="web scrape dates")
    parser.add_argument(
        "--start_date", help="Start date for scraping",
        default=dateToday, required=False)
    parser.add_argument(
        "--end_date", help="End date for scraping.", default=dateToday,
        required=False)
    parser.add_argument(
        "--keyword", help="Keyword search", default='cannabis',
        required=False)
    parser.add_argument(
        "--file", help="choose .txt and .html file name", default='news--results',
        required=False)
    parser.add_argument(
        "--mail", help="who to send to ", default='pjburg@me.com',
        required=False)
    return parser.parse_args()

if __name__ == "__main__":
    table = pd.DataFrame(columns=['Headline', 'News Topic', 'Summary', 'Link'])
    topics = ['Cannabis', 'LSD', 'Psilocybin', 'CBD', 'Drug criminal justice', 'Woman incarceration']
    importance = [5, 2, 2, 3, 3, 3]
    getDate()
    getDateLastWeek()
    args = parse_args()
    for i, j in zip(topics, importance):
        run(args.start_date, args.end_date, i, args.file, args.mail, j)
        table = pd.concat([table, run.df])
        #text = text + '<b><b>' + run.dfhtml
    #print('table: \n', table)
    tablehtml = htmlConvert(table)
    print('tablehtml: ', tablehtml)
    #tablehtml = table.to_html(
    #index = False, justify = 'center', col_space = '25%').replace(
    #'<th>','<th style = "background-color: HoneyDew">')
    #.replace('<table border="1" class="dataframe">', ' <table border="4" class="dataframe">\n <colgroup>\n <col span="1" style="width: 60%;">\n    <col span="1" style="width: 10%;">\n    <col span="1" style="width: 15%;">\n    <col span="1" style="width: 15%;">\n </colgroup>\n')

    send_email(args.start_date, args.end_date, args.file, args.mail, tablehtml)
args = parse_args()
args = parse_args()
print('Done')
