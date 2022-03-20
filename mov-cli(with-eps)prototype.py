import requests, json, os
from bs4 import BeautifulSoup as BS
from colorama import Fore

def query(q,morws):
    if morws == "ws":
        lst = [[i['name'].replace(":","").replace("'",'-'),i['id'],i['available'],i['numberOfSeasons'],"WS"] for i in json.loads(BS(requests.get(f"https://theflix.to/tv-shows/trending?search={q}").text,"html.parser").select('#__NEXT_DATA__')[0].text)['props']['pageProps']['mainList']['docs'] if i['available']]
        return lst
    elif morws == "m":
        lst = [[i['name'].replace(":","").replace("'",'-'),i['id'],i['available'],"MOVIE"] for i in json.loads(BS(requests.get(f"https://theflix.to/movies/trending?search={q.replace(' ','+')}").text,"html.parser").select('#__NEXT_DATA__')[0].text)['props']['pageProps']['mainList']['docs'] if i['available']]
        return lst

def data(q,ws=True,m=True,v=False):
    choices = []
    if ws and m:
        for i in query(q,'ws'):choices.append(i) 
        for i in query(q,'m'):choices.append(i)
    elif m:
        for i in query(q,"m"):choices.append(i)
    elif ws:
        for i in query(q,'ws'):choices.append(i)
    return display(choices)

def page(info):
    link = f'https://theflix.to/movie/{info[1]}-{info[0].lower().replace(" ","-").replace(":","").replace(a,"").replace(".","")}'
    return (link,info[0])

def wspage(info):
    print(info)
    a = "'"
    link = f'https://theflix.to/tv-show/{info[1]}-{info[0].lower().replace(" ","-").replace(":","").replace(a,"").replace(".","")}/season-{info[-2]}/episode-{info[-1]}'
    #https://theflix.to/tv-show/60574-peaky-blinders/season-6/episode-2
    #1=id,0=name,2=season,3=episode
    return (link,info[0])


def display(info):
    for idx,val in enumerate(info):print(Fore.GREEN + f"[{idx+1}] {val[0]}", end="\n\n")
    print(Fore.RED + "[q] Exit!", end="\n\n")
    print(Fore.YELLOW + "[s] Search Again!")
    print(Fore.CYAN + "[d] Download!")
    choice = ""
    while choice not in range(len(info) + 1):# or not choice == "q"
        choice = input(Fore.BLUE + "Enter choice: ")
        if choice == "q":return
        elif choice == "s":
            q = input(Fore.BLUE + "[!] Please Enter the name of the Movie: ")
            return data(q)
        elif choice == 'd':
            try:
                mov = int(input(Fore.YELLOW + "[!] Please enter the number of the movie you want to download: "))-1
                inf = info[mov]
                print(inf)
                if inf[-1] == "WS":
                    season = ""
                    while season not in range(inf[-2]+1):
                        season = input(Fore.LIGHTMAGENTA_EX + f"Please input the season number(total seasons:{inf[-2]}): ")
                        episodes = json.loads(BS(requests.get(f"https://theflix.to/tv-show/{inf[1]}-{inf[0].lower().replace(' ','-').replace(a,'-').replace(':','').replace('.','')}/season-{season}/episode-1").text,"html.parser").select('#__NEXT_DATA__')[0].text)['props']['pageProps']['selectedTv']['seasons'][0]['numberOfEpisodes']
                        episode = input(Fore.LIGHTMAGENTA_EX + f"Please input the episode number(total episodes in {season}:{episodes}): ")
                        with open(f'{inf[0]}.mp4','wb') as f:
                            url = cdnurl(wspage([inf[0],inf[1],season,episode])[0],inf[0])
                            req = requests.get(url,stream=True)
                            for i in req.iter_content(chunk_size=1024):
                                if i:
                                    f.write(i)
                            print('.',end="")
                with open(f'{inf[0]}.mp4','wb') as f:
                    url = cdnurl(page(inf)[0],inf[0])[0]
                    req = requests.get(url,stream=True)
                    for i in req.iter_content(chunk_size=1024):
                        if i:
                            f.write(i)
                            print('.',end="")
            except:
                if len(info) < mov:print(Fore.RED + "Invalid Choice entered" )
                else:print(Fore.LIGHTRED_EX + 'Unable to Download')
        else:
            try:
                selection = info[int(choice)-1]
                print(selection)
                if selection[-1] == "WS":
                    season = input(Fore.LIGHTMAGENTA_EX + f"Please input the season number(total seasons:{selection[-2]}): ")
                    a = "'"
                    episodes = json.loads(BS(requests.get(f"https://theflix.to/tv-show/{selection[1]}-{selection[0].lower().replace(' ','-').replace(a,'-').replace(':','').replace('.','')}/season-{season}/episode-1").text,"html.parser").select('#__NEXT_DATA__')[0].text)['props']['pageProps']['selectedTv']['seasons'][0]['numberOfEpisodes']
                    episode = input(Fore.LIGHTMAGENTA_EX + f"Please input the episode number(total episodes in {season}:{episodes}): ")
                    selection.append(season)
                    selection.append(episode)
                    play(wspage(selection))
                else:play(page(selection))
            except:
                try:
                    if episode == episodes:print(fore.RED + "This episode is coming soon!")
                except:print(Fore.RED + "Invalid choice entered")


def cdnurl(link,info):
    req = requests.get(link).text
    soup = BS(req,"html.parser")
    link = json.loads(soup.select('#__NEXT_DATA__')[0].text)['props']['pageProps']['videoUrl']
    return (link,info)


def play(info):
    #print(info)
    #req = requests.get(info[0]).text
    #soup = BS(req,"html.parser")
    #try:link = json.loads(soup.select('#__NEXT_DATA__')[0].text)['props']['pageProps']['videoUrl']
    try:link,info = cdnurl(info[0], info[1])
    except Exception as e:return print(Fore.RED + e)
    #except:link = json.loads(soup.select('#__NEXT_DATA__')[0].text)['props']['pageProps']['videoUrl']
    try:
        try:os.system(f'mpv --referrer="https://theflix.to" "{link}" --force-media-title="mov-cli:{info}"')
        except:os.system(f'vlc --http-referrer="https://theflix.to" "{link}"')# --meta-title="{info}"
    except:print(Fore.RED + "Please install either mpv or vlc!")

data(input(Fore.BLUE + "[!] Please Enter the name of the Movie: "))
