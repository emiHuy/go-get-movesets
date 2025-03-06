# Filename:     web_scraper.py
# Author:       Emily
# Created:      December 15, 2024
# Description:  This file contains functions that fetch Pokemon data.
  
from bs4 import BeautifulSoup
import requests

def get_moveset(pokemon):
    """
    Function Description:
        Fetches moveset of a given Pokemon from the Pokemon database
    Parameters:
        pokemon (str): Name of Pokemon being searched
    Return:
        tuple: Names of fast and charged attacks
    """
    page = requests.get("https://pokemon.gameinfo.io/en/pokemon/"+pokemon)
    soup = BeautifulSoup(page.text, "html.parser")
    moves = soup.select('a[href^="/en/move/"]')[:2]

    for i in range(2):
        moves[i] = moves[i].get_text(strip=True)
        target_tag = soup.find('a', string=moves[i])
        if target_tag.find_next().get_text(strip=True) == "Elite TM":
            moves[i] += "*"
            
    return moves[0], moves[1]

def get_pokedex():
    """
    Function Description:
        Fetches list of Pokemon names and ids from Pokedex page
    Return:
        tuple: List of pokemon names and list of their corresponding ids
    """
    page = requests.get("https://pokemondb.net/go/pokedex")
    soup = BeautifulSoup(page.text, "html.parser")
    tags = soup.findAll("a", attrs={"class": "ent-name"})

    pokedex = []
    for t in tags:
        pokemon = t.getText(strip=True)
        id = t.get("title")[18:22]
        if pokemon[-1].isalpha() == False:
            pokemon = pokemon[:-1]
        if [pokemon,id] not in pokedex:
            pokedex.append([pokemon,id])
    
    pokedex.sort()
    pokemon_list = []
    pokemon_ids = []
    for line in pokedex:
        pokemon_list.append(line[0])
        pokemon_ids.append(line[1])
        
    return pokemon_list, pokemon_ids

if __name__ == "__main__":
    p = input("Pokemon ('quit' to quit): ")
    while p.lower() != "quit":
        try:
            f,c = get_moveset(p)
            print("Fast attack: " + f)
            print("Charged attack: " + c)
            p = input("\nPokemon ('quit' to quit): ")
        except:
            print("Pokemon does not exist in database.\n")
            p = input("Pokemon ('quit' to quit): ")
    print("Thanks for using GO Get Movesets!")
