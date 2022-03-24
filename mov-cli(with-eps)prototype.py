import requests, json, os, re
from bs4 import BeautifulSoup as BS
from colorama import Fore
from sys import stdout as st

def parse(q):return re.sub("\W+", "-", q.lower())

def query(q):
    data = []
    for i in [[parse(i['name']),i['id'],i['available'],i['numberOfSeasons'],"WS"] for i in json.loads(BS(requests.get(f"https://theflix.to/tv-shows/trending?search={q}").text,"html.parser").select('#__NEXT_DATA__')[0].text)['props']['pageProps']['mainList']['docs'] if i['available']]:data.append(i)
    for i in [[parse(i['name']),i['id'],i['available'],"MOVIE"] for i in json.loads(BS(requests.get(f"https://theflix.to/movies/trending?search={q.replace(' ','+')}").text,"html.parser").select('#__NEXT_DATA__')[0].text)['props']['pageProps']['mainList']['docs'] if i['available']]:data.append(i)
    if not len(data):
        print(Fore.RED + "No Results found")
        return print(Fore.RESET + "Bye!")
    else:return data

def data(q,ws=True,m=True,v=False):return display(query(q))

#def ask(ts):

def page(info):
    i = info[0]
    return (f'https://theflix.to/movie/{info[1]}-{i}',i)

def wspage(info):
    i = info[0]
    return (f'https://theflix.to/tv-show/{info[1]}-{i}/season-{info[-2]}/episode-{info[-1]}',f"{i}_S_{info[-2]}_EP_{info[-1]}")

def cdnurl(link,info):return (json.loads(BS(requests.get(link).text,"html.parser").select('#__NEXT_DATA__')[0].text)['props']['pageProps']['videoUrl'],info)

def dl(url,name):
    try:
        req = requests.get(url,stream=True)
        tl,dl = int(req.headers.get('content-length')),0
        with open(f"{name}.mp4","wb") as f:
            for i in req.iter_content(chunk_size=1024):
                if i:
                    dl+=len(i)
                    f.write(i)
                    done = int(50 * dl / tl)
                    st.write("\r[%s%s]" % ('▋' * done, ' ' * (50-done)) )    
                    st.flush()
                st.write('\n')
                return print(Fore.RESET + f"Downloaded {name}")
    except:return print(Fore.RESET + 'Unable to Download')

def play(info):
    link,info = cdnurl(info[0], info[1])
    try:
        try:os.system(f'mpv --referrer="https://theflix.to" "{link}" --force-media-title="mov-cli:{info}"')
        except:os.system(f'vlc --http-referrer="https://theflix.to" "{link}" --meta-title="{info}"')
    except:print(Fore.RED + "Please install either mpv or vlc!")

def display(wm):
    for ix,vl in enumerate(wm):print(Fore.GREEN + f"[{ix+1}] {vl[0]} {vl[-1]}", end="\n\n")
    print(Fore.RED + "[q] Exit!", end="\n\n")
    print(Fore.YELLOW + "[s] Search Again!", end="\n\n")
    print(Fore.CYAN + "[d] Download!", end="\n\n")
    choice = ""
    while choice not in range(len(wm)+1):
        choice = input(Fore.BLUE + "Enter choice: ")
        if choice == "q":return print(Fore.RESET + "Bye!")
        elif choice == "s":return data(input(Fore.BLUE + "[!] Please Enter the name of the Movie: "))
        elif choice == 'd':
            try:
                mov = int(input(Fore.YELLOW + "[!] Please enter the number of the movie you want to download: "))-1
                chn = wm[mov]
                name = chn[0]
                if chn[-1] == "WS":
                    season = ""
                    while season not in range(chn[-2]+1):
                        season = input(Fore.LIGHTMAGENTA_EX + f"Please input the season number(total seasons:{chn[-2]}): ")
                        episodes = json.loads(BS(requests.get(f"https://theflix.to/tv-show/{chn[1]}-{i}/season-{season}/episode-1").text,"html.parser").select('#__NEXT_DATA__')[0].text)['props']['pageProps']['selectedTv']['seasons'][0]['numberOfEpisodes']
                        episode = input(Fore.LIGHTMAGENTA_EX + f"Please input the episode number(total episodes in {season}:{episodes}): ")
                        dl(cdnurl(wspage([name,chn[1],season,episode]), name)[0],f"{name}_S_{season}_EP_{episode}")
                else:dl(cdnurl(page(chn)[0],chn[0])[0],name)
            except:
                if len(wm) < mov:print(Fore.RED + "Invalid Choice entered" )
                else:print(Fore.RED + "Invalid choice entered")
        else:
            selection = wm[int(choice)-1]
            try:
                if selection[-1] == "WS":
                    season = input(Fore.LIGHTMAGENTA_EX + f"Please input the season number(total seasons:{selection[-2]}): ")
                    episodes = json.loads(BS(requests.get(f"https://theflix.to/tv-show/{selection[1]}-{selection[0]}/season-{season}/episode-1").text,"html.parser").select('#__NEXT_DATA__')[0].text)['props']['pageProps']['selectedTv']['seasons'][0]['numberOfEpisodes']
                    episode = input(Fore.LIGHTMAGENTA_EX + f"Please input the episode number(total episodes in {season}:{episodes}): ")
                    selection.append(season)
                    selection.append(episode)
                    play(wspage(selection))
                else:play(page(selection))
            except:
                print(Fore.RED + "This episode is coming soon! or unable to play")

data(input(Fore.BLUE + "[!] Please Enter the name of the Movie: "))
