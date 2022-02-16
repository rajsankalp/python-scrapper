from audioop import add
from django.http.response import HttpResponse
from django.shortcuts import render

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from scraper.models import Decorations,Images
from scraper.models import Buss
from django.db.models import Max
import datetime
import urllib
import os
from django.conf import settings
import random
import re
#from scraper.serializers import DecorationSerializer
#from rest_framework.response import Response
#from rest_framework.decorators import api_view

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By

import json

def index(request):

    driver_location = "/usr/bin/chromedriver"
    binary_location = "/usr/bin/google-chrome"
    options = webdriver.ChromeOptions()
    options.binary_location = binary_location
    options.add_argument("--headless")
    options.add_argument('--no-sandbox') 
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")       
    # options.add_argument("--start-maximized") #open Browser in maximized mode
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument("--no-sandbox") #bypass OS security model
    # options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)   

    # selenium = webdriver.Chrome("/usr/local/bin/chromedriver")


    land = request.GET['land']

    selenium = webdriver.Chrome(executable_path=driver_location,chrome_options=options)
 

    max_row = Buss.objects.filter(land=land).order_by('-page_num').all()[:1]

    # return HttpResponse(max_row.query)

    if max_row:
        page_num = int(max_row[0].page_num) + 1
    else:
        page_num = 1   


    url = 'https://www.tierheim-verzeichnis.com/verzeichnis/tierheime/bundeslaender?land='+ str(land)

    print(url)

    # return HttpResponse(page_num)

    #Choose your url to visit
    selenium.get(url)

    # selenium.implicitly_wait(10)

    # decoration_links = WebDriverWait(selenium, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.hz-photo-card__ratio-box')))

    # print(url)

    decoration_links = selenium.find_elements_by_css_selector("ul.list-by-state li a")
    # decoration_links = selenium.find_elements_by_class_name("a.hz-photo-card__ratio-box")

    


    for decoration_link in decoration_links:

        

        if decoration_link:
            # print(decoration_link.get_attribute('href')) 
            link_url = decoration_link.get_attribute('href')

            print(link_url)
            # splitted = link_url.split('~')
            url_exist = Buss.objects.filter(url__contains=link_url)[:1]
            if not url_exist:
                Buss.objects.create(url=link_url,status=0,land=land)    
          

    selenium.quit()
    return HttpResponse("It works!")





def profile(request):

    driver_location = "/usr/bin/chromedriver"
    binary_location = "/usr/bin/google-chrome"
    options = webdriver.ChromeOptions()
    options.binary_location = binary_location
    options.add_argument("--headless")
    options.add_argument('--no-sandbox') 
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")       
    # options.add_argument("--start-maximized") #open Browser in maximized mode
    options.add_argument('--disable-dev-shm-usage')




    selenium = webdriver.Chrome(executable_path=driver_location,chrome_options=options)
 

    row = Buss.objects.filter(status=0).order_by('-page_num').all()[:1]

    title = ''
    email = ''
    phone = ''
    website = ''
    address = '' 
    lat_long = ''
    latitude = 0
    longitude = 0

    # return HttpResponse(row[0].url) 
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    

    if row:
        # print(row[0].url)

        profile_url = row[0].url

        # profile_url = "https://www.tierheim-verzeichnis.com/verzeichnis/tierheime/tierheim-frstenberg"

        selenium.get(profile_url)
        title_line = selenium.find_elements_by_css_selector(".content__inner__column--main h2")
        if(title_line):
            title = title_line[0].text

        other_info = selenium.find_elements_by_css_selector(".content__inner__column--main p")

        if(other_info):
            description = other_info[0].text
            address = other_info[1].text      

        contact_info_raw = selenium.find_elements_by_css_selector(".content__inner__column--main table td") 
        contact_info_absolute_raw = selenium.find_elements_by_css_selector(".content__inner__column--main table") 

        script_raw = selenium.find_elements_by_css_selector(".content__inner__column script") 

        if(contact_info_raw):

            if(contact_info_raw[0]):

                urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', contact_info_absolute_raw[0].text) 
                if(urls):
                    website = urls[0] 

                emails = re.findall('\S+@\S+', contact_info_absolute_raw[0].text) 
                if(emails):
                    email = emails[0]

                phones = re.findall('\S+ - \S+ \S+', contact_info_absolute_raw[0].text) 
                if(phones):
                    phone = phones[0] 
                    phone = contact_info_raw[0].text

                if(script_raw and script_raw[0]):

                    #Grab lat long from script tag 
                    lat_long = re.findall('\[\S+, \S+\]', script_raw[1].get_attribute("innerHTML")) 

                    if(lat_long):
                        lat_long_string =  lat_long[0]
                        lat_long_string = lat_long_string.replace("[","")
                        lat_long_string = lat_long_string.replace("]","")
                        lat_long_string = lat_long_string.replace(" ","")
                        lat_long_array = lat_long_string.split(',')

                        latitude = lat_long_array[0]
                        longitude = lat_long_array[1]

                        # print(lat_long_array[0]) 
                        # print(lat_long_array[1]) 




        business = row[0]
        business.email = email
        business.title = title
        business.description = description
        business.phone = phone
        business.address = address
        business.status = 1
        business.website = website
        business.latitude = latitude
        business.longitude = longitude
        business.updated_at = datetime.datetime.now()
        business.save()

          
    selenium.close()
    selenium.quit()
    
    return HttpResponse("Working!") 




def link2(request):

    driver_location = "/usr/bin/chromedriver"
    binary_location = "/usr/bin/google-chrome"
    options = webdriver.ChromeOptions()
    options.binary_location = binary_location
    options.add_argument("--headless")
    options.add_argument('--no-sandbox') 
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")       
    # options.add_argument("--start-maximized") #open Browser in maximized mode
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument("--no-sandbox") #bypass OS security model
    # options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)   

    # selenium = webdriver.Chrome("/usr/local/bin/chromedriver")


    city = request.GET['city']
    area = request.GET['area']
    min_max = request.GET['min_max']

    selenium = webdriver.Chrome(executable_path=driver_location,chrome_options=options)
 

    max_row = Buss.objects.filter(city=city).order_by('-page_num').all()[:1]

    # return HttpResponse(max_row.query)

    if max_row:
        page_num = int(max_row[0].page_num) + 1
    else:
        page_num = 1   


    url = 'https://www.tierarzt-onlineverzeichnis.de/tieraerzte/'+area+'/'+city+'/'+min_max+'/'+ str(page_num)+'/'

    print(url)

    # return HttpResponse(page_num)

    #Choose your url to visit
    selenium.get(url)

    # selenium.implicitly_wait(10)

    # decoration_links = WebDriverWait(selenium, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.hz-photo-card__ratio-box')))

    # print(url)

    decoration_links = selenium.find_elements_by_css_selector(".arzt-ergebnis .arzt-ergebnis-box a")
    # decoration_links = selenium.find_elements_by_class_name("a.hz-photo-card__ratio-box")

    


    for decoration_link in decoration_links:

        

        if decoration_link:
            # print(decoration_link.get_attribute('href')) 
            link_url = decoration_link.get_attribute('href')

            print(link_url)
            # splitted = link_url.split('~')
            url_exist = Buss.objects.filter(url__contains=link_url)[:1]
            if not url_exist:
                Buss.objects.create(url=link_url,status=0,page_num=page_num,city=city)    
          

    selenium.quit()
    return HttpResponse("It works!")    




def profile2(request):

    driver_location = "/usr/bin/chromedriver"
    binary_location = "/usr/bin/google-chrome"
    options = webdriver.ChromeOptions()
    options.binary_location = binary_location
    options.add_argument("--headless")
    options.add_argument('--no-sandbox') 
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")       
    # options.add_argument("--start-maximized") #open Browser in maximized mode
    options.add_argument('--disable-dev-shm-usage')




    selenium = webdriver.Chrome(executable_path=driver_location,chrome_options=options)
 

    row = Buss.objects.filter(status=0,url__startswith='https://www.tierarzt-onlineverzeichnis.de').order_by('-page_num').all()[:1]

    title = ''
    description = ''
    email = ''
    phone = ''
    mobile = ''
    website = ''
    address = '' 
    lat_long = ''
    latitude = 0
    longitude = 0

    # return HttpResponse(row[0].url) 
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    

    if row:
        # print(row[0].url)

        profile_url = row[0].url

   
        
        selenium.get(profile_url)
        title_line = selenium.find_elements_by_css_selector("#top_main_box .do_adresse h1")
        if(title_line):
            title = title_line[0].text

        other_info = selenium.find_elements_by_css_selector("#top_main_box .do_adresse h2")

        if(other_info):
            description = other_info[0].text
        
        address_info = selenium.find_elements_by_css_selector("#top_main_box .do_adresse p")

        if(address_info):
            address = address_info[0].get_attribute('innerHTML')  



        contact_info_raw = selenium.find_elements_by_css_selector("#top_main_box .do_adresse dl dd") 
        if(contact_info_raw):
            phone = contact_info_raw[0].text 

        if(contact_info_raw):
            mobile = contact_info_raw[1].text          

        email_info = selenium.find_elements_by_css_selector("#top_main_box .do_adresse dl")                    

        if(email_info):

            emails = re.findall('\S+@\S+', email_info[0].text) 
            if(emails):
                email = emails[0]            

            urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', email_info[0].text) 
            if(urls):
                website = urls[0] 

 



        script_raw = selenium.find_elements_by_css_selector("#content script")             

        if(script_raw and script_raw[1]):

            #Grab lat long from script tag 
            lat_long = re.findall('\[\S+,\S+\]', script_raw[1].get_attribute("innerHTML")) 

            if(lat_long):
                lat_long_string =  lat_long[0]
                lat_long_string = lat_long_string.replace("[","")
                lat_long_string = lat_long_string.replace("]","")
                lat_long_string = lat_long_string.replace(" ","")
                lat_long_array = lat_long_string.split(',')

                latitude = lat_long_array[0]
                longitude = lat_long_array[1]

                # print(lat_long_array[0]) 
                # print(lat_long_array[1]) 




        business = row[0]
        business.email = email
        business.title = title
        business.description = description
        business.phone = phone
        business.mobile = mobile
        business.type = "Tierarztpraxis"
        business.address = address
        business.status = 1
        business.website = website
        business.latitude = latitude
        business.longitude = longitude
        business.updated_at = datetime.datetime.now()
        business.save()

          
    selenium.close()
    selenium.quit()
    
    return HttpResponse("Working!") 




def index3(request):

    driver_location = "/usr/bin/chromedriver"
    binary_location = "/usr/bin/google-chrome"
    options = webdriver.ChromeOptions()
    options.binary_location = binary_location
    options.add_argument("--headless")
    options.add_argument('--no-sandbox') 
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")       
    # options.add_argument("--start-maximized") #open Browser in maximized mode
    options.add_argument('--disable-dev-shm-usage')




    selenium = webdriver.Chrome(executable_path=driver_location,chrome_options=options)
 

    max_row = Buss.objects.filter(url__icontains='www.tieraerzteverband.de').order_by('-page_num').all()[:1]

    # return HttpResponse(max_row.query)

    if max_row:
        page_num = int(max_row[0].page_num) + 1
    else:
        page_num = 1   


    url = 'https://www.tieraerzteverband.de/bpt/ueber-den-bpt/mitgliedersuche/?animals%5B%5D=1&p='+str(page_num)

    print(url)

    # return HttpResponse(page_num)

    #Choose your url to visit
    selenium.get(url)

    doctor_elements = selenium.find_elements_by_css_selector("#elementContentOverflow .elementList div.mgStyle")

 



    for doctor_element in doctor_elements:

        title = ""
        description = ""
        address = ""
        phone = ""
        fax = ""
        email = ""
        website = ""
        latitude = 0
        longitude = 0
        city = ""
        zip = ""
        addresss_text = ""
        tags = ""

        id = doctor_element.get_attribute('id')

        name_element = selenium.find_element_by_css_selector("#elementContentOverflow .elementList #"+id+" .headline h2")
        if(name_element):
            title = name_element.text

        address_element = selenium.find_element_by_css_selector("#elementContentOverflow .elementList #"+id+" .elementContent .col1 div")
        if(address_element):
            description_html = address_element.get_attribute("innerHTML")       
            addresss_text = address_element.text
            splitted_description = description_html.split('<br><br>')

            if(len(splitted_description) > 1):
                description = splitted_description[0].strip()
                address = splitted_description[1].strip()
                
                address.replace('<div class="clearBoth">&nbsp;</div>','')
                # address.replace('<br>',' ')
            else:
                address = description_html 


        phone_element = selenium.find_elements_by_css_selector("#elementContentOverflow .elementList #"+id+" .elementContent .col2 a.phone")
        if(phone_element):
            phone = phone_element[0].text   



        email_element = selenium.find_elements_by_css_selector("#elementContentOverflow .elementList #"+id+" .elementContent .col2 a.wpst")
        if(email_element):
            email = email_element[0].get_attribute('href') 
            email = email.replace('mailto:','')

        web_element = selenium.find_elements_by_css_selector("#elementContentOverflow .elementList #"+id+" .elementContent .col2 a.www")
        if(web_element):
            website = web_element[0].get_attribute('href') 
            if(website=="http:"): 
                website = ""


        script_raw = selenium.find_elements_by_css_selector("#elementContentOverflow .elementList #"+id+" .elementOpenStreetMapStyler_var0 script")             

        if(script_raw and script_raw[0]):

            #Grab lat long from script tag 
            latitude_raw = re.findall('latitude = \'\S+\'', script_raw[0].get_attribute("innerHTML")) 
            longitude_raw = re.findall('longtitude = \'\S+\'', script_raw[0].get_attribute("innerHTML"))  

            if(latitude_raw):
                lat_string =  latitude_raw[0]
                lat_string = lat_string.replace("latitude = '","")
                lat_string = lat_string.replace("'","")
                latitude = lat_string.replace(" ","")
                

            if(longitude_raw):
                long_string =  longitude_raw[0]
                long_string = long_string.replace("longtitude = '","")
                long_string = long_string.replace("'","")
                longitude = long_string.replace(" ","")              

        fresh_tags = []
        tag_elements = selenium.find_elements_by_css_selector("#elementContentOverflow .elementList #"+id+" .elementContent .col3 .checkbox")    

        if(tag_elements):
            for tag_element in tag_elements:
                new = tag_match(tag_element.text)
                if(new):
                    fresh_tags.append(new) 
            s = ";"
            tags = s.join(fresh_tags) 

        if(addresss_text):
            zip_raw = addresss_text.split(" ")       
            zip_only =  zip_raw[-2:]

            if(zip_only and len(zip_only) > 1):
                exploded_zip = zip_only[0].split('\n')

                if(exploded_zip and len(exploded_zip)==2):
                    zip = exploded_zip[1]
                    city =  zip_only[1]   





        Buss.objects.create(title=title,description=description,url='https://www.tieraerzteverband.de/'+id,page_num=page_num,address=address,email=email,phone=phone,status=1,website=website,latitude=latitude,longitude=longitude,city=city,zip=zip,tags=tags,updated_at=datetime.datetime.now()) 


    selenium.quit()
    return HttpResponse("It works!")  




def tierheim_gesucht_link_crawler(request):

    driver_location = "/usr/bin/chromedriver"
    binary_location = "/usr/bin/google-chrome"
    options = webdriver.ChromeOptions()
    options.binary_location = binary_location
    options.add_argument("--headless")
    options.add_argument('--no-sandbox') 
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")       
    # options.add_argument("--start-maximized") #open Browser in maximized mode
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument("--no-sandbox") #bypass OS security model
    # options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)   

    # selenium = webdriver.Chrome("/usr/local/bin/chromedriver")


    # city = request.GET['city']
    # area = request.GET['area']
    # min_max = request.GET['min_max']

    selenium = webdriver.Chrome(executable_path=driver_location,chrome_options=options)
    web_name = 'tierheim-gesucht.de'

    max_row = Buss.objects.filter(url__contains=web_name).order_by('-page_num').all()[:1]

    # return HttpResponse(max_row.query)

    if max_row:
        page_num = int(max_row[0].page_num) + 1
    else:
        page_num = 1   


    url = 'https://www.tierheim-gesucht.de/tierheime-in-der-naehe/seite-'+str(page_num)

    print(url)

    # return HttpResponse(page_num)

    #Choose your url to visit
    selenium.get(url)

    # selenium.implicitly_wait(10)

    # decoration_links = WebDriverWait(selenium, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.hz-photo-card__ratio-box')))

    # print(url)

    decoration_links = selenium.find_elements_by_css_selector("a.box_topic")
    # decoration_links = selenium.find_elements_by_class_name("a.hz-photo-card__ratio-box")

    


    for decoration_link in decoration_links:

        if decoration_link:
            # print(decoration_link.get_attribute('href')) 
            link_url = decoration_link.get_attribute('href')
            # splitted = link_url.split('~')
            url_exist = Buss.objects.filter(url__contains=link_url)[:1]
            if not url_exist:
                Buss.objects.create(url=link_url,status=0,page_num=page_num)

                print("--------------")
                print(link_url)   
                print("--------------") 

    selenium.quit()
    return HttpResponse("It works!")    



def tierheim_gesucht_detail_crawler(request):

    driver_location = "/usr/bin/chromedriver"
    binary_location = "/usr/bin/google-chrome"
    options = webdriver.ChromeOptions()
    options.binary_location = binary_location
    options.add_argument("--headless")
    options.add_argument('--no-sandbox') 
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")       
    # options.add_argument("--start-maximized") #open Browser in maximized mode
    options.add_argument('--disable-dev-shm-usage')




    selenium = webdriver.Chrome(executable_path=driver_location,chrome_options=options)
 

    row = Buss.objects.filter(url__icontains='www.tierheim-gesucht.de',status=0).order_by('-page_num').all()[:1]

    title = ''
    email = ''
    phone = ''
    mobile = ''
    website = ''
    address = '' 
    lat_long = ''
    latitude = 0
    longitude = 0
    zip = ""
    city = ""
    description = ""
    facebook = ""
    organization_name = ""
    donation_detail = ""
    availablity_json = ""

    # return HttpResponse(row[0].url) 
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    
    

    if row:
        # print(row[0].url)

        profile_url = row[0].url
        print(profile_url)

        # profile_url = "https://www.tierheim-verzeichnis.com/verzeichnis/tierheime/tierheim-frstenberg"

        selenium.get(profile_url)
        title_line = selenium.find_elements_by_css_selector(".margin_30_40 .singlepost h2")
        if(title_line):
            title = title_line[0].text

        org_name_line = selenium.find_elements_by_css_selector(".page_header h1")  

        if(org_name_line):
            organization_name = org_name_line[0].text  

        address_info = selenium.find_elements_by_css_selector(".margin_30_40 .singlepost .row div:nth-child(2) p")

        

        if(address_info and len(address_info) > 1):
            address = address_info[1].get_attribute("innerHTML")  

            zip_raw = address_info[1].get_attribute("innerHTML").split("<br>") 
                  
            zip_only =  zip_raw[-1:]
           
            
            
            if(zip_only):
                zip_only = zip_only[0].strip()

                exploded_zip = zip_only.split(' ')

                if(exploded_zip and len(exploded_zip)==2):
                    zip = exploded_zip[0]
                    city =  exploded_zip[1]             



        contact_info_raw = selenium.find_elements_by_css_selector(".margin_30_40 .singlepost .row > div:nth-child(3)") 
        contact_info_raw_phone = selenium.find_elements_by_css_selector(".margin_30_40 .singlepost .row div:nth-child(3) p")
        contact_info_raw_website = selenium.find_elements_by_css_selector(".margin_30_40 .singlepost .row div:nth-child(3) p > a[target=_blank]") 

        if(contact_info_raw):

            if(contact_info_raw[0]):

                emails = re.findall('\S+@\S+', contact_info_raw[0].text) 
                if(emails):
                    email = emails[0]

        
        if(contact_info_raw_website):        
            # urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', contact_info_raw_website[0].get_attribute('href')) 
            website = contact_info_raw_website[0].get_attribute('href') 

        # Get Facebook Link

        if(contact_info_raw_website):

            for web_link in contact_info_raw_website:
                
                if(web_link.get_attribute('href').find('facebook.com') > 0):
                    facebook = web_link.get_attribute('href') 




        if(contact_info_raw_phone):
            # phones = re.findall('\S+ - \S+ \S+', contact_info_raw_phone[0].text) 
            phone = contact_info_raw_phone[0].text

            if(phone):
                if(phone[0:2]=="01"):
                    mobile = phone
                    phone = ""
                else:
                    mobile = ""   


                
        found_elements = selenium.find_elements_by_css_selector(".margin_30_40 .row .singlepost") 

        if(found_elements):
            for found_element in found_elements:
 
                if(found_element.text.find("Spendenkonto") >= 0):

                    raw_element = found_element.find_elements_by_tag_name('p')

                    if(raw_element):

                        donation_detail = raw_element[1].get_attribute("innerHTML") 


        # Grab working hours

        working_days_elements = selenium.find_elements_by_css_selector("table.RespTable thead > tr > th")
        working_time_elements = selenium.find_elements_by_css_selector("table.RespTable tbody > tr > td")

        day_list = {
            "Montag" : "Monday",
            "Dienstag" : "Tuesday",
            "Mittwoch" : "Wednesday",
            "Donnerstag" : "Thursday",
            "Freitag" : "Friday",
            "Samstag" : "Saturday",
            "Sonntag" : "Sunday",  
        }

        available_dates = []
        if(working_days_elements):
            for working_days_element in working_days_elements:
                # if(day_list.get(working_days_element.text) is not None):
                available_dates.append(working_days_element.text)

        initial_v = 0
        final_dictionary = {}
        if(working_time_elements):
            initial_v = 0
            for working_time_element in working_time_elements:
                final_dictionary[available_dates[initial_v]]= working_time_element.text
                initial_v += 1 
                
            availablity_json = json.dumps(final_dictionary)        











        # print(email)
        # print(website)
        # print(f'facebook: {facebook}')
        # print(f'phone: {phone}')
        # print(f'mobile: {mobile}')
        # print("-------------------")
        # print(f'Donation Detail: {donation_detail}')
        # return HttpResponse("Reached")


        business = row[0]
        business.email = email
        business.title = title
        business.description = description
        business.phone = phone
        business.mobile = mobile
        business.address = address
        business.status = 1
        business.website = website
        business.facebook = facebook
        business.organization_name = organization_name
        business.latitude = latitude
        business.longitude = longitude
        business.zip = zip
        business.city = city
        business.availablity_json = availablity_json
        business.donation_detail = donation_detail
        business.updated_at = datetime.datetime.now()
        business.save()

          
    selenium.close()
    selenium.quit()
    
    return HttpResponse("Working!")   



def tag_match(tag):

    tags = {
        "Pferde" : "Pferdepraxis",
        "Reptilien" : "Reptilien",
        "Kleine Heimtiere" : "Kleintierpraxis",
        "Zierfische" : "Fische",
        "Kleine Ziervögel" : "Vögel",
        "Papageien" : "Papageien",
        "Hunde" : "Hunde",
        "Katze" : "Katze",
    }

    for key,value in tags.items():
        if(key==tag):
            return tags[key]
    return ''        

