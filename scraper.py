# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
from requests_html import HTMLSession
import json,sys,time
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")


SCRAPERWIKI_DATABASE_NAME = 'data.sqlite'

base = 'https://mangakakalot.com/'



def mangalist():
    options={
        'type':'latest',
        'category':'all',
        'state':'all'
    }
    url=base+'/manga_list'
    session=HTMLSession()
    data=session.get(url,params=options)
    sel = 'body > div.container > div.main-wrapper > div.leftCol.listCol > div > div.panel_page_number > div.group_page > a.page_blue.page_last'
    list_range = data.html.find(sel,first=True).search('Last({})')[0]
    session.close()
    manga_data = {}
    for item in range(2):
        try:
            data = session.get(url,params=options)
            data.html.render()
        except Exception as e:
            print(e)
            print('Going to sleep')
            time.sleep(5)
        sel='body > div.container > div.main-wrapper > div.leftCol.listCol > div'
        manga_list = data.html.find(sel,first=True)
        for manga in manga_list.find('div.list-truyen-item-wrap'):
            detail = manga.find('a',first=True)
            manga_name = detail.attrs['title']
            print(f'Finding the details of {manga_name}')
            manga_data[manga_name] = {}
            manga_data['link']=detail.attrs['href']
            manga_data['icon']=detail.find('img',first=True).attrs['src']
    scraperwiki.sql.save(manga_data,table_name='manga_data')
