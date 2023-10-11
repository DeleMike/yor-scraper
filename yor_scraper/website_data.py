class WebsiteData: 
    """
    Summary
    ------
    This is a data class to hold the name and link of the website to be scraped
    """
    name: str
    link: str
    csv_path_name: str

    def __init__(self, name, link, csv_path_name=''):
        self.name =  name
        self.link = link
        self.csv_path_name = csv_path_name

    def __str__(self):
        return f"{{'name':'{self.name}', 'link':'{self.link}', 'csv_path_name':'{self.csv_path_name}'}}"
