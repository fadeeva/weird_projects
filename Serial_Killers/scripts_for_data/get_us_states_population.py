import bs4 as bs
import pickle as pk
import requests


# US states and cities
response = requests.get('https://www.britannica.com/topic/largest-U-S-state-by-population')

soup = bs.BeautifulSoup(response.text, features='lxml')
states = soup.findAll('div', {'class': 'md-drag md-table-wrapper'})


US = []
for state in states[0].findAll('tr')[1:]:
    s = []
    for td in state.findAll('td'):
        s.append(td.text)
    US.append(s)


with open('../data/US_states_population.pickle', 'wb') as f:
    pk.dump(US, f, pk.HIGHEST_PROTOCOL)

        