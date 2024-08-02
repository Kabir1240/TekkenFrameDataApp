import requests
from bs4 import BeautifulSoup


class TekkenDocs:
    def __init__(self):
        self.url = "https://tekkendocs.com/"
        
        response = requests.get(self.url)
        response.raise_for_status()

        self.soup = BeautifulSoup(response.text, "html.parser")
        
    def get_character_data(self):
        characters = []
        list_elements = self.soup.find(class_="grid grid-cols-4 gap-x-1 gap-y-3 xs:grid-cols-5 xs:gap-x-2 sm:grid-cols-6 md:grid-cols-8 lg:grid-cols-9").find_all(class_="cursor-pointer")

        for element in list_elements:
            link = element.select("a.cursor-pointer")
            if link != []:
                link = link[0].get("href")
                
                name = link.replace("/t8/", "")
                link = self.url[:-1] + link
                image_link = self.url[:-1] + element.select("a div div.rt-CardInner img")[0].get('src')
                
                character = {
                    "name":name,
                    "link":link,
                    "image_link":image_link,
                }
                
                characters.append(character)
        
        return characters
