__author__ = 'Mike'

# Grab free Pack books

import requests
import os
from bs4 import BeautifulSoup

import re

email    = 'elio@capelati.com'
password = 'elicap123@'

form_url = 'https://www.packtpub.com/packt/offers/free-learning'
download_url = 'https://www.packtpub.com/ebook_download/'
file_types = ['pdf', 'epub', 'mobi']
markup_type='lxml'
BOOK_ID_REGEX='[0-9]{5}'
BOOK_NAME_REGEX='[0-9]{13}(-)?([a-zA-Z_])+'

def get_book_with_regex(url, regex):
    p = re.compile(regex)
    m = p.search(url)
    return m.group()

def claim_book(form_url, email, password):
    s = requests.Session()
    r = s.get(form_url)
    soup = BeautifulSoup(r.text, markup_type)

    form = soup.find(attrs={"name": "form_build_id"})
    if not form:
        print 'Cannot find login form'
        return

    payload = {
        'email': email,
        'password': password,
        'op': 'Login',
        'form_build_id': form.id,
        'form_id': 'packt_user_login_form'
    }
    headers = {
         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.116 Chrome/48.0.2564.116 Safari/537.36',
    }

    r = s.post(form_url, data = payload, headers = headers)
    soup = BeautifulSoup(r.text, markup_type)
    if soup.find('div', class_='error'):
        print 'Login failed'
        return

    url = soup.find('a', class_='twelve-days-claim')
    if not url:
        print 'Failed to find claim url'

    r = s.get('https://www.packtpub.com'+url['href'])

    if r.status_code == 200:
    
        print 'Success'
        
        #save pdf
        book_id = get_book_with_regex(url['href'], BOOK_ID_REGEX)
        for ftype in file_types:
            r = s.get(download_url+'/'+book_id+'/'+ftype)
            local_filename = get_book_with_regex(r.url, BOOK_NAME_REGEX) + "." + ftype
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024): 
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
            print 'Success Downloaded = ' + local_filename 
         
    else:
        print 'Error claiming book'

    # messages error


if __name__ == "__main__":
    claim_book(form_url, email, password)
