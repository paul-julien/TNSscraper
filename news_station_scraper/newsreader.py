#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
from gensim.summarization import summarize
from gensim.summarization import keywords
import urllib.request, sys, re
import xmltodict, json

def alexaRank(link):
    xml = urllib.request.urlopen('http://data.alexa.com/data?cli=10&dat=s&url={}'.format(link)).read()

    result= xmltodict.parse(xml)

    data = json.dumps(result).replace("@","")
    data_tojson = json.loads(data)
    url = data_tojson["ALEXA"]["SD"][1]["POPULARITY"]["URL"]
    alexaRank.rank= data_tojson["ALEXA"]["SD"][1]["POPULARITY"]["TEXT"]
    return alexaRank.rank


def articleReader(links, headlines, keyword):
    results = []
    for i, j in zip(links, headlines):
        url = i

        #get content of url
        try: page = requests.get(i, timeout=4).text
        except: continue

        #get html tags
        soup = BeautifulSoup(page)

        #get text from all the content components of article
        content = soup.find_all('p')

        #get all words in article
        content_text = []
        for c in content:
            words = c.get_text().strip()
            content_text.append(words)

        content_text
        #get article
        #article = list(itertools.chain.from_iterable(content_text))
        articleFirstEdit = [keptSentence for keptSentence in content_text if not '\n' in keptSentence]
        articleSecondtEdit = [keptSentence for keptSentence in articleFirstEdit if '.' in keptSentence]
        articleThirdEdit = [keptSentence for keptSentence in articleSecondtEdit if not 'Image' in keptSentence]
        finalArticle = ' '.join(list(articleThirdEdit))
        #summarize article with natural language processing
        try:
            article_summary = summarize(finalArticle, word_count=75)
            article_summary_pretty = article_summary.replace('.', '. ')
        except:
            article_summary_pretty = 'Empty article or not available'
        try:
            article_keywords = keywords(article_summary, ratio = 0.3, lemmatize = True, words = 5, split = True)
            article_keywords_pretty = ", ".join(str(x) for x in article_keywords)
        except:
            article_keywords_pretty = 'Empty article or not available'
        link = i
        alexaRank(i)
        results.append({'Headline': j, 'News Topic': keyword, 'Summary': article_summary_pretty.replace('\n', ''), 'Link': link, 'Rank': alexaRank.rank })
    #print(results)
    return results
    #results.append('')
    #results.append('-------------------')
    #results.append('')
    #convert to html
