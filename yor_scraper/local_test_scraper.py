from bs4 import BeautifulSoup
from pathlib import Path


def try_scraping():
    """
    Used for scraping
    """
    absolute_path = Path('.').resolve() / "yor_scraper/yor_test/home.html"
    print(f'Absolute Path = {absolute_path}')


    # read file
    with open(str(absolute_path), 'r') as html_file:
        content = html_file.read()

        soup = BeautifulSoup(content, 'lxml')

        # get information you need
        # get all h5-tags 
        courses_cards = soup.find_all('div', class_='card-body')
        for course in courses_cards:
          course_name = course.h5.text
          course_price = str(course.a.text).replace('Start for ', '')

          print(f'{course_name} costs {course_price}')