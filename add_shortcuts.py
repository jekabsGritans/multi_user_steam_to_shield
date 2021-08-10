from os import listdir, getlogin, mkdir, getcwd,chdir
from sys import path as syspath
from subprocess import call
from os.path import isdir as dir_exists
from shutil import move
from getpass import getpass
##############################################################################################
#run setup.py if error
##############################################################################################
from re import search, findall
from PIL import Image,ImageDraw,ImageFont
from win32com.client import Dispatch

##############################################################################################
chdir(syspath[0])
cwd = getcwd()

##############################################################################################
##############################################################################################

steam_dir = "C:\\Program Files (x86)\\Steam\\"
shield_app_dir = f"C:\\Users\\{getlogin()}\\AppData\\local\\NVIDIA Corporation\\Shield Apps\\"
##############################################################################################
##############################################################################################
boxart_dir = f"{steam_dir}appcache\\librarycache\\"
script_steam_dir = steam_dir.replace('\\','\\\\')
class Game:
    def __init__(self,username,password,gameid,title):
        forbidden = [':','/','\\','*','?','<','>','|']
        for char in forbidden:
            title = title.replace(char,'')
        self.title = title
        self.username = username
        self.password = password
        self.gameid = gameid
        self.boxart_path = f"{boxart_dir}{self.gameid}_library_600x900.jpg"


    def create_bat(self):
        script = r"""
from subprocess import call, check_output
from time import time
from threading import Thread

call("taskkill /F /IM steam.exe")

Thread(target=call,args="""+f"""['"{script_steam_dir}steam.exe" -login {self.username} {self.password}"""+r"""'], kwargs={"shell":True}).start()
start = time()
while time()-start<20:
    if 'steam.exe' in check_output("wmic process get description").decode('utf-8'):
        game = Thread(target=call,args=['"""+f'"C:\\\\Program Files (x86)\\\\Steam\\\\steam.exe" -applaunch {self.gameid}'+r"""'], kwargs={"shell":True})
        game.start()
        break
"""

        if not dir_exists('games'):
            mkdir('games')

        pywpath = f'games\\{self.title} ({self.username}).pyw'
        print(pywpath)
        with open(pywpath,'w') as f:
            f.write(script)


    def add_to_shield(self):
        #add boxart(needed)
        p = f"{shield_app_dir}StreamingAssets\\{self.title} ({self.username})\\"
        mkdir(p)
        try:
            img = Image.open(self.boxart_path)
        except:
            img = Image.open("lib\\defbox.jpg")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("lib\\NotoSans-Regular.ttf", 50)
        draw.text((0,img.height-75), self.username,(255,255,255),font=font)
        img.save(f'{p}box-art.png')

        #Create shortcut
        path = shield_app_dir+f'{self.title} ({self.username}).lnk'
        target = f"{cwd}\\games\\{self.title} ({self.username}).pyw"
        wDir = f"{cwd}\\games"

        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = wDir
        shortcut.save()

def read(path):
    with open(path,'r',encoding='Latin-1') as f:
        return f.read()

users ={}

for user_id in listdir(f'{steam_dir}userdata\\'):
    user_info = read(f'{steam_dir}userdata\\{user_id}\\config\\localconfig.vdf')
    owned_app_ids = [item for item in findall('(\d*)"\n.*\n.*"LastPlayed',user_info)]
    personaname = search('"PersonaName".*"(.*)"',user_info).group(1)
    users[user_id] = {}
    users[user_id]['PersonaName'] = personaname
    login_users = read(f"{steam_dir}config\\loginusers.vdf")
    ress = findall('"AccountName".*"(.*)".*\n.*"PersonaName".*"(.*)"',login_users)
    for res in ress:
        accname, personaname_r = res
        if personaname_r == personaname:
            users[user_id]['username'] = accname

    users[user_id]['apps'] = owned_app_ids

    users[user_id]['password']=getpass(f'Enter password for {users[user_id]["username"]}: ')





dir = listdir(f"{steam_dir}steamapps\\")
acfs = [file for file in dir if file.endswith("acf")]
games=[]

for acf in acfs:
    manifest = read(f"{steam_dir}steamapps\\{acf}")
    appid = search('"appid"	*"(\d*)"',manifest).group(1)
    name = search('"name"	*"(.*)"',manifest).group(1)
    for user in users:
        user = users[user]
        if appid in user['apps']:
            games.append(Game(user['username'], user['password'], appid, name))

for game in games:
    game.create_bat()
    game.add_to_shield()