import requests
import math



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
while math.ceil(items/10) > index and cont:


    req = requests.get("https://www.googleapis.com/books/v1/volumes?q={search_term}&maxResults=10&startIndex={index}&projection=lite&langRestrict=en&key={key}".format(index=index,search_term=plus.join(key.split(' ')),key=api_key))
    req = requests.get("https://www.googleapis.com/books/v1/volumes?q={search_term}&maxResults=10&startIndex={index}&projection=lite&langRestrict=en&key={key}".format(index=x*10,search_term=term,key=GOOGLE_API_KEY))
    
    #print(req)
    response = req.json()


    for i in response["items"]:
        """
        try:
            print(i["volumeInfo"]["title"],i["volumeInfo"]["authors"])
        except:
            print(i["volumeInfo"]["title"])        
        """
        print(i["volumeInfo"])
        print("\n\n")
    items = response["totalItems"]
    #print(items)
    index += 10
    #print(index)
    #cont = input("continue?(y)") == "y"
    for k in i["volumeInfo"]:
        print(k)
    print("\n\n")
    for k in i:
        print(k)
    break

#print(len(response["items"]))
