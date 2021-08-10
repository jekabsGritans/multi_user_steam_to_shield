from json import loads
from requests import post
from os.path import isfile as exists
def get_access_token(secret,id):
    r = post(f"https://id.twitch.tv/oauth2/token?client_id={id}&client_secret={secret}&grant_type=client_credentials")
    j = loads(r.text)
    token = j['access_token']
    with open('token','w') as f:
        f.write(token)
    return token

if exists('id'):
    with open('id','r') as f:
        id = f.read()
else:
    print("Find out more about getting the ID and Secret - https://api-docs.igdb.com/#about")
    id = input("Enter your twitch app id: ")
    with open('id','w') as f:
        f.write(id)

if exists('secret'):
    with open('secret','r') as f:
        secret = f.read()
else:
    print("Find out more about getting the ID and Secret - https://api-docs.igdb.com/#about")
    secret = input("Enter your twitch app secret: ")
    with open('secret','w') as f:
        f.write(secret)

if exists('token'):
    with open('token','r') as f:
        token = f.read()
else:
    token = get_access_token(secret,id)

titles = ['csgo','Battlefield V']

HEADERS = {"Client-ID":id,"Authorization":f"Bearer {token}"}
