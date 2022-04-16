'''
function to get imdb id of a show
usage
from imdb import get_id
'''

import requests
from colorama import Fore, Style

cyan = lambda a: f"{Fore.CYAN}{a}{Style.RESET_ALL}"

def get_id(query):
    query = query.replace(" ","_")
    
    url = f"https://v2.sg.media-imdb.com/suggestion/{query[0]}/{query}.json"
    
    r=requests.get(url)
    
    imdb_ids = [i["id"] for i in r.json().get("d")]
    names = [i["l"] for i in r.json().get("d")]
    
    print(cyan("[*]Results: "))
    print("\n")
    for i in range(len(names)):
        print(cyan(f"{i+1}. {names[i]}"))
    
    print("\n")    
    c = int(input(cyan("[*]Enter number: ")))
    
    return imdb_ids[c-1]