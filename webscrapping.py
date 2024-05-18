# -*- coding: utf-8 -*-
"""WebScrapping.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VeQHFPGIByNUZTRd0FK6DT2xtGZ0qDHF

## Import python libraries:
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

"""## Declaring functions get detail data:"""

def get_title(soup):
    return soup.find('title').text.lower()

def get_header(soup,size):
    header_tag = f"h{size}"
    data = soup.find_all(header_tag)
    text = ' '.join(map(lambda h: h.text.lower(), data))
    return text

def get_paragraphs(soup):
    paragraphs=soup.find_all('p')
    return' '.join(map(lambda h: h.text.lower(), paragraphs))

def get_all_headers(soup):
    for n in range(1,7):
        get_header(soup,n)

def get_soup(url):
    res = requests.get(url)
    return BeautifulSoup(res.text, 'html.parser')

def weights(Title, h1, h2, h3, h4, h5, h6, para,concatinated):
    word_weights = {}
    for word in set(concatinated):
        weight = 0
        if(word in Title):
            weight = weight + 1
        if(word in h1):
            weight = weight + 0.8
        if(word in h2):
            weight = weight + 0.7
        if(word in h3):
            weight = weight + 0.6
        if(word in h4):
            weight = weight + 0.5
        if(word in h5):
            weight = weight + 0.4
        if(word in h6):
            weight = weight + 0.3
        if(word in para):
            weight = weight + 0.5
        word_weights[word] = weight
    return word_weights

def sortKeysInDescendingOrder(df,urls):
    webdirectory_dict = {}
    for i in range(len(df)):
        data = df.iloc[1]
        url = urls[i]
        sortedList = sorted(data.items(), key=lambda kv: kv[1], reverse=True)
        webdirectory_dict[url] = sortedList
    return webdirectory_dict

def writeToTextFile(content):
    f = open("webdirectory.txt", "w")
    f.write("{\n")
    for k in content.keys():
        f.write(F"'{k}': '{content[k]}',\n")  # add comma at end of line
    f.write("}")
    f.close()

"""## Main programme:"""

if __name__ == '__main__':

  with open ('URLList.txt', 'r') as file:
        urls = file.readlines()
        titles=[]
        h1s= []
        h2s= []
        h3s= []
        h4s= []
        h5s= []
        h6s= []
        paragraphs= []
        count = 0
        for url in urls:
          #Remove spaces at the beginning and at the end of the string
            strippedUrl = url.strip()
            if(strippedUrl and count < 10):
                soup = get_soup(strippedUrl)
                titles.append(get_title(soup))
                paragraphs.append(get_paragraphs(soup))
                h1s.append(get_header(soup,1))
                h2s.append(get_header(soup,2))
                h3s.append(get_header(soup,3))
                h4s.append(get_header(soup,4))
                h5s.append(get_header(soup,5))
                h6s.append(get_header(soup,6))
                count= count+1
        df = pd.DataFrame(list(zip(titles, h1s, h2s, h3s, h4s, h5s, h6s,
                                   paragraphs)),
               columns =['Title', 'h1', 'h2','h3', 'h4', 'h5','h6','paragraph'])

        df.to_csv('raw_data.csv', index=False)

        df['concatinated'] = df[['Title','h1','h2','h3','h4', 'h5', 'h6',
                                 'paragraph']].agg(' '.join, axis=1)

        #Read stopwords from commonwords.txt file and do the removal of stopwords
        with open('commonwords.txt', 'r', encoding="utf8") as f:
          stopWords = f.readlines()
          stopWords_arr = []
          for stopWord in stopWords:
            strippedStopWord = stopWord.strip()
            stopWords_arr.append(strippedStopWord)

        df['concatinated_clean'] = df['concatinated'].apply(lambda x: ' '.
                                                            join([word for word
                                                                  in x.split()
                                                                  if word not in
                                                                  stopWords_arr]))

        stemmer = SnowballStemmer("english")
        # Stem every word
        df['stemmed'] = df['concatinated_clean'].apply(lambda x: [stemmer.stem(y)
        for y in x.split()])
        df['stemmed'].to_csv('stemmed.csv', index=False)

        df['weighted'] = df.apply(lambda x: weights(x['Title'], x['h1'], x['h2'],
                                                    x['h3'], x['h4'], x['h5'],
                                                    x['h6'],x['paragraph'],
                                                    x['stemmed']), axis=1)

        result = sortKeysInDescendingOrder(df['weighted'], urls)

        writeToTextFile(result)