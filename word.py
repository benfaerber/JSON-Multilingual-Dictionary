import json
from pprint import pprint

with open("data/data.json") as file:    
	data = json.load(file)

def Translate(w, l):
	try:
		for item in data[w]:
			got = (item[l])
		return got
	except:
		return "ERROR"

langs = ["Spanish", "French", "Italian", "German", "Russian"]

print("Translate into Spanish, French, Italian, German, Russian or all")
word = input("To translate: ")
lang = input("To langauge: ")

word = word.lower()
lang = lang.lower()

if (lang == "all"):
	for l in langs:
		print(l + ": " + Translate(word, l.lower()))
else:
	print(Translate(word, lang))
