import requests
from Button import Button

newButton = Button(400, 300, 10, 10, "hello", "Comic Sans MS", 50)

r = requests.get('https://traktrain.com/')

print(help(r))