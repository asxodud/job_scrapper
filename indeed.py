import requests
from bs4 import BeautifulSoup

LIMIT = 50
KEYWORD = 'python'
URL = f'https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and={KEYWORD}&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&as_src=&radius=25&l=Seoul&fromage=any&limit={LIMIT}&sort=&psf=advsrch&from=advancedsearch'


def extract_indeed_pages():

    indeed_result = requests.get(URL)
    indeed_soup = BeautifulSoup(indeed_result.text, 'html.parser')

    pagination = indeed_soup.find("div", {"class": "pagination"})

    links = pagination.find_all("a")
    pages = []

    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]

    return max_page


def extract_job(html):
    title = html.find('div', {'class': 'title'}).find('a')['title']
    company = html.find('span', {'class': 'company'})
    company_a = company.find('a')
    if company_a is not None:
        company = str(company_a.string)
    else:
        company = str(company.string)
    company = company.strip()

    location = html.find('div', {'class', 'recJobLoc'})['data-rc-loc']
    job_id = html['data-jk']

    return {'title': title, 'company': company, 'location': location,'link':f'https://kr.indeed.com/viewjob?jk={job_id}'}


def extract_jobs(last_page):
  
  jobs = []
  # Get last page
  for page in range(last_page):
    print(f'Scrapping Page {page}')
    result = requests.get(f'{URL}&start={page*LIMIT}')
    # print(result.status_code)
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all('div', {'class': 'jobsearch-SerpJobCard'})

  # Get title & Company
    for r in results:
        job = extract_job(r)
        jobs.append(job)
  return jobs



def get_jobs():
  last_page = extract_indeed_pages()
  jobs = extract_jobs(last_page)
  return jobs 
