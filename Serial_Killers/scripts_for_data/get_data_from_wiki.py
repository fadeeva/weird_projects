import bs4 as bs
import pandas as pd
import numpy as np
import requests

# US serial killers
response = requests.get('https://en.wikipedia.org/wiki/List_of_serial_killers_in_the_United_States')

soup = bs.BeautifulSoup(response.text, features='lxml')
tables = soup.findAll('table', {'class': 'wikitable'})

serial_killers = {
    'Identified'  : [],
    'Unidentified': [],
}

for sk_type, table in zip(serial_killers.keys(), tables):
    for row in table.find('tbody').findAll('tr'):
        row_data = []
        
        for cell in row.find_all('td'):
            row_data.append(cell.text.replace('\n', ''))
        
        if row_data:
            serial_killers[sk_type].append(row_data)

columns = [
    'Name',
    'Years active',
    'Proven Victims',
    'Possible Victims',
    'Status',
    'Notes',
    'Ref',
]            
serial_killers_identified = pd.DataFrame(data=serial_killers['Identified'],
                                         columns=columns)
serial_killers_identified.to_csv('../data/serial_killers_identified_RAW.csv')

columns = [
    'Name',
    'Years active',
    'Proven Victims',
    'Possible Victims',
    'Region where active',
    'Notes',
    'Ref',
]            
serial_killers_unidentified = pd.DataFrame(data=serial_killers['Unidentified'],
                                           columns=columns)
serial_killers_unidentified.to_csv('../data/serial_killers_unidentified_RAW.csv')
    
    
    
    
    
    
