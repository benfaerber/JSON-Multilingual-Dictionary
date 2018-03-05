#!/usr/bin/env python
import urllib.request, re, requests

langs = ["spanish", "french", "italian", "german", "russian"]
base = "http://www.langtolang.com/?txtLang="
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
error = "No translation found."

count = 0
start = 4372
end = 71799

starting = 0

def FindBetween(s, first, last):
	try:
		start = s.index(first) + len(first)

		end = s.index(last, start)
		starting = start
		return s[start:end]
	except ValueError:
		return ""

def ExtractWord(s, word):
	a = FindBetween(str(s), "<table class=\"table table-striped\">", "</table>")
	b = FindBetween(a, "<tbody>", "</tbody>")

	b = b.replace(" ", "_")

	under = "__"
	for x in range(0, 10):
		b = b.replace(under, "")
		under += "_"

	b = b.replace("\n", "")
	b = b.replace("\t", "")
	b = b.replace("<tr>", "")
	b = b.replace("</tr>", "")
	b = b.replace("<td_width=\"40%\"_style=\"padding:_2px;\">", "")
	b = b.replace(word + "</td>", "")
	b = b.replace("</td>", ",")
	b = b.replace("_", " ")
	b = b[:-1]
	return b

data = open("data/data.json", "a")

with open("data/common.txt") as f:
	for line in f:
		if (count >= start and count <= end):
			line = line.replace("\n", "")
			print("Translating: " + line + " @ " + str(count))
			buf = '"' + line + '":[{'
			tran = 0
			for l in langs:
				url = base + line + "&submitButton=Search&selectFrom=english&selectTo=" + l
				response = requests.get(url, headers=headers)
				html = str(response.content, 'utf-8')
				if (error in html):
					tran += 1
					buf += '"' + l + '":"",'
				else:
					word = ExtractWord(html, line)
					word = word.replace("\"", "")
					if ("translation unavailable" in word):
						buf += '"' + l + '":"",'
					else:
						buf += '"' + l + '":"' + word + '",'
			buf += "}],"
			buf = buf.replace(",}", "}")
			if (tran != 5):
				data.write(buf + "\n")
			else:
				print("Cannot translate: " + line)
		count += 1

print(count)