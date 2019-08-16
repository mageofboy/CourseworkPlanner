from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import unicodedata
import pandas as pd
import json 
import re

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


    def check_major_id(self, tag):
        valid_ids = ['majorrequirementstexttab','majorrequirementsbstexttab','majorrequirementsbatexttab','majorrequirementsbsdegreetexttab','majorrequirementsbadegreetexttab']
        if tag.has_attr('id'):
            return tag['id'] in valid_ids
        else:
            return False


    def check_majorreq_id(self, tag):
        valid_ids = ['majorrequirementstextcontainer','majorrequirementsbstextcontainer','majorrequirementsbatextcontainer','majorrequirementsbsdegreetextcontainer','majorrequirementsbadegreetextcontainer']
        if tag.has_attr('id'):
            return tag['id'] in valid_ids
        else:
            return False


    def has_major(self):
        return self.homepage_html.find(self.check_major_id) != None 


    def has_minor(self):
        return self.homepage_html.find(id="minorrequirementstexttab") != None


    def get_major_requirements(self):
        major_html = self.homepage_html.find(self.check_majorreq_id)
        reqs = []
        for table in major_html.find_all('table', 'sc_courselist'):
            s = [x.parent for x in table.find_all('td', class_="codecol")]
            for row in s:
                req = unicodedata.normalize("NFKD", row.find('td', class_="codecol").text.strip())
                if "or " in req:
                    req = req[3:]
                title = row.find('td', class_="").text
                units = row.find('td', class_="hourscol").text if row.find('td', class_="hourscol") != None else "-1"
                if units == "":
                    try:
                        units = re.search(r"\[([\w\-]+)\]", title).groups()[0]
                    except:
                        units = "-1"
                    title = title.split('[')[0].strip()
                reqs.append({req:[title.strip(), units]})
        return reqs


    def get_minor_requirements(self):
        minor_html = self.homepage_html.find(id="minorrequirementstextcontainer")
        reqs = []
        for table in minor_html.find_all('table', 'sc_courselist'):
            s = [x.parent for x in table.find_all('td', class_="codecol")]
            for row in s:
                req = unicodedata.normalize("NFKD", row.find('td', class_="codecol").text.strip())
                if "or " in req:
                    req = req[3:]
                title = row.find('td', class_="").text
                units = row.find('td', class_="hourscol").text if row.find('td', class_="hourscol") != None else "-1"
                if units == "":
                    try:
                        units = re.search(r"\[(.+)\]", title).groups()[0]
                    except:
                        units = "-1"
                    title = title.split('[')[0].strip()
                reqs.append({req:[title, units]})
        return reqs


if __name__ == "__main__":
    result_dir = 'coursedata.json'
    raw_html = simple_get('http://guide.berkeley.edu/undergraduate/degree-programs/')
    html = BeautifulSoup(raw_html, 'html.parser')
    programs_html = html.select('li.program')
    programs = []
    for i in programs_html:
        programs.append(Program(i))

    program_name = []
    has_major = []
    major_req = []
    has_minor = []
    minor_req = []
    program_homepage = []


    for program in programs:
        program_name.append(program.getName())
        program_homepage.append(program.getHomepage())
        if program.has_major():
            has_major.append(True)
            major_req.append(program.get_major_requirements())
        else:
            has_major.append(False)
            major_req.append(None)
        if program.has_minor():
            has_minor.append(True)
            minor_req.append(program.get_minor_requirements())
        else:
            has_minor.append(False)  
            minor_req.append(None)   
    df = pd.DataFrame({'Name':program_name,'Homepage URL':program_homepage,'Has Major':has_major,'Has Minor':has_minor, 'Major Requirements': major_req,'Minor Requirements':minor_req})
    d = df.to_dict(orient='records')
    with open(result_dir, 'w', encoding='utf-8') as result_dir:
        json.dump(d,result_dir,ensure_ascii=False,indent=4)
