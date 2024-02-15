import bs4 as bs
import pickle as pk
import requests


# US states and cities
response = requests.get('https://www.britannica.com/topic/list-of-cities-and-towns-in-the-United-States-2023068')

soup = bs.BeautifulSoup(response.text, features='lxml')
states = soup.findAll('div', {'class': 'reading-channel'})

US = {}
for state in states[0].findAll('section')[1:]:
    st = state.find('h2').text
    US[st] = []
    for city in state.find('ul').findAll('li'):
        US[st].append(city.text)

with open('../data/US_states_and_cities.pickle', 'wb') as f:
    pk.dump(US, f, pk.HIGHEST_PROTOCOL)

        