import requests, json, os, re, sys
from bs4 import BeautifulSoup as BS
from colorama import Fore
a = "'"

def parse(q):return re.sub("\W+", "-", q.lower())

def query(q,morws):
    try:
        if morws == "ws":return [[parse(i['name']),i['id'],i['available'],i['numberOfSeasons'],"WS"] for i in json.loads(BS(requests.get(f"https://theflix.to/tv-shows/trending?search={q}").text,"html.parser").select('#__NEXT_DATA__')[0].text)['props']['pageProps']['mainList']['docs'] if i['available']]
        elif morws == "m":return [[parse(i['name']),i['id'],i['available'],"MOVIE"] for i in json.loads(BS(requests.get(f"https://theflix.to/movies/trending?search={q.replace(' ','+')}").text,"html.parser").select('#__NEXT_DATA__')[0].text)['props']['pageProps']['mainList']['docs'] if i['available']]
    except:return print(Fore.RESET + "No results found")

def data(q,ws=True,m=True,v=False):
    choices = []
    if ws and m:
        for i in query(q,'ws'):choices.append(i) 
        for i in query(q,'m'):choices.append(i)
    #elif m:
    #    for i in query(q,"m"):choices.append(i)
    #elif ws:
    #    for i in query(q,'ws'):choices.append(i)
    return display(choices)

def page(info):
    i = info[0]
    return (f'https://theflix.to/movie/{info[1]}-{i}',i)

def wspage(info):
    i = info[0]
    return (f'https://theflix.to/tv-show/{info[1]}-{i}/season-{info[-2]}/episode-{info[-1]}',i)


def display(info):
    if not len(info):return print("No result Found!")
    for idx,val in enumerate(info):print(Fore.GREEN + f"[{idx+1}] {val[0]} {val[-1]}", end="\n\n")
    print(Fore.RED + "[q] Exit!", end="\n\n")
    print(Fore.YELLOW + "[s] Search Again!", end="\n\n")
    print(Fore.CYAN + "[d] Download!", end="\n\n")
    choice = ""
    while choice not in range(len(info) + 1):
        choice = input(Fore.BLUE + "Enter choice: ")
        if choice == "q":return print(Fore.RESET + "Bye!")
        elif choice == "s":return data(input(Fore.BLUE + "[!] Please Enter the name of the Movie: "))
        elif choice == 'd':
            try:
                mov = int(input(Fore.YELLOW + "[!] Please enter the number of the movie you want to download: "))-1
                inf = info[mov]
                if inf[-1] == "WS":
                    season = ""
                    while season not in range(inf[-2]+1):
                        season = input(Fore.LIGHTMAGENTA_EX + f"Please input the season number(total seasons:{inf[-2]}): ")
                        i = inf[0]
                        episodes = json.loads(BS(requests.get(f"https://theflix.to/tv-show/{inf[1]}-{i}/season-{season}/episode-1").text,"html.parser").select('#__NEXT_DATA__')[0].text)['props']['pageProps']['selectedTv']['seasons'][0]['numberOfEpisodes']
                        episode = input(Fore.LIGHTMAGENTA_EX + f"Please input the episode number(total episodes in {season}:{episodes}): ")
                        with open(f'{inf[0]}.mp4','wb') as f:
                            url = cdnurl(wspage([i,inf[1],season,episode])[0],i)
                            req = requests.get(url,stream=True)
                            dl = 0
                            tl = int(req.headers.get('content-length'))
                            for j in req.iter_content(chunk_size=1024):
                                if i:
                                    dl += len(j)
                                    f.write(j)
                                    done = int(50 * dl / tl)
                                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                                    sys.stdout.flush()
                            sys.stdout.write('\n')
                            return print(Fore.LIGHTYELLOW_EX + f"Downloaded {i}")
                else:
                    with open(f'{inf[0]}.mp4','wb') as f:
                        url = cdnurl(page(inf)[0],inf[0])[0]
                        req = requests.get(url,stream=True)
                        dl = 0
                        tl = int(req.headers.get('content-length'))
                        if not tl:f.write(req.content)
                        for j in req.iter_content(chunk_size=1024):
                            if j:
                                dl += len(j)
                                f.write(j)
                                done = int(50 * dl / tl)
                                sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
                                sys.stdout.flush()
                        sys.stdout.write('\n')
                        return print(Fore.LIGHTYELLOW_EX + f"Downloaded {i}")
            except:
                if len(info) < mov:print(Fore.RED + "Invalid Choice entered" )
                else:print(Fore.LIGHTRED_EX + 'Unable to Download')
        else:
            try:
                selection = info[int(choice)-1]
                #print(selection)
                if selection[-1] == "WS":
                    season = input(Fore.LIGHTMAGENTA_EX + f"Please input the season number(total seasons:{selection[-2]}): ")
                    episodes = json.loads(BS(requests.get(f"https://theflix.to/tv-show/{selection[1]}-{selection[0]}/season-{season}/episode-1").text,"html.parser").select('#__NEXT_DATA__')[0].text)['props']['pageProps']['selectedTv']['seasons'][0]['numberOfEpisodes']
                    episode = input(Fore.LIGHTMAGENTA_EX + f"Please input the episode number(total episodes in {season}:{episodes}): ")
                    selection.append(season)
                    selection.append(episode)
                    play(wspage(selection))
                else:play(page(selection))
            except:
                try:
                    if episode == episodes:print(fore.RED + "This episode is coming soon!")
                except:print(Fore.RED + "Invalid choice entered")


def cdnurl(link,info):return (json.loads(BS(requests.get(link).text,"html.parser").select('#__NEXT_DATA__')[0].text)['props']['pageProps']['videoUrl'],info)


def play(info):
    try:link,info = cdnurl(info[0], info[1])
    except Exception as e:return print(e)
    try:
        try:os.system(f'mpv --referrer="https://theflix.to" "{link}" --force-media-title="mov-cli:{info}"')
        except:os.system(f'vlc --http-referrer="https://theflix.to" "{link}"')# --meta-title="{info}"
    except:print(Fore.RED + "Please install either mpv or vlc!")

data(input(Fore.BLUE + "[!] Please Enter the name of the Movie: "))
