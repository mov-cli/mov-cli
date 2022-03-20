from bs4 import BeautifulSoup as BS 
import requests, json, os
from colorama import Fore

class Movie:
    def __init__(self):
        q = input(Fore.BLUE + "[!] Please Enter the name of the Movie: ")
        self.data(q)
        
    def play(self, link,info):
        req = requests.get(link).text
        soup = BS(req,"html.parser")
        link = json.loads(soup.select('#__NEXT_DATA__')[0].text)['props']['pageProps']['videoUrl']
        try:
            try:os.system(f'mpv --referrer="https://theflix.to" "{link}" --force-media-title="mov-cli:{info}"')
            except:os.system(f'vlc --http-referrer="https://theflix.to" "{link}"')# --meta-title="{info}"
        except:print(Fore.RED + "Please install either mpv or vlc!")

    def data(self, q):
        #q = input("Please Enter the name of the Movie!")
        req = requests.get(f"https://theflix.to/movies/trending?search={q.replace(' ','+')}").text
        soup = BS(req,"html.parser")
        link = json.loads(soup.select('#__NEXT_DATA__')[0].text)['props']['pageProps']['mainList']['docs']
        choices = [[i['name'],i['id'],i['available']] for i in link if i['available']]
        for i in choices:
            if i[0].__contains__(':'):i[0] = i[0].replace(":","")
        self.display(choices)

    def display(self, info):
        for idx,val in enumerate(info):print(Fore.GREEN + f"[{idx+1}] {val[0]}", end="\n\n")
        print(Fore.RED + "[q] Exit!", end="\n\n")
        print(Fore.YELLOW + "[s] Search Again!")
        print(Fore.CYAN + "[d] Download!")
        choice = ""
        while choice not in range(len(info) + 1):# or not choice == "q"
            choice = input(Fore.BLUE + "Enter choice: ")
            if choice == "q":
                print(Fore.RESET + 'Bye!')
                return                
            elif choice == "s":
                q = input(Fore.BLUE + "[!] Please Enter the name of the Movie: ")
                self.data(q)
            else:
                try:self.page(info[int(choice)-1])
                except:print(Fore.RED + "Invalid choice entered")

    def page(self, info):
        link = f'https://theflix.to/movie/{info[1]}-{info[0].lower().replace(" ","-")}'
        self.play(link,info[0])

mov = Movie()
