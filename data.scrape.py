from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import nltk
from nltk.corpus import stopwords
from collections import Counter

def collect_incident_urls(days):
    incident_urls = []
    url_base = 'https://incidentreports.uchicago.edu/incidentReportArchive.php?reportDate='
    # base date is 7/7/16
    base_date = 1467867600
    for d in range(days):
        url = url_base + str(base_date - d * 86400)
        incident_urls.append(url)
    return(incident_urls)

def scrape_incident_page(url):
    htmlText = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(htmlText)
    table = soup.find('table')
    sub_tables = table.findAll('tr')
    sub_tables = sub_tables[1:len(sub_tables)-1]
    incidents = []
    for tbl in sub_tables:
        ts = tbl.findAll('td')
        l = [str(t)[4:-5] for t in ts]
        incidents.append(l)
    df = pd.DataFrame(incidents)
    if len(df.columns) != 7:
        return(pd.DataFrame([url]))
    else: return(df)


def get_incident_data(number_of_days):
    urls = collect_incident_urls(number_of_days)
    dfs = [scrape_incident_page(url) for url in urls]
    big_df = pd.concat(dfs, ignore_index= True)
    big_df.columns = ['Incident', 'Location', 'Reported Date', 'Occured Date', 'Comments', 'Disposition', 'UCPDI#']
    return(big_df)

#def refine_incident_data(df):
    # nltk.download()
    # s = set(stopwords.words('english'))
    # dict = Counter(filter(lambda w: not w in s, ' '.join(df['Comments'].dropna()).split()))
    # print(dict)
df = pd.read_csv('incident_data.csv')
#get_incident_data(365*5).to_csv('incident_data.csv')