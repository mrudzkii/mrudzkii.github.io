from bs4 import BeautifulSoup
import requests
from duckduckgo_search import DDGS


url = 'https://pawelbiega.pl/buty-do-biegania-z-maksymalna-amortyzacja-przeglad/'
request = requests.get(url)
# print(request.text)
soup = BeautifulSoup(request.text, 'html.parser')
print(type(soup));
kolumnny = {}
i = 0
nazwy = soup.find('tr', attrs='row-1')
for kolumna in nazwy.find_all('th'):
    kolumnny[i] = kolumna.text
    i += 1

buty = {}
for i in range(2, 13):
    but = soup.find('tr', attrs=f"row-{i}")
    specki = but.find_all('td')
    model = specki[0].text
    buty[model] = {}
    with open(model.strip().replace(' ', '-') + ".md", 'w') as podstrona:
        podstrona.write('# ' + model + '\n')
        for j in range(1, len(specki)):
            buty[model][kolumnny[j]] = specki[j].text
            podstrona.write('- ' + kolumnny[j] + ': ' + specki[j].text + '\n')
        results = DDGS().images(
            keywords=model,
            region="wt-wt",
            safesearch="off",
            size=None,
            type_image=None,
            layout=None,
            license_image=None,
            max_results=5,
        )
        for res in results:
            link = res['image'].split(' ')[0]
            podstrona.write("![Alt text](" + link + ')\n')

with open('strona.md', 'w') as website:
    website.write('## Lista NAJLEPSZYCH butów jeśli chodzi o amortyzację\n')
    for but in buty.keys():
        website.write('- [' + but.strip() + '](' + but.strip().replace(' ', '-').replace('\n', '') + '.md' + ')\n')
    website.write('### [źródło](' + url + ')\n')
