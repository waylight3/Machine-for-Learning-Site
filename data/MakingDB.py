import os
import json
from sqlite3 import *
os.chdir('C:\\Users\Public\Desktop\Machine-for-Learning-Site\parser\ids')
######## load json
datas={}
for i,j in enumerate(os.listdir()):
    with open(j) as data_file:    
        datas[j] = json.load(data_file)
datass=list(datas.keys())
datass.sort()

import urllib.request, json, sys, os, time
from bs4 import BeautifulSoup
os.chdir('C:\\Users\Public\Desktop\Machine-for-Learning-Site\data')
########### connect db
db=connect('dbofsite.db')
cursor=db.cursor()
########### parsing source
def get_post_by_id(idx):
    try:
        # get html code
        url = 'http://stackoverflow.com/questions/%d' % int(idx)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        r = urllib.request.Request(url, headers=headers)
        p = urllib.request.urlopen(r)
        html = p.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # get title
        title = soup.find('a', {'class':'question-hyperlink'}).text.strip()

    

        # get answers
        answers = []
        answers_list = soup.find_all('div', {'class':'answer'})
        for answer in answers_list:
            td = answer.find('td', {'class':'answercell'})
            answers.append(td.find('div').text.strip())

        # get views
        try:
            qinfo = soup.find('table', {'id':'qinfo'})
            view_count = int(qinfo.find_all('tr')[1].find_all('td')[1].p.text.split()[0].strip())
        except:
            view_count = 0

        # get votes
        try:
            vote_count = int(soup.find('span', {'class':'vote-count-post '}).text.strip())
        except:
            vote_count = 0

        # get favorites
        try:
            favorite_count = int(soup.find('div', {'class':'favoritecount'}).find('b').text.strip())
        except:
            favorite_count = 0

        # get tags
        tags = []
        try:
            tags_list = soup.find('div', {'class':'post-taglist'}).find_all('a')
            for tag in tags_list:
                tags.append(tag.text.strip())
        except:
            pass

        return {'url':url, 'title':title, 'answer_count':len(answers), 'view_count':view_count, 'vote_count':vote_count, 'favorite_count':favorite_count, 'tags':tags}
    except:
        return {}

for data in datass:
    print(data)
    idx=datas.get(data)
    for i in range(len(idx)):
        result=get_post_by_id(int(idx[i]))
        tu=[result.get('answer_count'),result.get('favorite_count'),'#'.join(result.get('tags')),result.get('title'),result.get('url'),result.get('view_count'),result.get('vote_count')]
        cursor.execute('''INSERT INTO sites (answer_count,favorite_count,tags,title,url,view_count,vote_count) VALUES(?,?,?,?,?,?,?)''',tu)
        db.commit()

