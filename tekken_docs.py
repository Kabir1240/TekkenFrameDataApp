import requests
from bs4 import BeautifulSoup
from typing import Dict


class TekkenDocs:
    def __init__(self):
        self.url = "https://tekkendocs.com/"
        
        response = requests.get(self.url)
        response.raise_for_status()

        self.soup = BeautifulSoup(response.text, "html.parser")
        
    def get_character_data(self) -> list[Dict]:
        # return value
        characters = []
        # get data for tekken 8 specifically
        list_elements = self.soup.find(class_="grid grid-cols-4 gap-x-1 gap-y-3 xs:grid-cols-5 xs:gap-x-2 sm:grid-cols-6 md:grid-cols-8 lg:grid-cols-9").find_all(class_="cursor-pointer")

        # for each character
        for element in list_elements:
            link = element.select("a.cursor-pointer")
            if link != []:
                link = link[0].get("href")
                
                # isolate and save character data in a dictionary
                name = link.replace("/t8/", "")
                link = self.url[:-1] + link
                image_link = self.url[:-1] + element.select("a div div.rt-CardInner img")[0].get('src')
                
                character = {
                    "name":name,
                    "link":link,
                    "image_link":image_link,
                }
                
                # add each character's data to the return value list
                characters.append(character)
                
        # return the list of dictionaries
        return characters
    
    def get_character_moveset(self, character_url:str) -> list[Dict]:
        moves = []
        
        # get all moves from character page
        response = requests.get(character_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        moveset = soup.find_all("tr", class_="rt-TableRow")

        # find each row
        for move in moveset:
            move_data = move.find_all('td', class_="rt-TableCell")
            new_move = {}
            
            # if row is'nt empty, isolate required data into a dictionary
            if move_data != []:
                new_move['command'] = move_data[0].find("a").text
                new_move['hit level'] = move_data[1].text
                new_move["damage"] = move_data[2].text
                new_move['startup'] = move_data[3].text
                new_move['block'] = move_data[4].text
                new_move['hit'] = move_data[5].text
                new_move['counter hit'] = move_data[6].text
                
                # retrieve notes as a list
                notes = []
                notes_soup = move_data[7].find_all("div")
                for note in notes_soup:
                    notes.append(note.text)
                new_move['notes'] = notes

                # add each move to a list
                moves.append(new_move)
        
        return moves