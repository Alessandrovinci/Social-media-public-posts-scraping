# selenium-related

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


# other necessary ones
import pandas as pd
import time
import re


def convert_query_to_url_part(query):
    query=query.split(' ')
    new_query=''
    for q in query:
        new_query+=q+'%20'
    return new_query[:-3]
    
def get_date(t):
    t=t[0]
    try:
        res= t.split('\xa0')[1].strip()
    except:
        res='Not found'
    if res=='':
        try:
            res = t.split('\xa0')[2].strip()
            if "Paid" in res:
                res= t.split('\xa0')[3].strip()
        except:
            res='Not found'
    return res


def get_auth(t):
    t=t[0]
    try:
        return t.split('\xa0')[0].strip()
    except:
        return ''

def get_clen_text(t):
    t=t[0]
    try:
        if "· Shared with" in t.split('Public')[1]:
            return t.split('Public')[1].split("See more")[0]+' CITING: '+t.split('Public')[2].split("See more")[0]
        else:
            return t.split('Public')[1].split("See more")[0]
    except:
        pass
    try:
        return t.split('Custom')[1].split("See more")[0]
    except:
        return t
    

def main(query,words,EMAIL,PASSWORD,already_saved):
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")
    option.add_argument("--headless")
    option.add_argument("--no-sandbox")
    option.add_argument("--disable-dev-shm-usage")
    
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    option.add_experimental_option("prefs",prefs)
    
    browser = webdriver.Chrome(options=option)
    browser.get("http://facebook.com")
    browser.maximize_window()
    wait = WebDriverWait(browser, 30)
    email_field = wait.until(EC.visibility_of_element_located((By.NAME, 'email')))
    email_field.send_keys(EMAIL)
    time.sleep(3)
    pass_field = wait.until(EC.visibility_of_element_located((By.NAME, 'pass')))
    pass_field.send_keys(PASSWORD)
    time.sleep(3)
    pass_field.send_keys(Keys.RETURN)
    time.sleep(5)
    browser.implicitly_wait(10)
    
    try:
        time.sleep(2)
        browser.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div/div/div/div[1]/div[2]/div/div/div/div/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[1]").click()
        time.sleep(2)
    except:
        print("RERUN")
        pass
        
    
    query=convert_query_to_url_part(query)
    browser.get(f'https://www.facebook.com/search/posts/?q={query}')
    browser.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div[2]/div[2]/div[1]/div/div[2]/div/input").click()
                       
    time.sleep(5)
    
    # scroll to the bottom
    SCROLL_PAUSE_TIME = 5
    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        browser.implicitly_wait(10)
        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    time.sleep(5)
    post_to_monitor={}
    soup=bs(browser.page_source,"html.parser")
    
    #go to each post and get text
    #query=soup.find_all("div",{"class":"du4w35lb k4urcfbm l9j0dhe7 sjgh65i0"})
    query=soup.find_all("div",{"class": "g4tp4svg mfclru0v om3e55n1 p8bdhjjv"})

    texts=[q.text for q in query]
    
    dates=[]
    for q in query:
        kk=str(q).split('<a aria-label=')
        try:
            d=kk[2].split("class")[0]
        except:
            d=''
        dates.append(d)
        
    urls=[]
    for q in query:
        try:
            d=str(q).split('href')[1].split('role')[0]
            ur=re.findall(r'\"(.+)\"',d)[0]
        except:
            ur=''
        urls.append(ur)
        
    #if the query word is in the text save the post
    for i,t in enumerate(texts):
        my_list=[]
        for w in words:
            if w.lower()=='eni':
                test=re.search(rf'\b{w.lower()}\b', t.lower())
                if test!=None:
                    my_list.append(w)
                else:
                    pass
            else:
                if w.lower() in t.lower():
                    my_list.append(w)
                else:
                    pass
        post_to_monitor[i]=[my_list,[t]]
        
    #Check that the post is not already saved
    keep_saving=[]
    for i,post in enumerate(texts):
        if post in already_saved:
            pass
        else:
            already_saved.append(post)
            keep_saving.append(i)
    
    final_dict = { key: post_to_monitor[key] for key in keep_saving }
    final_dict_dates={ key: dates[key] for key in keep_saving }
    final_dict_urls={ key: urls[key] for key in keep_saving }
    
    df=pd.DataFrame(final_dict).T
    df.columns=['keywords','complete_text']
    df_dates=pd.Series(final_dict_dates).T
    df_urls=pd.Series(final_dict_urls).T
    df['new_dates']=df_dates
    df['date']=df['complete_text'].apply(get_date)
    df['author']=df['complete_text'].apply(get_auth)
    df['clean']=df['complete_text'].apply(get_clen_text)
    df['urls']=df_urls
    df2=df[['new_dates','date','author','clean','keywords','urls']]
    return df2,already_saved


