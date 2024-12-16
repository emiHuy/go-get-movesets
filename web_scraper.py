from bs4 import BeautifulSoup
import requests

def get_moveset(pokemon):
    page = requests.get("https://pokemon.gameinfo.io/en/pokemon/"+pokemon)
    soup = BeautifulSoup(page.text, "html.parser")
    aTags = soup.findAll('a')

    moves = []
    for a in aTags:
        info = a.getText(strip=True)
        href = a.get('href')
        if "/en/move/" in href:
            moves.append(info)
    return moves[0], moves[1]

def get_pokedex():
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

