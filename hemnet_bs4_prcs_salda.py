import time
import re
from hemnet_bs4_mainclass import jsonimp
import requests
from bs4 import BeautifulSoup


# Class for returining requests and soups 
#------------------------------------------------------------------------------
class linkext:
    def __init__(self,url):
        self.url = url
    
    def soup (self):       
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        }
        basereq  = requests.get(self, headers = headers)
        return basereq
class linksoup(linkext):
    def soup(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        }
        basereq  = requests.get(self, headers = headers)
        basesoup = BeautifulSoup(basereq.text,'html.parser')
        return basesoup


# Extracting data from the Sitemap
#------------------------------------------------------------------------------


# Extracting the links of land types
url = 'https://www.hemnet.se/sitemap'

type_lst = linksoup.soup(url).find_all(href=re.compile("salda"))
typelinks = []
baseurl = 'https://www.hemnet.se'
for land in type_lst:
    link = land.get('href')

    typelinks.append(baseurl + link)
print(len(typelinks))
pagelst = []
for url in typelinks:
    for i in range(1,51):
        link = url + '/?page=' + str(i)
        pagelst.append(link)

print(len(pagelst))




# Scrapping raw data by parsing each link extracted
#------------------------------------------------------------------------------

data = []
startarea = time.time()
for link in pagelst:
    hits = linksoup.soup(link).find_all("li",{
            'class':"sold-results__normal-hit"})
    page_type= linksoup.soup(link).find("div",{
        'class':"small-results-header__filters"}).text.replace('/n',"")      
    for hit in hits:
        
        try:
            name=hit.find("span",{
                'class':"item-result-meta-attribute-is-bold item-link qa-selling-price-title"}).text.replace('\n',"")
            name = name.strip()
        except:
            name = 'No Info'
            
        try:
            price=hit.find("span",{
                'class':"sold-property-listing__subheading sold-property-listing--left"}).text.replace('\n',"")
        except:
            price = 0
                
        try:
            area_room=hit.find("div",{
                'class':"sold-property-listing__subheading sold-property-listing--left"}).text.replace('/n',"")
        except Exception:
            try:
                area_room=hit.find("div",{
                    'class':"sold-property-listing__subheading"}).text.replace('/n',"")                             
            except:
                area_room = 0
            
        try:
            loc_upclass=hit.find("div",{
                'class':"sold-property-listing__location"})
            for i in loc_upclass():
                loc = loc_upclass.find("div").text.replace('/n',"")
        except:
            loc = 'No Info'  


        try:
            item_url=hit.find('a', href=True)['href']
            
        except:
            item_url = 'No Info'

            
        try:
            item_type= page_type
        except:
            item_type = 'No Info'

            
        hem_details = {"title":name ,"price":price, "area_room":area_room ,
                       'city_kommun':loc,'url':item_url,'type':item_type,
                       'land_enc':'', 'type_enc':''}

        data.append(hem_details)
        

print ('data scrapping time is:', time.time() - startarea)
jsonimp(data, 'datajson.txt')

