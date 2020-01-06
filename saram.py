import requests
from bs4 import BeautifulSoup

KEYWORD = 'python'

URL = f'http://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword={KEYWORD}&loc_mcd=101000&company_cd=0,1,2,3,4,5,6,7,9&panel_type=&search_optional_item=y&search_done=y&panel_count=y'


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pages = soup.find('div', {'class', 'pagination'}).find_all('a')
    last_page = pages[-2].string
    return int(last_page)


def extract_jobs(last_page):
    jobs = []
    for page in range(1, last_page + 1):
      print(f'Scrapping Saram page {page}')
      result = requests.get(
          f'{URL}&recruitPage={page+1}&recruitSort=relation&recruitPageCount=50&inner_com_type='
      )
      soup = BeautifulSoup(result.text, 'html.parser')
      results = soup.find_all('div', {'class', 'item_recruit'})
      for result in results:
          job = extract_job(result)
          # print(job)
          jobs.append(job)

    return jobs


def extract_job(html):
    title = html.find('h2', {'class', 'job_tit'}).find('a')['title']
    company = html.find('strong',{'class','corp_name'}).find('a')['title']
    link = html.find('h2', {'class', 'job_tit'}).find('a').get('href')
    link = ('https://saramin.co.kr'+link)
    location = html.find('div', {'class', 'job_condition'}).find('span').get_text().lstrip(' ').strip('\n')
    detail = html.find('div', {'class', 'job_condition'}).find_all('span')[1].get_text()


    return {'title':title,'company':company,'location':location, 'link':link, 'detail':detail}


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
