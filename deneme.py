import requests
import math
import unicodedata



api_key = "AIzaSyDGkEHbMHzjlk4PsJ0ud_1S7ZfyPHI0btg"
#Venv\Scripts\activate
#req = requests.get("https://www.googleapis.com/books/v1/volumes?q=Harry+potter")

#key = input("Search term?")
key = "harry potter rowling"
#s = s.split(' ')
plus = "+"

index = 0
items = 10
cont = True

req = requests.get("https://www.googleapis.com/books/v1/volumes/{volumeId}".format(volumeId = "5v1NBhR1W88C"))

response = req.json()

info = {}
vi = response["volumeInfo"]
plus = "+"

try:
    info["title"] = vi["title"] + "--" + vi["subtitle"]
except:
    info["title"] = vi["title"]

try:
    info["authors"] = plus.join(vi["authors"])
except:
    info["authors"] = None

try:
    info["publisher"] = vi["publisher"]
except:
    info["publisher"] = None

try:
    info["publishedDate"] = vi["publishedDate"]
except:
    info["publishedDate"] = None

try:
    new_str = unicodedata.normalize("NFKD", vi["description"])
    info["description "] = new_str
except:
    info["description "] = None

try:
    all_categories = vi["categories"]
except:
    all_categories = None
unique_categories = []
for i in all_categories:
    sub = i.split('/')
    for k in sub:
        if k not in unique_categories:
            unique_categories.append(k)

info["categories"] = unique_categories

try:
    image = vi["imageLinks"]["smallThumbnail"]
except:
    try:
        image = vi["imageLinks"]["thumbnail"]
    except:
        try:
            image = vi["imageLinks"]["small"]
        except:
            try:
                image = vi["imageLinks"]["medium"]
            except:
                try:
                    image = vi["imageLinks"]["large"]
                except:
                    image = None

info["imagelink"] = image
print(info)