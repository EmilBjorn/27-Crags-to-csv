#%%#
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os


def scrape_routes(URL: str) -> None:
    os.system('cls')
    print('Fetching data from website...\r', end='')
    page = requests.get(URL)
    print('Fetching data from website... Done!')
    # %%
    print('Parsing routes...\r', end='')
    soup = BeautifulSoup(page.content, 'html.parser')
    routesouplist = soup.find_all('tr')[1:]
    # %%
    df = pd.DataFrame()

    for route in routesouplist:
        name = route.find("div", class_='hidden').contents[0].strip()
        info = route.find_all('td', class_='hidden-xs')
        grade = info[0].find('span', class_='grade').contents[0]
        genre = info[1].contents[0]
        ascents = info[2].contents[0]
        rating = info[3].find('div', class_='rating').contents[0]
        sector = route.find('td',
                            class_='stxt hidden-xs').find('a').contents[0]
        rowdict = {
            'name': [name],
            'grade': [grade],
            'genre': [genre],
            'sector': [sector],
            'ascents': [ascents],
            'rating': [rating]
        }
        df = pd.concat([df, pd.DataFrame(rowdict)])

    print('Parsing routes... Done!')
    print('Writing csv-file...\r', end='')
    df.to_csv(f"{URL.split('/')[-2]}.csv", index=False)
    print('Writing csv-file... Done!')


# %%

if __name__ == '__main__':
    URL = input(
        "Enter routelist URL for the desired area, eg. 'https://27crags.com/crags/kullaberg/routelist'\n"
    )
    scrape_routes(URL)
