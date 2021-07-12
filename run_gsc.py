#!/usr/bin/env python
'''
@author:    Jean-Christophe Chouinard. 
@role:      Sr. SEO Specialist at SEEK.com.au
@website:   jcchouinard.com
@LinkedIn:  linkedin.com/in/jeanchristophechouinard/ 
@Twitter:   twitter.com/@ChouinardJC

Learn Python for SEO
jcchouinard.com/python-for-seo

Get API Keys
jcchouinard.com/how-to-get-google-search-console-api-keys/

How to format your request
jcchouinard.com/what-is-google-search-console-api/
'''

from dateutil import relativedelta

from gsc_by_url import gsc_by_url
from gsc_with_filters import gsc_with_filters
from gsc_to_csv_by_month import gsc_to_csv
from oauth import authorize_creds, execute_request

site = 'https://www.armine.com'# Property to extract              
creds = 'client_secret.json' # Credential file from GSC
output = 'gsc_data.csv'
start_date = '2021-07-01'
end_date = '2021-07-05'      

webmasters_service = authorize_creds(creds) 

# Google Search Console Data From a List of URLs
"""
list_of_urls = ['/indirimli-kampanya-urunleri/','/kampanya/']
list_of_urls = [site + x for x in list_of_urls]
args = webmasters_service,site,list_of_urls,creds,start_date
url_info_df = gsc_by_url(*args)
print(url_info_df)
"""

# Filters
"""
dimension = 'query'     # query, page
operator = 'contains'   # contains, equals, notEquals, notContains
expression = 'tesettur'   # whatever value that you want
args = webmasters_service,site,creds,dimension,operator,expression,start_date

filter_info_df = gsc_with_filters(*args, rowLimit=100)
filter_info_df = filter_info_df.sort_values(['position'], ascending=True)
print(filter_info_df)
"""

# All gsc data to csv
"""
args = webmasters_service,site,output,creds,start_date
gsc_to_csv(*args, end_date=end_date)
"""

# Get List of Validated Websites Url
# Let’s see what websites we have validated in Google Search Console using the API.
"""
site_list = webmasters_service.sites().list().execute()
#print(site_list)
verified_sites_urls = [s['siteUrl'] for s in site_list['siteEntry']
                       if s['permissionLevel'] != 'siteUnverifiedUser'
                          and s['siteUrl'][:4] == 'http']

for site_url in verified_sites_urls:
    print(site_url)
"""

