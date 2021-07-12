'''
    https://www.jcchouinard.com/keyword-cannibalization-tool-with-python/
'''

import pandas as pd
import requests
from bs4 import BeautifulSoup

from collections import defaultdict
import datetime
from dateutil import relativedelta

from date_manip import date_to_str
from oauth import authorize_creds, execute_request

today = datetime.datetime.now()
days = relativedelta.relativedelta(days=3)
default_end = today - days 

# Run the extraction
def keyword_cannibalization(webmasters_service,site,start_date,device_category='',end_date=default_end,rowLimit=1000):
    request = {
        'startDate': date_to_str(start_date),
        'endDate': date_to_str(end_date),
        'dimensions': ['page','query','device'],
        'rowLimit': rowLimit #up to 25.000 urls
    }
    
    #Adding a device filter to request
    if device_category:
        request['dimensionFilterGroups'] = [{'filters':[{'dimension':'device','expression':device_category}]}]
    
    #Request to SC API
    response = execute_request(webmasters_service, site, request)

    scDict = defaultdict(list)
    for row in response['rows']:
        scDict['page'].append(row['keys'][0] or 0)
        scDict['query'].append(row['keys'][1] or 0)
        scDict['device'].append(row['keys'][2] or 0)
        scDict['clicks'].append(row['clicks'] or 0)
        scDict['ctr'].append(row['ctr'] or 0)
        scDict['impressions'].append(row['impressions'] or 0)
        scDict['position'].append(row['position'] or 0)
    
    df = pd.DataFrame(data = scDict)
    df['clicks'] = df['clicks'].astype('int')
    df['ctr'] = df['ctr']*100
    df['impressions'] = df['impressions'].astype('int')
    df['position'] = df['position'].round(2)
    df.sort_values('clicks',inplace=True,ascending=False)

    SERP_results = 8 #insert here your prefered value for SERP results
    branded_queries = 'armine|armıne' #insert here your branded queries
    
    df_canibalized = df[df['position'] > SERP_results] 
    #df_canibalized = df
    #df_canibalized = df_canibalized[~df_canibalized['query'].str.contains(branded_queries, regex=True)]
    df_canibalized = df_canibalized[df_canibalized.duplicated(subset=['query'], keep=False)]
    df_canibalized.set_index(['query'],inplace=True)
    df_canibalized.sort_index(inplace=True)
    df_canibalized.reset_index(inplace=True)

    try:
        df_canibalized['title'],df_canibalized['meta'] = zip(*df_canibalized['page'].apply(get_meta))
    except:
        print('warning: insufficient rowLimit')

    return df_canibalized

def get_meta(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content,'html.parser')
        title = soup.find('title').get_text().strip()
    except:
        title = ''
    try:
        meta = soup.find('meta', attrs={'name':'description'})['content'].strip()
    except:
        meta = ''
    return title, meta