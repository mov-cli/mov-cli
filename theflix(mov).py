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

def tok():
    r = requests.post("https://theflix.to:5679/authorization/session/continue?contentUsageType=Viewing",data={
    "affiliateCode": "",
    "pathname": "/"
    })
    return r.headers['Set-Cookie']

def query(q):
    data = []
    for i in [[parse(i['name']),i['id'],i['available'],"MOVIE"] for i in json.loads(BS(requests.get(f"https://theflix.to/movies/trending?search={q.replace(' ','+')}").text,"html.parser").select('#__NEXT_DATA__')[0].text)['props']['pageProps']['mainList']['docs'] if i['available']]:data.append(i)
    if not len(data):
        print(red("No Results found"))
        return print(lmagenta("Bye!"))
    else:return data

def data(q,ws=True,m=True,v=False):return display(query(q))

def ask(ts,id,name):
    season = input(lmagenta(f"Please input the season number(total seasons:{ts}): "))
    episodes = json.loads(BS(requests.get(f"https://theflix.to/tv-show/{id}-{name}/season-{season}/episode-1").text,"html.parser").select('#__NEXT_DATA__')[0].text)['props']['pageProps']['selectedTv']['seasons'][0]['numberOfEpisodes']
    episode = input(lmagenta( f"Please input the episode number(total episodes in {season}:{episodes}): "))
    return (season,episodes,episode)

def page(info):
    i = info[0]
    return (f'https://theflix.to/movie/{info[1]}-{i}',i)

def wspage(info):
    i = info[0]
    return (f'https://theflix.to/tv-show/{info[1]}-{i}/season-{info[-2]}/episode-{info[-1]}',f"{i}_S_{info[-2]}_EP_{info[-1]}")

def cdnurl(link,info,k): 
    f = json.loads(BS(requests.get(link,headers={'cookie':k}).text,"html.parser").select('#__NEXT_DATA__')[0].text)['props']['pageProps']['video']['id']
    link = requests.get(f"https://theflix.to:5679/movies/videos/{f}/request-access?contentUsageType=Viewing",headers={'cookie':k}).json()['url']
    #thanks to CADES & CoolnsX (https://github.com/alpha-hexor,https://github.com/CoolnsX)
    return (link,info)

def dl(url,name):
    try:
        req = requests.get(url,stream=True)
        tl,dl = int(req.headers.get('content-length')),0
        with open(f"{name}.mp4","wb") as f:
            for i in req.iter_content(chunk_size=1024):
                if i:
                    dl+=len(i)
                    f.write(i)
                    done = int(50 * dl/tl)
                    st.write("\r[%s%s]" % ('█'*done, ' '*(50-done)) )    
                    st.flush()
        st.write('\n')
        return print(green(f"Downloaded {name}"))
    except Exception as e:return print(red(f'Unable to Download: {e}'))

def play(info):
    link,info = cdnurl(info[0], info[1],tok())
    try:
        try:os.system(f'mpv --referrer="https://theflix.to" "{link}" --force-media-title="mov-cli:{info}"')
        except:os.system(f'vlc --http-referrer="https://theflix.to" "{link}" --meta-title="{info}"')
    except:print(Fore.RED + "Please install either mpv or vlc!")

def display(wm):
    for ix,vl in enumerate(wm):print(Fore.GREEN + f"[{ix+1}] {vl[0]} {vl[-1]}", end="\n\n")
    print(red("[q] Exit!"), end="\n\n")
    print(yellow("[s] Search Again!"), end="\n\n")
    print(cyan("[d] Download!"), end="\n\n")
    choice = ""
    while choice not in range(len(wm)+1):
        choice = input(blue( "Enter choice: "))
        if choice == "q":return print(lmagenta("Bye!"))
        elif choice == "s":return data(input(blue("[!] Please Enter the name of the Movie: ")))
        elif choice == 'd':
            try:
                mov = int(input(yellow("[!] Please enter the number of the movie you want to download: ")))-1
                chn = wm[mov]
                name = chn[0]
                if chn[-1] == "WS":
                    season = ""
                    while season not in range(chn[-2]+1):
                        season,episodes,episode = ask(chn[-2],chn[1],name)
                        dl(cdnurl(wspage([name,chn[1],season,episode]), name,tok())[0],f"{name}_S_{season}_EP_{episode}")
                else:dl(cdnurl(page(chn)[0],chn[0])[0],name,tok())
            except Exception as e:
                print(e)
                if len(wm) < mov:print(red("Invalid Choice entered" ))
                else:print(red("Invalid choice entered"))
        else:
            try:
                selection = wm[int(choice)-1]
                if selection[-1] == "WS":
                    season,episodes,episode = ask(selection[-2],selection[1],selection[0])
                    selection.append(season)
                    selection.append(episode)
                    play(wspage(selection))
                else:play(page(selection))
            except:print(Fore.RED + "This episode is coming soon! or unable to play")

data(input(blue("[!] Please Enter the name of the Movie: ")))
