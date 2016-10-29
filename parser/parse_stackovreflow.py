import urllib.request, json, sys, os
from bs4 import BeautifulSoup

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
        qinfo = soup.find('table', {'id':'qinfo'})
        view_count = int(qinfo.find_all('tr')[1].find_all('td')[1].p.text.split()[0].strip())

        # get votes
        vote_count = int(soup.find('span', {'class':'vote-count-post '}).text.strip())

        # get favorites
        favorite_count = int(soup.find('div', {'class':'favoritecount'}).find('b').text.strip())

        # get tags
        tags = []
        tags_list = soup.find('div', {'class':'post-taglist'}).find_all('a')
        for tag in tags_list:
            tags.append(tag.text.strip())

        return {'url':url, 'title':title, 'content':content, 'answers':answers, 'answer_count':len(answers), 'view_count':view_count, 'vote_count':vote_count, 'favorite_count':favorite_count, 'tags':tags}
    except:
        return {}

with open('SearchList.txt', 'r') as fp:
    keys = fp.read().split()

for key in keys:
    url = 'http://stackoverflow.com/search?q=%s' % (key)
    #headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
    headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }
    r = urllib.request.Request(url, headers=headers)
    p = urllib.request.urlopen(r)
    html = p.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    questions = soup.find_all('div', {'class':'question-summary'})
    print('%s: %d' % (key, len(questions)))