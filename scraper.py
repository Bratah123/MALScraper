import bs4
from urllib.request import urlopen
import json

with open("anime_characters.json", "r") as f:
    characters = json.load(f)  # Refer to the README.md to check how the data is organized


def main():
    page_num = int(input("What page number do you want to scrape? "))
    web_page_num = (page_num - 1) * 50
    url = f'https://myanimelist.net/character.php?limit={web_page_num}'  # limit=0 indicates first page
    web_client = urlopen(url)
    page_html = web_client.read()
    page_soup = bs4.BeautifulSoup(page_html, "html.parser")
    list_of_images = page_soup.findAll('img')
    # Remove all the img tags that don't have anime characters
    list_of_anime_characters = [img for img in list_of_images if "https://cdn.myanimelist.net/r" in str(img)]

    for img_html in list_of_anime_characters:
        name = img_html['alt'].split(", ")
        img_link = img_html['data-srcset'].split()[2]

        character = {
            "name": name,
            "img": img_link
        }

        characters.append(character)

    update_json(characters)
    print("Finished writing to json file, total characters:", len(characters))


def update_json(data):
    with open("anime_characters.json", "w") as file:
        json.dump(data, file, indent=4)


if __name__ == '__main__':
    main()
