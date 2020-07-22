import requests
import datetime



api_key = "AIzaSyDGkEHbMHzjlk4PsJ0ud_1S7ZfyPHI0btg"
#Venv\Scripts\activate
#req = requests.get("https://www.googleapis.com/books/v1/volumes?q=Harry+potter")

key = "john green"
#s = s.split(' ')
plus = "+"



req = requests.get("https://www.googleapis.com/books/v1/volumes?q={search_term}&projection=lite&key={key}".format(search_term = plus.join(key.split(' ')), key=api_key))

print(req)
response = req.json()


for i in response["items"]:
    try:
        print(i["volumeInfo"]["title"],i["volumeInfo"]["authors"])
    except:
        print(i["volumeInfo"]["title"])        

#print(response)
#print(len(response["items"]))
"""


statement = "INSERT INTO public.users (id, pass, full_name, screen_name, email,created_at) VALUES ({id},crypt('{pw}', gen_salt('bf')),'{full_name}','{screen_name}','{email}','{date}');"
today = datetime.date.today()
statement = statement.format(id=30,pw=45,full_name="atakan",screen_name="atakan",email="a@a",date=str(today))
print(statement)

"""