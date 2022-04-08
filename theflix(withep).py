import requests, json, os, re
from bs4 import BeautifulSoup as BS
from colorama import Fore, Style
from sys import stdout as st

###Text###
blue = lambda a: f"{Fore.BLUE}{a}{Style.RESET_ALL}"
yellow = lambda a: f"{Fore.YELLOW}{a}{Style.RESET_ALL}"
red = lambda a: f"{Fore.RED}{a}{Style.RESET_ALL}"
lmagenta = lambda a: f"{Fore.LIGHTMAGENTA_EX}{a}{Style.RESET_ALL}"
cyan = lambda a: f"{Fore.CYAN}{a}{Style.RESET_ALL}"
green = lambda a: f"{Fore.GREEN}{a}{Style.RESET_ALL}"

def parse(q):
    l = ""
    for i in q[1:]:
        if i.isupper():l += f" {i}"
        else:l += i
    return re.sub("\W+", "-", f"{q[0]}{l}".lower())

def tok():return requests.post("https://theflix.to:5679/authorization/session/continue?contentUsageType=Viewing",data={"affiliateCode": "","pathname": "/"}).headers['Set-Cookie']

def query():
    q = input(blue("[!] Please Enter the name of the Movie: "))
    data = []
    for i in [[parse(i['name']),i['id'],i['available'],i['numberOfSeasons'],"WS"] for i in json.loads(BS(requests.get(f"https://theflix.to/tv-shows/trending?search={q}").text,"html.parser").select('#__NEXT_DATA__')[0].text)['props']['pageProps']['mainList']['docs'] if i['available']]:data.append(i)
    for i in [[parse(i['name']),i['id'],i['available'],"MOVIE"] for i in json.loads(BS(requests.get(f"https://theflix.to/movies/trending?search={q.replace(' ','+')}").text,"html.parser").select('#__NEXT_DATA__')[0].text)['props']['pageProps']['mainList']['docs'] if i['available']]:data.append(i)
    if not len(data):return print(red("No Results found"),lmagenta("Bye!"))
    else:return data

def data(q,ws=True,m=True,v=False):return display(query())

def ask(ts,id,name,tok):
    season = input(lmagenta(f"Please input the season number(total seasons:{ts}): "))
    episodes = json.loads(BS(requests.get(f"https://theflix.to/tv-show/{id}-{name}/season-{season}/episode-1",headers={'cookie':tok}).text,"html.parser").select('#__NEXT_DATA__')[0].text)['props']['pageProps']['selectedTv']['numberOfEpisodes']
    episode = input(lmagenta( f"Please input the episode number(total episodes in {season}:{episodes // int(ts)}: "))
    return (season,episodes,episode)

def redo():display(query())

def page(info):return (f'https://theflix.to/movie/{info[1]}-{info[0]}',info[0])

def wspage(info):return (f'https://theflix.to/tv-show/{info[1]}-{info[0]}/season-{info[-2]}/episode-{info[-1]}',f"{info[0]}_S_{info[-2]}_EP_{info[-1]}")

def cdnurl(link,info,k):
    f = json.loads(BS(requests.get(link,headers={'cookie':k}).text,"html.parser").select('#__NEXT_DATA__')[0].text)['props']['pageProps']['video']['id']
    link = requests.get(f"https://theflix.to:5679/movies/videos/{f}/request-access?contentUsageType=Viewing",headers={'cookie':k}).json()['url']
    #thanks to CADES & CoolnsX (https://github.com/alpha-hexor,https://github.com/CoolnsX)
    return (link,info)

def cdnurlep(link,info,k): 
    f = json.loads(BS(requests.get(link,headers={'cookie':k}).text,"html.parser").select('#__NEXT_DATA__')[0].text)['props']['pageProps']['video']['id']
    link = requests.get(f"https://theflix.to:5679/tv/videos/{f}/request-access?contentUsageType=Viewing",headers={'cookie':k}).json()['url']
    #thanks to CADES & CoolnsX (https://github.com/alpha-hexor,https://github.com/CoolnsX)
    return (link,info)

def dl(url,name):
    os.system(f'ffmpeg -loglevel error -stats -i "{url}" -c copy "{name}.mp4"')
    return print(blue(f"Downloaded {name}"))

def play(info,morep):
    token = tok()
    if morep == "MOVIE":link,info = cdnurl(info[0], info[1],token)
    else:link,info = cdnurlep(info[0], info[1],token)
    try:
        try:os.system(f'mpv --referrer="https://theflix.to" "{link}" --force-media-title="mov-cli:{info}"')
        except:os.system(f'vlc --http-referrer="https://theflix.to" "{link}" --meta-title="{info}"')
    except:print(Fore.RED + "Please install either mpv or vlc!")

def display(wm):
    for ix,vl in enumerate(wm):print(green(f"[{ix+1}] {vl[0]} {vl[-1]}", end="\n\n"))
    print(red("[q] Exit!"), end="\n\n")
    print(yellow("[s] Search Again!"), end="\n\n")
    print(cyan("[d] Download!"), end="\n\n")
    choice = ""
    while choice not in range(len(wm)+1):
        choice = input(blue( "Enter choice: "))
        if choice == "q":return print(lmagenta("Bye!"))
        elif choice == "s":return data(query())
        elif choice == 'd':
            try:
                mov = int(input(yellow("[!] Please enter the number of the movie you want to download: ")))-1
                chn = wm[mov]
                name = chn[0]
                if chn[-1] == "WS":
                    season = ""
                    while season not in range(chn[-2]+1):
                        token = tok()
                        season,episodes,episode = ask(chn[-2],chn[1],name,tok)
                        dl(cdnurlep(wspage([name,chn[1],season,episode]), name,token)[0],f"{name}_S_{season}_EP_{episode}/{episodes}")
                else:dl(cdnurl(page(chn)[0],chn[0])[0],name,token)
            except:
                if len(wm) < mov:print(red("Invalid Choice entered" ))
                else:print(red("Invalid choice entered"))
        else:
            try:
                selection = wm[int(choice)-1]
                if selection[-1] == "WS":
                    season,episodes,episode = ask(selection[-2],selection[1],selection[0])
                    selection.append(season)
                    selection.append(episode)
                    play(wspage(selection),"WS")
                else:play(page(selection),'MOVIE')
            except:print(red("This episode is coming soon! or unable to play"))

data(query())
