import os
import json
os.chdir('C:\\Users\Public\Desktop\Machine-for-Learning-Site\parser\ids')
datas={}
for i,j in enumerate(os.listdir()):
    with open(j) as data_file:    
        datas[j] = json.load(data_file)
datass=list(datas.keys())
datass.sort()

import urllib.request, json, sys, os, time

from bs4 import BeautifulSoup
import docclass
import nltk
from nltk.corpus import stopwords
from nltk import tokenize as tk
stop = stopwords.words('english')
cl=docclass.fisherclassifier(docclass.getwords)
import os
os.chdir('C:\\Users\\kikun\Desktop')
with open('SearchList.txt', 'r') as fp:
    keys2 = [i for i in fp.read().lower().split('\n') if not i in stop]
cl.setdb('test3.db')
def get_post_by_id(idx):
    try:
        # get html code
        url = 'http://stackoverflow.com/questions/%d' % idx
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        r = urllib.request.Request(url, headers=headers)
        p = urllib.request.urlopen(r)
        html = p.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # get title
        title = soup.find('a', {'class':'question-hyperlink'}).text.strip()

        # get content
        content = soup.find('td', {'class':'postcell'}).find('div', {'class':'post-text'}).text.strip()

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

        return {'url':url, 'title':title, 'content':content, 'answers':answers, 'answer_count':len(answers), 'view_count':view_count, 'vote_count':vote_count, 'favorite_count':favorite_count, 'tags':tags}
    except:
        return {}

    
class learning_classify():
    def __init__(self,title,cl,keys,T=True):
        titles=[]
        for i in title:
            try:
                titles.append(' '.join([w for w in i.lower().split() if not w in stop]))
            except: pass
        self.titles=titles
        self.cl=cl
        self.keys=keys
        self.T=T
        self.counts=self.count()
        self.responses=self.response()
        
    def count(self):
        counts=[]
        for title in self.titles:
            have={}
            for key in self.keys:
                if key in title:
                    have[key]=title.count(key)
            counts.append(have)
        return counts
    
    def response(self):
        if self.T==True:
            responses=[]
            for l in self.counts:
                if list(l.values()):
                    responses.append(list(l.keys())[list(l.values()).index(max(list(l.values())))])
                else: responses.append('machine learning')
            return responses
        if self.T!=True:
            responses=[]
            for i in range(len(self.titles)):
                responses.append('not')
            return responses
    def train_bayes(self):
        for i in range(len(self.responses)):
            self.cl.train(self.titles[i],self.responses[i])


for data in datass:
    try:
        print(data)
        idx=datas.get(data)
        results=[]
        for i in range(len(idx)):
            results.append(get_post_by_id(int(idx[i])))
        title=[]
        for i in range(len(results)):
            title.append(results[i].get('title'))

        os.chdir('C:\\Users\\kikun\Desktop')
        with open('SearchList.txt', 'r') as fp:
            keys2 = [i for i in fp.read().lower().split('\n') if not i in stop]
        lc=learning_classify(title,cl,keys2,True)
        lc.train_bayes()
    except: pass

