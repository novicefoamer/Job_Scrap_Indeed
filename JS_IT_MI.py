import csv
from datetime import datetime
from typing import Counter
import requests
from bs4 import BeautifulSoup
import xlsxwriter
import openpyxl
from openpyxl.utils.cell import get_column_letter
import pandas as pd
def get_url(position,location):
    template = 'https://www.indeed.com/jobs?q={}&l={}&sort=date&fromage=14'
    position = position.replace(' ','+')
    location = location.replace(' ','+')

    url=template.format(position,location)
    return url
url = get_url('IT','Livonia, MI')
print(url)
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
cards = soup.find_all('td', 'resultContent')
print(len(cards))
#card = cards[0]
for i in range(0,len(cards)):
    card=cards[i]
    #print(card)
    job_title = card.find('div', class_='css-1xpvg2o e37uo190').text.strip()
    company = card.find('span','companyName').text.strip()
    job_location = card.find('div', 'companyLocation').text.strip()
#post_date = card.find('span', 'date').text
#today = datetime.today().strftime('%Y-%m-%d')
    record = (job_title, company, job_location)

def get_record(card):
    job_title = card.find('div', class_='css-1xpvg2o e37uo190').text.strip()
    company = card.find('span', 'companyName').text.strip()
    job_location = card.find('div', 'companyLocation').text.strip()
    record = (job_title, company, job_location)
    return record
records = []
for card in cards:
    record = get_record(card)
    records.append(record)
while True:
    try:
        url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
    except AttributeError:
        break

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all('td', 'resultContent')

    for card in cards:
        record = get_record(card)
        records.append(record)

workbook=xlsxwriter.Workbook("Job_MI.xlsx")
worksheet=workbook.add_worksheet()
row = 0 
col = 0
for job_title,company,job_location in records:
    worksheet.write(row,col,job_title)
    worksheet.write(row,col+1,company)
    worksheet.write(row,col+2,job_location)
    row+=1
workbook.close()
df = pd.read_excel('Job_MI.xlsx', names=['Job','Company','Location'])
for Job in df.columns:
    df[Job] = df[Job].str.replace('new'," ")
df.sort_values(by='Company', inplace=True)
# df.sort_index(axis=0)

