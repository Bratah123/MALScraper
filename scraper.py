import bs4
from urllib.request import urlopen
import json
import time

with open("anime_characters.json", "r") as f:
    characters = json.load(f)  # Refer to the README.md to check how the data is organized


def main():
    page_num = int(input("How many pages would you like to scrape? "))
    print(f"Estimated {page_num * 4} seconds until completion.")
    for n in range(1 , page_num+1):
        print(f"Scraping page {n}...")
        time.sleep(4)
        web_page_num = (n - 1) * 50
        url = f'https://myanimelist.net/character.php?limit={web_page_num}'  # limit=0 indicates first page
        web_client = urlopen(url)
        page_html = web_client.read()
        page_soup = bs4.BeautifulSoup(page_html, "html.parser")
        list_of_ranks = page_soup.findAll("tr", class_="ranking-list")
        # Remove all the img tags that don't have anime characters

        for rank in list_of_ranks:
            img_html = rank.find('img') # Information about the characters, name and image are stored here
            title_html = rank.find('div', class_='title').find('a') # Information about where the character came from is here

            name = img_html['alt'].split(", ")
            anime_from = title_html.contents[0] # What anime the character came from.

            img_link = img_html['data-srcset'].split()[2]

            character = {
                "name": name,
                "img": img_link,
                "anime": anime_from,
            }

            characters.append(character)

    update_json(characters)
    print("Finished writing to json file, total characters:", len(characters))


def update_json(data):
    with open("anime_characters.json", "w") as file:
        json.dump(data, file, indent=4)


if __name__ == '__main__':
    main()
