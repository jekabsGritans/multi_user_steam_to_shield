from os import listdir, getlogin, mkdir, getcwd, chdir
from subprocess import call
from os.path import isdir as dir_exists
from shutil import move

##############################################################################################
#run setup.py if error
##############################################################################################
from re import search, findall
from PIL import Image,ImageDraw,ImageFont
import win32com.client
##############################################################################################


# from vdf import to_dict
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
        batpath = f'games\\{self.title} ({self.username}).bat'
        print(pywpath)
        print(batpath)
        with open(pywpath,'w') as f:
            f.write(script)

        with open(batpath,'w') as f:
            f.write(f'start "" "{self.title} ({self.username}).pyw" /popup \n exit')
        self.batpath = batpath

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
        #create a shortcut
        shell = win32com.client.Dispatch("WScript.shell")
        shortcut = shell.CrateShortCut(f"{shield_app_dir}{self.title} ({self.username}).lnk")
        shortcut.Targetpath = f'{cwd}\\games\\{self.title}.bat'
        shortcut.save()

def read(path):
    with open(path,'r',encoding='Latin-1') as f:
        return f.read()

users ={}

for user_id in listdir(f'{steam_dir}userdata\\'):
    # user_info = to_dict(read(f'{steam_dir}userdata\\{user_id}\\config\\localconfig.vdf'))
    user_info = read(f'{steam_dir}userdata\\{user_id}\\config\\localconfig.vdf')
    # owned_app_ids = [id for id in user_info["UserLocalConfigStore"]["Software"]["Valve"]["steam"]["Apps"]]
    owned_app_ids = [item for item in findall('(\d*)"\n.*\n.*"LastPlayed',user_info)]
    # personaname = user_info["UserLocalConfigStore"]["friends"]["PersonaName"]
    personaname = search('"PersonaName".*"(.*)"',user_info).group(1)
    users[user_id] = {}
    users[user_id]['PersonaName'] = personaname
    # login_users = to_dict(read("{steam_dir}config\\loginusers.vdf"))['users']
    login_users = read(f"{steam_dir}config\\loginusers.vdf")

    # for id in login_users:
    #     if login_users[id]['PersonaName'] == personaname:
    #         users[user_id]['username'] = login_users[id]['AccountName'] #DEPENDENT ON VDF read

    ress = findall('"AccountName".*"(.*)".*\n.*"PersonaName".*"(.*)"',login_users)
    for res in ress:
        accname, personaname_r = res
        if personaname_r == personaname:
            users[user_id]['username'] = accname

    users[user_id]['apps'] = owned_app_ids

    users[user_id]['password']=input(f'Enter password for {users[user_id]["username"]}: ')





dir = listdir(f"{steam_dir}steamapps\\")
acfs = [file for file in dir if file.endswith("acf")]
games=[]

for acf in acfs:
    # manifest = to_dict(read(f"{steam_dir}steamapps\\{acf}"))
    manifest = read(f"{steam_dir}steamapps\\{acf}")
    #appid = manifest['AppState']['appid']
    appid = search('"appid"	*"(\d*)"',manifest).group(1)
    # name = manifest['AppState']['name']
    name = search('"name"	*"(.*)"',manifest).group(1)
    for user in users:
        user = users[user]
        if appid in user['apps']:
            games.append(Game(user['username'], user['password'], appid, name))

for game in games:
    game.create_bat()
    game.add_to_shield()