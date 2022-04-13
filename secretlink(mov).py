from bs4 import BeautifulSoup as BS
import json, os, requests, re
from colorama import Fore, Style

###Text###
blue = lambda a: f"{Fore.BLUE}{a}{Style.RESET_ALL}"
yellow = lambda a: f"{Fore.YELLOW}{a}{Style.RESET_ALL}"
red = lambda a: f"{Fore.RED}{a}{Style.RESET_ALL}"
lmagenta = lambda a: f"{Fore.LIGHTMAGENTA_EX}{a}{Style.RESET_ALL}"
cyan = lambda a: f"{Fore.CYAN}{a}{Style.RESET_ALL}"
green = lambda a: f"{Fore.GREEN}{a}{Style.RESET_ALL}"

###Small_Functions###
def parse(q):return q.replace(" ","%20")

###Declarations###
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"

def search():
    q = parse(input(blue("Enter the name of the movie:")))
    return requests.get(f"https://secretlink.xyz/search/keyword/{q}").text

def results(res:requests.Response):    
    soup = BS(res,'html.parser')
    titles = [ i.text for i in soup.select(".panel-body")[0].select("h5")]
    urls = [x['href'] for i in soup.select(".panel-body")[0].select("h5") for x in i.select("a")]
    return [list(sublist) for sublist in zip(urls,titles)]

def validate(u1,u2):
    r1=requests.head(u1)
    #r2 = requests.head(u2)
    
    if r1.status_code == 200:
        return u1
    else:
        return u2 #hoping the other one will work automatically
     
    

def get_link(url,id,token1,token2):
    #construct the proper post request
    post_url = "https://secretlink.xyz/home/index/GetMInfoAjax"
    headers = { 
               'User-Agent': useragent, 
               
               'X-Requested-With': 'XMLHttpRequest', 
               
               'Referer': url} 
               
    
    data1 = {'pass':id,"param" : token1}
    data2 = {'pass':id,"param" : token2}
    
    r1=json.loads(requests.post(post_url,headers=headers,data=data1).json())["val"]
    r2 = json.loads(requests.post(post_url,headers=headers,data=data2).json())["val"]
    
    return validate(r1,r2)
    
    
    
def play(link,sub_url):
    os.system(f'mpv --sub-file="{sub_url}" --referrer="https://secretlink.xyz" "{link}"')

###Main###
def dl(url,sub_url,name):
    r=requests.get(sub_url)
    with open("english.srt",'wb') as f:
        f.write(r.content)
    f.close()
    print(blue(f"Subtitle downloaded"))
    
    os.system(f'ffmpeg -loglevel error -stats -i "{url}" -c copy "{name}.mp4"')
    return print(blue(f"Downloaded {name}"))

def redo():display(search())

def display(wm):
    #print(wm)
    for ix,vl in enumerate(wm):print(Fore.GREEN + f"[{ix+1}] {vl[1]}", end="\n\n")
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
            slection = wm[mov]
            link = slection[0]
            r=requests.get("https://secretlink.xyz"+link)
            id =  re.findall(r'id="hId" value="(.*?)"',r.text)[0]
            token1 = BS(r.text,'html.parser').select("#divU")[0].text
            token2 = BS(r.text,'html.parser').select("#divP")[0].text
            subtitle_url = f"https://secretlink.xyz/subtitle/movie/{id}/English.srt"
            dl(get_link("https://secretlink.xyz"+link,id,token1,token2),subtitle_url,slection[1])
            
        else:
            selection = wm[int(choice)-1]
            link = selection[0]
            r=requests.get("https://secretlink.xyz"+link)
            id =  re.findall(r'id="hId" value="(.*?)"',r.text)[0]
            token1 = BS(r.text,'html.parser').select("#divU")[0].text
            token2 = BS(r.text,'html.parser').select("#divP")[0].text
            subtitle_url = f"https://secretlink.xyz/subtitle/movie/{id}/English.srt" 
            play(get_link("https://secretlink.xyz"+link,id,token1,token2),subtitle_url)
            

display(results(search()))
