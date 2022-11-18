import json
import math
import time
from datetime import datetime, timedelta
import random
from bs4 import BeautifulSoup
from lxml import etree
import lxml.html

import numpy as np
import pandas as pd
import requests
from random_user_agent.params import OperatingSystem, SoftwareName
from random_user_agent.user_agent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def get_reviews_count(driver, url, upd_per_count):
    x = 'def get_reviews_count'

    if upd_per_count:
        HEADERS = ({
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-User": "?1",
                    "Sec-Fetch-Dest": "document",
                    "Referer": "https://www.google.com/",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.9"
                    })

        webpage = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
        dom = etree.HTML(str(soup))
        r_count = dom.xpath('//span[@class="reviews_header_count"]/text()')
        r_count = int(r_count[0][1:-1])
    else:
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//span[@class="reviews_header_count"]')))
            r_count = driver.find_element(By.XPATH, '//span[@class="reviews_header_count"]').text
            r_count = int(r_count[1:-1])
            # print(r_count)
        except Exception as e:
            print('\n   ---->Problem with '+x+'\n        '+str(datetime.now()))
            err = 0

    return r_count

url = 'https://www.tripadvisor.com/Restaurant_Review-g303506-d9969088-Reviews-Vezpa_Pizzas_Tijuca-Rio_de_Janeiro_State_of_Rio_de_Janeiro.html'
print(get_reviews_count('1', url, True))




def open_page_list(driver, try_err):
        #timeout de 20s em cada click e vai rodar por 10 tentativas// quanto menor o time.sleep() mais erros //  
        err = 0
        cont = 1
        print('   Trying to open page #'+str(cont))
        while err == 0 and cont<=try_err:
            err = 1
            cont+=1

            x = 'All languages Click'
            try:
                elmnt = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@data-tracker="All languages"]')))
                elmnt.click()
            except Exception as e:
                print('\n   ---->Problem with '+x+'\n        '+str(datetime.now()))
                err = 0
            time.sleep(1)

            x = 'Most Recent Click'
            try:
                elmnt = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sort-by"]/option[1]')))
                elmnt.click()
            except Exception as e:
                print('\n   ---->Problem with '+x+'\n        '+str(datetime.now()))
                err = 0
            time.sleep(1)

            x = 'ShowMore Click'
            try:
                elmnt = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'taLnk.ulBlueLinks')))
                elmnt.click()
                show_less = WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'taLnk.ulBlueLinks'), 'Show less'))
                if show_less == False:
                    err = 0     
            except Exception as e:
                print('\n   ---->Problem with '+x+'\n        '+str(datetime.now()))
                err = 0
            time.sleep(0.5)

            x = 'random click bait'
            try:
                vet_click = [
                                WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.CLASS_NAME, 'title_text'))),
                                WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="prw_rup prw_filters_query_resp"]//div[@class="title"]'))),
                                WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//span[@class="reviews_header_count"]'))) 
                ]
                elmnt = random.choice(vet_click)
                elmnt.click()
                # print('Random click ok')
            except Exception as e:
                print('\n   ---->Problem with '+x+'\n        '+str(datetime.now()))
                err = 0
            
        print('   Openned '+str(datetime.now())+'\n\n')

def switch_page(driver, j):
    on_right_page = 0
    try_err = 5
    err = 0
    cont = 1

    while err == 0 and cont<=try_err:
        err = 1
        cont+=1

        # print(driver.current_url)

        x = 'switch_page'
        if on_right_page == 0:
            try:
                elmnt = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[@data-page-number='+str(j)+']')))
                elmnt.click()
            except Exception as e:
                print('\n   ---->Problem with '+x+'\n        '+str(datetime.now()))
            time.sleep(1)

            curr_url = driver.current_url
            st1 = curr_url[curr_url.find('Reviews-or')+10:curr_url.find('Reviews-or')+14]
            st2 = int(st1[:st1.find('-')])
            page = st2/15 + 1
            if page == j:
                on_right_page = 1
            else: 
                on_right_page = 0
                err = 0

        x = 'random click bait in switch page'
        try:
            vet_click = [
                            WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.CLASS_NAME, 'title_text'))),
                            WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//span[@data-options="autoReposition"]'))), 
                            WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="prw_rup prw_filters_query_resp"]//div[@class="title"]'))),
                            WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//span[@class="reviews_header_count"]'))) 
            ]
            elmnt = random.choice(vet_click)
            elmnt.click()
        except Exception as e:
            print('\n   ---->Problem with '+x+'\n        '+str(datetime.now()))

        x = 'pass all languages bait'
        # checked="checked"
        try:
            checkBoxElement = driver.find_element(By.XPATH, '//div[@data-tracker="English"]//input[@name="filters_detail_language_filterLang_0"]').get_attribute("checked")
            if checkBoxElement == True:
                print('---->Problem with '+x)
                elmnt = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@data-tracker="All languages"]')))
                elmnt.click()
                time.sleep(0.2)
                elmnt = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@data-tracker="English"]')))
                elmnt.click() 
                elmnt = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@data-tracker="All languages"]')))
                elmnt.click()

        except Exception as e:
            print('\n   ---->Problem with '+x+'\n        '+str(datetime.now()))
            err = 0
        # time.sleep(1)

        x = 'ShowMore Click in switch page'
        try:
            elmnt = WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.CLASS_NAME, 'taLnk.ulBlueLinks')))
            elmnt.click()
            show_less = WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'taLnk.ulBlueLinks'), 'Show less'))
            if show_less == False:
                err = 0
        except Exception as e:
            print('\n   ---->Problem with '+x+'\n        '+str(datetime.now()))
            err = 0
        # time.sleep(1)

def adjust_date(date):
    try:
        try:
            formated_date = pd.to_datetime(date, dayfirst=True).date()
        except:
            if date.find('yester')>=0:
                delta = timedelta(days = 1)
            elif date.find('today')>=0:
                delta = timedelta(days = 0)
            elif date.find('day')>=0:
                dt = int(date[:-9])
                delta = timedelta(days = dt)
            elif date.find('weeks')>=0:
                dt = int(date[:-10])
                delta = timedelta(weeks = dt)
            elif date.find('week')>=0:
                dt = int(date[:-9])
                delta = timedelta(weeks = dt)

            tod = datetime.today()
            a = tod - delta
            formated_date = pd.to_datetime(a, dayfirst=True).date()
    except:
        formated_date = date

    return formated_date

def get_single_review(driver, n):
    x = 'access class review-container' #'review-container' 
    try:
        user = driver.find_element(By.XPATH, '(//div[@class="review-container"])['+str(n)+']//div[@class="info_text pointer_cursor"]//div[1]').text
        print(user)
    except:
        user = ''
        # print('user not found')

    try:
        userloc = driver.find_element(By.XPATH, '(//div[@class="review-container"])['+str(n)+']//div[@class="info_text pointer_cursor"]//div[@class="userLoc"]').text
        # print(userloc)
    except:
        userloc = ''
        # print('userloc not found')

    try:
        try:
            n_reviews = driver.find_element(By.XPATH, '(//div[@class="review-container"])['+str(n)+']//div[@class="memberBadgingNoText is-shown-at-tablet"]//span[@class="badgetext"]').text
            n_reviews = int(n_reviews)
            # print(n_reviews)
        except: 
            n_reviews = driver.find_element(By.XPATH, '(//div[@class="review-container"])['+str(n)+']//div[@class="reviewerBadge badge"]//span[@class="badgeText"]').text
            n_reviews = int(n_reviews[:-8])
            # print(n_reviews)
    except:
        n_reviews = ''
        # print('n_reviews not found')

    try:
        title = driver.find_element(By.XPATH, '(//div[@class="review-container"])['+str(n)+']//span[@class="noQuotes"]').text
        # print(title)
    except:
        title = ''
        # print('title not found')

    try:
        link_review = driver.find_element(By.XPATH, '(//div[@class="review-container"])['+str(n)+']//div[@class="quote"]//a').get_attribute('href')
        # print(link_review)
    except:
        link_review = ''
        # print('link_review not found')
    
    try:
        id_review = driver.find_element(By.XPATH, '(//div[@class="review-container"])['+str(n)+']//div[@class="quote"]//a').get_attribute('id')
        id_review = int(id_review[2:])
        # print(id_review)
    except:
        try:
            id_review = driver.find_element(By.XPATH, '(//div[@class="review-container"])['+str(n)+']//div[@class="quote isNew"]//a').get_attribute('id')
            id_review = int(id_review[2:])
            # print(id_review)
        except:
            id_review = ''
            # print('id_review not found')

    try:
        try:
            tradutor = driver.find_element(By.XPATH, '(//div[@class="review-container"])['+str(n)+']//div[@class="prw_rup prw_reviews_google_translate_button_hsx"]')
            posic = 3
        except:
            posic = 2
        text = driver.find_element(By.XPATH, '(//div[@class="review-container"])['+str(n)+']//div/div/div/div[2]/div['+str(posic)+']/div/p').text
        # print(text)
    except:
        text = ''
        # print('text not found')

    try:
        score = driver.find_element(By.XPATH, '(//div[@class="review-container"])['+str(n)+']//div/div/div/div[2]/span[1]')
        score_class = score.get_attribute("class")
        score = int(score_class[-2])
        # print(score)
    except:
        score = ''
        # print('score not found')

    try:
        review_at = driver.find_element(By.XPATH, '(//div[@class="review-container"])['+str(n)+']//span[@class="ratingDate"]').text
        review_at = review_at[9:]
        review_at = adjust_date(review_at)
        # print(review_at)
    except:
        review_at = ''
        # print('review_at not found')

    try:
        visit_at = driver.find_element(By.XPATH, '(//div[@class="review-container"])['+str(n)+']//div[@class="prw_rup prw_reviews_stay_date_hsx"]').text
        visit_at = visit_at[15:]
        visit_at = adjust_date(visit_at)
        # print(visit_at)
    except:
        visit_at = ''
        # print('visit_at not found')

    try:
        response_by = driver.find_element(By.XPATH, '(//div[@class="review-container"])['+str(n)+']//div[@class="prw_rup prw_reviews_response_header"]//div[@class="header"]').text
        response_by = response_by[0:response_by.find(',')]
        # print(response_by)
    except:
        response_by = ''
        # print('response_by not found')

    try:
        response_date = driver.find_element(By.XPATH, '(//div[@class="review-container"])['+str(n)+']//span[@class="responseDate"]').text
        response_date = response_date[10:]
        response_date = adjust_date(response_date)
        # print(response_date)
    except:
        response_date = ''
        # print('response_date not found')

    try:
        response = driver.find_element(By.XPATH, '(//div[@class="review-container"])['+str(n)+']//div[@class="mgrRspnInline"]//p[@class="partial_entry"]').text
        # print(response)
    except:
        response = ''
        # print('response not found')
    
    return [id_review, user, userloc, n_reviews, title, link_review, text, score, review_at, visit_at, response_by, response_date, response]

def get_single_review_soup(dom, n):
    x = 'access class review-container' #'review-container'

    try:
        xpath = '(//div[@class="review-container"])['+str(n)+']//div[@class="info_text pointer_cursor"]//div[1]'
        user = dom.xpath(xpath)[0].text
        # print(user)
    except:
        user = ''
        # print('user not found')

    try:
        xpath = '(//div[@class="review-container"])['+str(n)+']//div[@class="info_text pointer_cursor"]//div[@class="userLoc"]/strong'
        userloc = dom.xpath(xpath)[0].text
        # print(userloc)
    except:
        userloc = ''
        # print('userloc not found')

    try:
        try:
            xpath = '(//div[@class="review-container"])['+str(n)+']//div[@class="memberBadgingNoText is-shown-at-tablet"]//span[@class="badgetext"]'
            n_reviews = dom.xpath(xpath)[0].text
            n_reviews = int(n_reviews)
            # print(n_reviews)
        except: 
            xpath = '(//div[@class="review-container"])['+str(n)+']//div[@class="reviewerBadge badge"]//span[@class="badgeText"]'
            n_reviews = dom.xpath(xpath)[0].text
            n_reviews = int(n_reviews[:-8])
            # print(n_reviews)
    except:
        n_reviews = ''
        # print('n_reviews not found')

    try:
        xpath = '(//div[@class="review-container"])['+str(n)+']//span[@class="noQuotes"]'
        title = dom.xpath(xpath)[0].text
        # print(title)
    except:
        title = ''
        # print('title not found')

    try:
        xpath = '(//div[@class="review-container"])['+str(n)+']//div[@class="quote"]//a/@href'
        link_review = dom.xpath(xpath)[0]
        link_review = 'https://www.tripadvisor.com/'+link_review
        # print(link_review)
    except:
        link_review = ''
        # print('link_review not found')
    
    try:
        xpath = '(//div[@class="review-container"])['+str(n)+']//div[@class="quote"]//a/@id'
        id_review = dom.xpath(xpath)[0]
        id_review = int(id_review[2:])
        # print(id_review)
    except:
        try:
            xpath = '(//div[@class="review-container"])['+str(n)+']//div[@class="quote isNew"]//a/@id'
            id_review = dom.xpath(xpath)[0]
            id_review = int(id_review[2:])
            # print(id_review)
        except:
            id_review = ''
            # print('id_review not found')

    try:
        try:
            xpath = '(//div[@class="review-container"])['+str(n)+']//div[@class="prw_rup prw_reviews_google_translate_button_hsx"]'
            tradutor = dom.xpath(xpath)[0].text #testa a exixtencia do tradutor
            posic = 3
        except:
            posic = 2
        xpath = '(//div[@class="review-container"])['+str(n)+']//div/div/div/div[2]/div['+str(posic)+']/div/p/text()'
        erro = dom.xpath(xpath)[0] #caso nao tenha vai dar erro aqui
        text = ''
        for k in dom.xpath(xpath): text=text+k+' '
        text = text[:-1]
        # print(text)
    except:
        text = ''
        # print('text not found')

    try:
        xpath = '(//div[@class="review-container"])['+str(n)+']//div/div/div/div[2]/span[1]//@class'
        score = dom.xpath(xpath)[0]
        score = int(score[-2])
        # print(score)
    except:
        score = ''
        # print('score not found')

    try:
        xpath = '(//div[@class="review-container"])['+str(n)+']//span[@class="ratingDate"]'
        review_at = dom.xpath(xpath)[0].text
        review_at = review_at[9:]
        review_at = adjust_date(review_at)
        # print(review_at)
    except:
        review_at = ''
        # print('review_at not found')

    try:
        xpath = '(//div[@class="review-container"])['+str(n)+']//div[@class="prw_rup prw_reviews_stay_date_hsx"]/text()'
        visit_at = dom.xpath(xpath)[0]
        visit_at = adjust_date(visit_at)
        # print(visit_at)
    except:
        visit_at = ''
        # print('visit_at not found')

    try:
        xpath = '(//div[@class="review-container"])['+str(n)+']//div[@class="prw_rup prw_reviews_response_header"]//div[@class="header"]'
        response_by = dom.xpath(xpath)[0].text
        response_by = response_by[0:response_by.find(',')]
        # print(response_by)
    except:
        response_by = ''
        # print('response_by not found')

    try:
        xpath = '(//div[@class="review-container"])['+str(n)+']//span[@class="responseDate"]'
        response_date = dom.xpath(xpath)[0].text
        response_date = response_date[10:]
        response_date = adjust_date(response_date)
        # print(response_date)
    except:
        response_date = ''
        # print('response_date not found')

    try:
        xpath = '(//div[@class="review-container"])['+str(n)+']//div[@class="mgrRspnInline"]//p[@class="partial_entry"]/text()'
        erro = dom.xpath(xpath)[0] #caso nao tenha vai dar erro aqui
        response = ''
        for k in dom.xpath(xpath): response=response+k+' '
        response = response[:-1]
        # print(response)
    except:
        response = ''
        # print('response not found')
    
    return [id_review, user, userloc, n_reviews, title, link_review, text, score, review_at, visit_at, response_by, response_date, response]

def finalize_process_data(url, driver, review_all_data):
    driver.quit()
    data = pd.DataFrame(review_all_data[1:], columns=review_all_data[0])
    data.sort_values(by='review_at')

    filename = ('rvw_' + url[url.find('Reviews-') + 8:url.find('_State_of_')] + '_' + url[url.find('_Review-') + 17:url.find('-Reviews-')]).lower().replace("-", "_")
    data.to_csv(filename+'.csv', encoding='utf-8', index=False)

    print('   WebScraping success for: '+filename)
    return [filename, data]

def upd_actions(v, review_all_data, url, driver, last_rvw_ID, last_rvw_date, upd_per_ID, upd_per_date):
    review_at = v[8] #isso aqui pode variar +-8
    id_review = v[0]
    
    try:
        if upd_per_date and last_rvw_date - timedelta(days = 8) > review_at:
            print('   Adding %d more reviews\n'%len(review_all_data))
            return True
        if upd_per_ID and int(last_rvw_ID) == int(id_review):
            # review_all_data.append(v) #para ir um Review a mais
            print('   Adding %d more reviews\n'%(len(review_all_data)-1))
            return True
    except Exception as e:
        print('   Problem with '+x+'\n'+str(datetime.now()))
        pass

def create_connection(url):
    try:
        #rotate user agents:
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value,
                            OperatingSystem.LINUX.value]
        user_agent_rotator = UserAgent(software_names=software_names,
                                    operating_systems=operating_systems,
                                    limit=100)
        user_agent = user_agent_rotator.get_random_user_agent()

        # Open chrome
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--headless")
        options.binary_location = "/usr/bin/google-chrome"
        options.add_argument("--no-sandbox")
        #options.add_argument("--window-size=1920,1080")
        options.add_argument('--disable-gpu --start-maximized')
        options.add_argument('user-agent={user_agent}')
        options.add_argument("user-data-dir=/tmp/profile")
        # options.add_argument('--proxy-server=66.94.120.161:443') #AWS lambdas automate solve this problem

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get(url)

        #automate accept cookies for TripAdvisor
        filename = "tripadvisor_cookies.json"
        with open(filename, 'r+') as file:
            cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

        return driver
        
    except:
        print('   Driver not reached')
        return 1
        pass

def wsp_update_from_link(url, rvw_count, last_rvw_ID, last_rvw_date, upd_per_count, upd_per_ID, upd_per_date):
    try:
        try:
            if upd_per_count:
                    r_count = get_reviews_count('', url, upd_per_count) #vai por requests
                    if r_count == rvw_count:
                        return ['r_count == rvw_count', True]
            else:
                driver = create_connection(url) # se n'ao for _per_count vai ter que abrir o driver mesmo
                r_count = get_reviews_count(driver, url, upd_per_count)
        except:
            driver = create_connection(url)
            r_count = get_reviews_count(driver, url, False)

        r_page_count = math.ceil(r_count/15)
        r_last_tab = r_count%15
        
        try_err = 10
        open_page_list(driver, try_err)

        review_all_data = [['id_review' ,'user', 'userloc', 'n_reviews','title', 'link_review', 'text', 'score', 'review_at', 'visit_at', 'response_by', 'response_date', 'response']]
        count = 0
        for j in range(1,r_page_count+1):
            soup = BeautifulSoup(driver.page_source, 'lxml')
            dom = etree.HTML(str(soup))     
            if j < r_page_count:
                for n in range(1,15+1):
                    v = get_single_review_soup(dom, n)

                    if upd_per_ID or upd_per_date: #pode-se colocar isso aqui na outra funcao, mas adicionaria um if para cada rvw...
                        if upd_actions(v, review_all_data, url, driver, last_rvw_ID, last_rvw_date, upd_per_ID, upd_per_date):
                            if len(review_all_data)+rvw_count + 5 < r_count:
                                print('   Update constraints not satisfied: Updating entire table again')
                                driver.quit()
                                return wsp_from_newlink(url)
                            else:
                                return finalize_process_data(url, driver, review_all_data)

                    review_all_data.append(v)
                switch_page(driver, j+1)
            else:
                for n in range(1,r_last_tab+1):
                    v = get_single_review_soup(dom, n)

                    if upd_per_ID or upd_per_date:
                        if upd_actions(v, review_all_data, url, driver, last_rvw_ID, last_rvw_date, upd_per_ID, upd_per_date):
                            return finalize_process_data(url, driver, review_all_data)

                    review_all_data.append(v)


    except Exception as e:
        filename = ('rvw_' + url[url.find('Reviews-') + 8:url.find('_State_of_')] + '_' + url[url.find('_Review-') + 17:url.find('-Reviews-')]).lower().replace("-", "_")
        print('\n   Webscraping unsuccessfull for: '+str(filename)+' '+str(datetime.now()))
        return [False, False]

def wsp_from_newlink(url):
    try:
        driver = create_connection(url)

        r_count = get_reviews_count(driver, url, False)
        r_page_count = math.ceil(r_count/15)
        r_last_tab = r_count%15

        try_err = 10
        open_page_list(driver, try_err)

        review_all_data = [['id_review' ,'user', 'userloc', 'n_reviews','title', 'link_review', 'text', 'score', 'review_at', 'visit_at', 'response_by', 'response_date', 'response']]
        for j in range(1,r_page_count+1):
            soup = BeautifulSoup(driver.page_source, 'lxml')
            dom = etree.HTML(str(soup))

            if j < r_page_count:
                for n in range(1,15+1):
                    v = get_single_review_soup(dom, n)
                    review_all_data.append(v)
                switch_page(driver, j+1)
            else:
                for n in range(1,r_last_tab+1):
                    v = get_single_review_soup(dom, n)
                    review_all_data.append(v)

        return finalize_process_data(url, driver, review_all_data)

    except Exception as e:
        filename = ('rvw_' + url[url.find('Reviews-') + 8:url.find('_State_of_')] + '_' + url[url.find('_Review-') + 17:url.find('-Reviews-')]).lower().replace("-", "_")
        print('\n   Webscraping unsuccessfull for: '+str(filename)+' '+str(datetime.now()))
        return [False, False]
