import re
import requests
from bs4 import BeautifulSoup
import json
import msgpack
import sys
import os
import random
import matplotlib.pyplot as plt
import time

from urllib import request

from Functions import getHTMLText

## Imitate human user
user_agent = [
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12;) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
]

def main():
    page_list = []
    for i in range(1, 28):
        url_base = 'http://gtghj.wuhan.gov.cn/pt-317-2-{}.html'.format(i)
        html_text = getHTMLText(url_base.format(1), _headers=user_agent[random.randint(0, len(user_agent)-1)])
        html_text.encoding = 'gbk'
        html_text = html_text.text
        html_text = html_text[ html_text.find('<div id="list">') : ]
        html_text = html_text[ : html_text.find('<div id="bottom">') ]
        # html_text.encode('gbk', errors="strict")

        #assert i==1        # assert for check
        #print(html_text)   # check the sub-string of webpage

        bs = BeautifulSoup(html_text, 'lxml')
        bs = bs.find_all('a')

        #assert i==1      # assert for check
        #print(type(bs))  # output[0]: <class 'bs4.element.ResultSet'> // This class can be used as 'List'.

        bs = [h for h in bs if (h.contents[0] in [r'首页', r'上一页', r'下一页', r'末页']) == False]
        page_list += [('http://gtghj.wuhan.gov.cn'+h['href'], h.contents[0]) for h in bs]

    #print(page_list[0])

    data = []

    for i in range(len(page_list)):
        print(i)
        time.sleep(0.25)
        url = page_list[i][0]
        html_text = getHTMLText(url, _headers=user_agent[random.randint(0, len(user_agent)-1)])
        html_text.encoding = 'gbk'
        html_text = html_text.text

        html_text = html_text[ html_text.find('<div class="content">') : ]
        html_text = html_text[ : html_text.find('</div>') ]

        bs = BeautifulSoup(html_text, 'lxml')
        bs = bs.find('table')
        if bs is None:
            print(page_list[i], i)
            continue
        bs = bs.find_all('tr')

        table = [line.find_all('td') for line in bs]
        table = [[str(col_ele) for col_ele in line] for line in table]
        table = [[re.sub(r'<.*?>', '', col_ele) for col_ele in line] for line in table]

        #assert i==0
        #print(table)

        data.append(table)

    json.dump(data, open('wuhan.json', 'w', encoding='utf8'))
    #msgpack.dump(data, open('wuhan.msgpack', 'wb'))

if __name__ == '__main__':
    main()

"""
## Translate a complex and disorderly html text to a orderly list of the shops' details
def textTranslator(text):

    ## Assure the range of shop details and cut the text
    text = text[text.find('<div class="shop-list J_shop-list shop-all-list" id="shop-all-list">') : ]
    text = text[ : text.find('<div class="page">')]

    ## Explain by xml
    bs = BeautifulSoup(text, 'lxml')
    #print(bs.prettify())

    ## Get the labels of shops
    bs = bs.find_all(attrs={'class': 'shop-list J_shop-list shop-all-list'})[0]
    bs = bs.contents[1]
    bs_list = bs.contents

    ## Drop out the blank elements
    bs_list = [w for w in bs_list if len(w) > 1]

    bs_list = [w.find_all(attrs={'class': 'txt'})[0] for w in bs_list]

    ## The list for return
    shop_details = []

    for i in range(len(bs_list)):
        detail = {}

        ## Get names, id-s, and the url of the shops
        shop_d = bs_list[i].find_all(attrs={'class': 'tit'})[0].find_all(attrs={'data-click-name': 'shop_title_click'})[0]
        #shop_d = shop_d.find_all(a)

        detail[r'name']  = shop_d['title']
        detail[r'id']    = shop_d['data-shopid']
        detail[r'url']   = shop_d['href']

        ## Get the number of comments and the mean prices
        comment_d = bs_list[i].find_all(attrs={'class': 'comment'})[0]
        rev_num = comment_d.find_all(attrs={'class': 'review-num'})
        ave_pri = comment_d.find_all(attrs={'class': 'mean-price'})[0].find('b')

        if ave_pri:
            ave_pri = ave_pri.string
            ave_pri = re.sub('\D', '', ave_pri)            
            detail[r'price'] = int(ave_pri)
        else:
            detail[r'price'] = 0

        if len(rev_num) > 0:
            rev_num = rev_num[0].find('b').string
            detail[r'rev_num'] = int(rev_num)
        else:
            detail[r'rev_num'] = 0

        ## Get the recommended dishes
        recommend_d = bs_list[i].find_all(attrs={'class': 'recommend'})
        if len(recommend_d) > 0:
            recommend_d = recommend_d[0]
            dishes = [i.string for i in recommend_d.find_all(attrs={'class': 'recommend-click'})]
        else:
            dishes = []
        detail[r'dishes'] = dishes

        ## Get average scores of taste, environment, services
        scores_d = bs_list[i].find_all(attrs={'class': 'comment-list'})
        if len(scores_d) > 0:
            scores_d = scores_d[0]
            scores = [i.string for i in scores_d.find_all('b')]
            if len(scores) != 3:
                scores = [0.0, 0.0, 0.0]
        else:
            scores = [0.0, 0.0, 0.0]

        detail[r'taste'] = float(scores[0])
        detail[r'environ'] = float(scores[1])
        detail[r'service'] = float(scores[2])

        shop_details.append(detail)

        #print(scores)
        #print(detail)

    return shop_details

def getCityShops(cityname, pages=20):
    url_base = 'https://www.dianping.com/' + str(cityname) + '/ch10/'
    shops = []
    for i in range(pages):
        print(i)
        url = url_base + 'p' + str(i+1)
        html_text = getHTMLText(url, _headers=user_agent[random.randint(0, len(user_agent)-1)])
        html_text = textNumberTrans(html_text, number_map)

        shops.extend(textTranslator(text=html_text))

    return shops
"""