from bs4 import BeautifulSoup
from pathlib import Path

import requests as http
import csv

def read_articles():
    """
    This is used to read all top articles from the Yoruba webpage of Global Voices
    """
    print('Reading home page...')

    absolute_path = Path('.').resolve() / "yor_scraper/yor_data_output"
    if(not absolute_path.exists()): absolute_path.mkdir()
    print(f'Absolute Path = {absolute_path}')

    csv_path = absolute_path / 'properly_diacritized_data.csv'
    with open(csv_path, mode='w') as csv_file:
        # set CSV file header
        fieldnames = ['title', 'content', 'link_to_resource', 'published_date']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # websites to parse
        html_text = http.get('https://yo.globalvoices.org/').text

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html_text, 'lxml')

        # contains the article title, link and date
        articles = soup.find_all('article', class_="gv-promo-card-dense gv-promo-card gv-post-promo-card")

        for article in articles:
            # inside these articles, we get individual titles, links and date
            article_title_container = article.find('div', class_='gv-promo-card-text')
            link_of_article = str(article_title_container.a['href']).strip()
            title_of_article = str(article_title_container.a.text).strip()

            article_date_container = article.find('div', class_='gv-promo-meta')
            date_of_article = (article_date_container.find('span', class_='datestamp').text).strip()
            
            # we use the article link to fetch article contents(paragraphs)
            content = str(_scrape_global_voices(url_to_scrape=str(link_of_article), title=title_of_article)).strip()

            # print to console
            output_template = _use_template(title=title_of_article, link=link_of_article, date=date_of_article)
            print(output_template)
        
            # write data out to CSV file
            writer.writerow({
                'title': title_of_article,
                'content': content,
                'link_to_resource': link_of_article,
                'published_date': date_of_article
            })

            
    print('Data written to CSV')
    print('Finished reading home page')

def _use_template(title, link, date):
    """
    Template string for output
    """
    return f"""Title = {title}
Link to resource = {link}
Published Date = {date}
"""


def _scrape_global_voices(url_to_scrape: str, title):
    """
    Used to scrape an article page from the Yoruba Global Voices blog
    """
    print(f'Fetching contents from {title}...')
    content = ''

    # Fetch the HTML content
    # https://yo.globalvoices.org/2023/01/11/1145/
    # https://yo.globalvoices.org/2023/02/01/1389/
    # https://yo.globalvoices.org/2023/01/11/1078/
    html_text = http.get(url_to_scrape).text

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_text, 'lxml')

    content_container = soup.find('div', class_='entry')
    content = str(content_container.text)

    print(f'Extracted data from {title}')
    return content