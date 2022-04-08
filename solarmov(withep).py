'''
based on:-
https://github.com/alpha-hexor/solar-cli
https://github.com/mov-cli/mov-cli/blob/main/movcli(prototype_witheps).py
'''


from bs4 import BeautifulSoup as BS
from urllib import parse as p
import base64, json, os, requests, re
from colorama import Fore, Style

###Text###
blue = lambda a: f"{Fore.BLUE}{a}{Style.RESET_ALL}"
yellow = lambda a: f"{Fore.YELLOW}{a}{Style.RESET_ALL}"
red = lambda a: f"{Fore.RED}{a}{Style.RESET_ALL}"
lmagenta = lambda a: f"{Fore.LIGHTMAGENTA_EX}{a}{Style.RESET_ALL}"
cyan = lambda a: f"{Fore.CYAN}{a}{Style.RESET_ALL}"
green = lambda a: f"{Fore.GREEN}{a}{Style.RESET_ALL}"

###Small_Functions###
x = lambda d: base64.b64encode(d.encode()).decode().replace("\n", "").replace("=", ".")
def parse(q):return re.sub("\W+", "-", q.lower())

###Declarations###
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
k = '6LeWLCYeAAAAAL1caYzkrIY-M59Vu41vIblXQZ48'
domain = x('https://rabbitstream.net:443')
def search():
    q = parse(input(blue("Enter the name of the movie/show: ")))
    return requests.get(f"https://solarmovie.pe/search/{q}").text

def results(res:requests.Response):    
    soup = BS(res,'html.parser')
    urls = [i['href'] for i in soup.select('.film-poster-ahref')]#if i['href'].__contains__('/movie/')
    f = []
    for i in urls:
        if i.__contains__('/movie/'):f.append("MOVIE") 
        else:f.append("TV")
    title = [re.sub(pattern="/tv/|/movie/|hd|watch|[0-9]*",repl='',string=" ".join(i.split("-"))) for i in urls]#.replace("/movie/",'').replace('hd','').replace('watch',"")|re.sub(pattern="-",repl=" ",string=parse(
    ids = [i.split('-')[-1] for i in urls]
    return [list(sublist) for sublist in zip(f,urls,title,ids)]

def return_server(id):

    rem = requests.get(f"https://solarmovie.pe/ajax/movie/episodes/{id}").text
    soup = BS(rem,'html.parser')
    return [i['data-linkid'] for i in soup.select('.link-item')][0]

def return_server_tv(id):
    rem = requests.get(f"https://solarmovie.pe/ajax/v2/episode/servers/{id}/#servers-list").text
    soup = BS(rem,'html.parser')
    return [i['data-id'] for i in soup.select('.link-item')][0]


def rab_id(id):
    ram = requests.get(f"https://solarmovie.pe/ajax/get_link/{id}").json()['link']
    meid = p.urlparse(ram,allow_fragments=True,scheme='/')
    rabbid = re.sub(pattern='/embed-4/|/embed-5/',repl="",string=meid.path).replace("/embed-4/",'')
    return (ram,rabbid)

def key_num(ram):
    yae_miko = requests.get(ram,headers={'user-agent':useragent,'referer':'https://solarmovie.pe'}).text
    soup = BS(yae_miko,'html.parser')
    f = [i.text for i in soup.find_all("script")][-3].replace("var","")
    k = list(f)
    key = "".join(k[21:61])
    num = k[-3]
    return (key,num)

def gettoken(key):
    #*IMP: Thanks to CADES(https://github.com/alpha-hexor)
    r = requests.get("https://www.google.com/recaptcha/api.js?render="+key,headers={'referer':'https://solarmovie.pe','user-agent':useragent,'cacheTime':'0'})
    s = r.text.replace("/* PLEASE DO NOT COPY AND PASTE THIS CODE. */","")
    s = s.split(";")
    vtoken = s[10].replace("po.src=","").split("/")[-2]

    r = requests.get("https://www.google.com/recaptcha/api2/anchor?ar=1&hl=en&size=invisible&cb=xxmovclix&k="+key+"&co="+domain+"&v="+vtoken,headers={'user-agent':useragent})
    
    soup = BS(r.content, "html.parser")
    recap_token = [i['value'] for i in soup.select("#recaptcha-token")][0]
    
    data = {
        "v" : vtoken,
        "k" : k,
        "c" : recap_token,
        "co" : domain,
        "sa" : "",
        "reason" :"q"
    }
    return requests.post("https://www.google.com/recaptcha/api2/reload?k="+key,data=data,headers={'user-agent':useragent,'cacheTime':'0'}).text.replace(")]}'",'')

def m3u8(rabbid,rose,num):return requests.get(f"https://rabbitstream.net/ajax/embed-4/getSources?id={rabbid}&_token={rose}&_number={num}",headers={'user-agent':useragent,'X-Requested-With': 'XMLHttpRequest'}).json()

def play(obj,s):os.system(f'mpv --referrer="https://solarmovie.pe" {obj}' if s == None else f'mpv --sub-file="{s}" --referrer="https://solarmovie.pe" {obj}')
###Main###
def ask(id):
    r = requests.get(f"https://solarmovie.pe/ajax/v2/tv/seasons/{id}").text
    season_ids = [i['data-id'] for i in BS(r,'html.parser').select(".dropdown-item")]
    season = input(lmagenta(f"Please input the season number(total seasons:{len(season_ids)}): "))
    rf = requests.get(f"https://solarmovie.pe/ajax/v2/season/episodes/{season_ids[int(season)-1]}").text
    #print(f"https://solarmovie.pe/ajax/v2/season/episodes/{season_ids[int(season)-1]}")
    episodes = [i['data-id'] for i in BS(rf,'html.parser').select("a")]
    episode = episodes[int(input(lmagenta(f"Please input the episode number(total episodes in season:{season}):{len(episodes)} : ")))-1]
    return return_server_tv(episode)
    #return (season_ids,season,episodes,episode)
    
def ask_subtitle(languages,subtitles):
    if len(subtitles) == 0:
        return None
    else:
        print(lmagenta("[*]Availabe subtitles:"))
        for i in range(len(languages)):
            print(cyan(f"[{i+1}]{languages[i]}"))
        i = int(input(lmagenta("[*]Please input the subtitle number: ")))
        return subtitles[i-1]
        
def dl(url,name,s):
    if s != None:
        r=requests.get(s)
        with open({name}.srt,"wb") as f: f.write(r.content)
        f.close()
        print(blue(f"Downloaded {name}.srt"))
    os.system(f'ffmpeg -loglevel error -stats -i "{url}" -c copy "{name}.mp4"')
    print(blue(f"Downloaded {name}"))

def redo():display(results(search()))

def display(wm):
    for ix,vl in enumerate(wm):print(green(f"[{ix+1}] {vl[2]} {vl[0]}"), end="\n\n")
    print(red("[q] Exit!"), end="\n\n")
    print(yellow("[s] Search Again!"), end="\n\n")
    print(cyan("[d] Download!"), end="\n\n")
    choice = ""
    while choice not in range(len(wm)+1):
        choice = input(blue("Enter choice: "))
        if choice == "q":return print(lmagenta("Bye!"))
        elif choice == "s":return redo()
        elif choice == 'd':
            mov = int(input(yellow("[!] Please enter the number of the movie you want to download: ")))-1
            chn = wm[mov]
            if chn[0] == "TV":
                sid = ask(chn[-1])
                #print(chn[-1])
                iframe_url,mov_id = rab_id(sid)
                key,num = key_num(iframe_url)
                token = json.loads(gettoken(key))[1]
                x=m3u8(mov_id,token,num)
                languages = [x["tracks"][i]["label"] for i in range(len(x["tracks"]))]
                subtitles = [x["tracks"][i]["file"] for i in range(len(x["tracks"]))]
                s=ask_subtitle(languages,subtitles)
                dl(x["sources"][0]["file"],chn[1],s)
            else:
                sid = return_server(chn[-1])
                iframe_url,mov_id = rab_id(sid)
                key,num = key_num(iframe_url)
                token = json.loads(gettoken(key))[1]
                x=m3u8(mov_id,token,num)
                languages = [x["tracks"][i]["label"] for i in range(len(x["tracks"]))]
                subtitles = [x["tracks"][i]["file"] for i in range(len(x["tracks"]))]
                s=ask_subtitle(languages,subtitles)
                dl(x["sources"][0]["file"],chn[1],s)
        else:
            selection = wm[int(choice)-1]
            if selection[0] == "TV":
                sid = ask(selection[-1])
                iframe_url,mov_id = rab_id(sid)
                key,num = key_num(iframe_url)
                token = json.loads(gettoken(key))[1]
                x=m3u8(mov_id,token,num)
                languages = [x["tracks"][i]["label"] for i in range(len(x["tracks"]))]
                subtitles = [x["tracks"][i]["file"] for i in range(len(x["tracks"]))]
                s=ask_subtitle(languages,subtitles)
                play(x["sources"][0]["file"],s)
            else:
                sid = return_server(selection[-1])
                iframe_url,mov_id = rab_id(sid)
                key,num = key_num(iframe_url)
                token = json.loads(gettoken(key))[1]
                x=m3u8(mov_id,token,num)
                languages = [x["tracks"][i]["label"] for i in range(len(x["tracks"]))]
                subtitles = [x["tracks"][i]["file"] for i in range(len(x["tracks"]))]
                s=ask_subtitle(languages,subtitles)
                play(x["sources"][0]["file"],s)

display(results(search()))