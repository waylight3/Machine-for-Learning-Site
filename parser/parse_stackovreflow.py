import urllib.request, json, sys, os, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

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
    keys = fp.read().split('\n')

chrome_path = r'C:\Users\ok\Desktop\chromedriver.exe'
driver = webdriver.Chrome(chrome_path)

id_list = {}

for key in keys:
    temp_list = []
    url='http://stackoverflow.com/search?pagesize=50&q=%s' % key
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    spans = soup.find_all('span', {'class':'page-numbers'})
    try: last_page = int(soup.find_all('span', {'class':'page-numbers'})[-3].text)
    except: last_page = 1
    print('%s[%d]: ' % (key, last_page), end='')
    for page in range(1, last_page + 1):
        print(page, end=' ', flush=True)
        url = 'http://stackoverflow.com/search?page=%d&pagesize=50&q=%s' % (page, key)
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.find_all('div', {'class':'result-link'})
        for div in divs:
            temp_list.append(div.span.a['href'].strip().split('/')[2])
        time.sleep(1)
    id_list[key] = temp_list
    time.sleep(1)
    print()
with open('id_list.json', 'w') as fp:
    fp.write(json.dumps(id_list))
driver.close()