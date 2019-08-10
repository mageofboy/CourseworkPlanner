from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)



class Program:
    def __init__(self, program):
        self.program = program
        self.name = self.program.text[:-10]
        self.homepage = "http://guide.berkeley.edu/undergraduate/degree-programs/" + self.program.select('a.pview')[0]['href']
        raw_html = simple_get(self.homepage)
        html = BeautifulSoup(raw_html, 'html.parser')
        self.homepage_html = html

    def getName(self):
        return self.name

    def getHomepage(self):
        return self.homepage

    def has_major(self):
        return self.homepage_html.find(id="majorrequirementstexttab") != None


    def has_minor(self):
        return self.homepage_html.find(id="minorrequirementstexttab") != None

    # def program_major_html(self):
    #     if self.has_major():
    #         major = self.homepage + "#majorrequirementstext"
    #         raw_html = simple_get(major)
    #         html = BeautifulSoup(raw_html, 'html.parser')
    #         return html
    #     else:
    #         return None

    # def program_minor_html(self):
    #     if self.has_major():
    #         minor = self.homepage + "#minorrequirementstext"
    #         raw_html = simple_get(minor)
    #         html = BeautifulSoup(raw_html, 'html.parser')
    #         return html
    #     else:
    #         return None


    def get_major_requirements(self):
        for table in self.homepage_html.find_all('table', 'sc_courselist'):
            for row in table.find_all('tr'):
                for i in row.find_all('td'):
                    print(i.text)
        
    def get_minor_requirements(self):
        html = self.program_minor_html()


if __name__ == "__main__":
    raw_html = simple_get('http://guide.berkeley.edu/undergraduate/degree-programs/')
    html = BeautifulSoup(raw_html, 'html.parser')
    programs_html = html.select('li.program')
    programs = []
    major_programs = []
    minor_programs = []
    for i in programs_html[:2]:
        programs.append(Program(i))

    for program in programs:
        if program.has_major():
            major_programs.append(program.name)
        if program.has_minor():
            minor_programs.append(program.name)
    programs[1].get_major_requirements()

