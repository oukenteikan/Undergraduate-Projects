from bs4 import BeautifulSoup
import requests
import sys
import time
import prettytable as pt
import pandas as pd

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'}
prefixs = {'shenyang':'http://zrzyj.shenyang.gov.cn/', }
urls = {'shenyang':'sygtzyj/tdjy/jyjg/glist.html', }
keys = prefixs.keys()
assert keys == urls.keys()

class get_link():

    def shenyang(links, url, key):
        url_list = [url]
        a = url.find('.html')
        for i in range(1, 29): #debug
            new_url = url[:a] + str(i) + url[a:]
            url_list.append(new_url)
        for ul in url_list:
            r = requests.get(prefix + ul, headers = headers)
            print(r.url)
            content = r.content.decode('utf-8')
            content = content.replace('\r', '')
            with open(key + '_glist.html', 'a+') as f:
                print(content, file=f)   
            soup = BeautifulSoup(content, 'lxml')
            rcs = soup.find_all('a', target = '_blank')
            for rc in rcs:
                link = rc['href']
                print(link)
                links.add(link)
            print("")
        return

class get_data():

    def shenyang(datum, link, key):
        r = requests.get(link, headers = headers)
        print(r.url)
        content = r.content.decode('utf-8')
        content = content.replace('\r', '')
        with open(key + '_page.html', 'a+') as f:
            print(content, file=f)
        soup = BeautifulSoup(content, 'lxml')
        
        nr = soup.find('div', class_ = 'nr_nr')
        tb = nr.find('table')
       
        if tb == None:
            return

        a = pd.concat(pd.read_html(tb.prettify()))

        with open(key + '_pandas.txt', 'a+') as f:
            print(a, file=f)
        datum.append(a)
        return

class get_dict:

    def shenyang(data_dict, data, key):
        contain = []
        keywords = ["时间", "总价", "单价", "面积"]
        for i in data.columns:
            col = data[i]
            for k in keywords:
                contain_bool = col.str.contains(k)
                for j in contain_bool:
                    if j == True:
                        contain.append(col)
                        break
        contain = pd.concat(contain, axis = 1)
        contain = contain.dropna()
        with open(key + '_pandas2.txt', 'a+') as f:
            print(contain, file=f)
        find_row = False
        for i in range(contain.shape[0]):
            row = contain.iloc[i, :]
            flag = True
            for k in keywords:
                row_true = row[row.str.contains(k)]
                if len(row_true) == 0:
                    flag = False
            if flag:
                contain.columns = row
                find_row = True
                break
        if not find_row:
            print(data)
            return
        contain = contain.iloc[:, ~contain.columns.duplicated()] 
        data_dict.append(contain)
        '''
        if contain.shape[1] > 4 and "交易时间" in contain.columns:
            for name in contain.columns:
                if "时间" in name and name != "交易时间":
                    del contain[name]
        if contain.shape[1] > 4:
            for name in contain.columns:
                if "建筑" in name:
                    del contain[name]
        for name in contain.columns:
            flag = False
            for k in keywords:
                if k in name:
                    flag = True
                    break
            if not flag:
                del contain[name]
        if contain.shape[1] != 4:
            print(contain.columns)
        for i in range(len(contain.columns)):
            for k in keywords:
                if k in contain.columns.values[i]:
                    contain.columns.values[i] = k
        if contain.shape[1] > 4:
            print(contain.columns, contain.shape)
        with open(key + '_pandas3.txt', 'a+') as f:
            print(contain, file=f)
        '''
        return

if __name__ == "__main__":

    for key in keys:
        prefix = prefixs[key]
        url = urls[key]
        links = set()
        getattr(get_link, key)(links, url, key)
        datum = []
        for link in links:
            getattr(get_data, key)(datum, link, key)
        data_dict = []
        for data in datum:
            getattr(get_dict, key)(data_dict, data, key)
        print("There are totally {} dicts.".format(len(data_dict)))
        data_dicts = pd.concat(data_dict, join = "outer", axis = 0)
        data_dicts.to_csv(key + '_data.txt')
        #json.dump(datum, open(key+'.json', 'w'))
