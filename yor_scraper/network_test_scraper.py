from bs4 import BeautifulSoup
from pathlib import Path

import requests as http

def try_network():
    print('Fetching...')

    absolute_path = Path('.').resolve() / "yor_scraper/test_data_output"
    if(not absolute_path.exists()): absolute_path.mkdir()
    print(f'Absolute Path = {absolute_path}')

    html_text = http.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    for index, job in enumerate(jobs):
        published_date = str(job.find('span', class_='sim-posted').span.text).lower()
        print(published_date)

        if(published_date == 'posted today' or published_date == 'posted 2 days ago' or published_date == 'posted few days ago'):
            company_name = str(job.find('h3', class_='joblist-comp-name').text)
            skills = str(job.find('span', class_='srp-skills').text.replace(' ', ''))
            more_info = job.header.h2.a['href']
            
            with open(f'{absolute_path}/job_{index + 1}.txt', 'w') as f:
                f.write(f'Company Name = {company_name.strip()}\n')
                f.write(f'Skills = {skills.strip()}\n')
                f.write(f'More Info = {more_info}\n')

    print('Extracted data from webpage')