import requests
from lxml import html
from bs4 import BeautifulSoup
from html_table_extractor.extractor import Extractor
payload = {
	"form_username": "b----------", 
	"form_password": "-----------", 
}
session_requests = requests.session()
login_url = "https://std.regis.ku.ac.th/_Login.php"
result = session_requests.get(login_url)

tree = html.fromstring(result.text)

result = session_requests.post(
	login_url, 
	data = payload, 
	headers = dict(referer=login_url)
)

url = 'https://std.regis.ku.ac.th/_Student_RptKu.php?mode=KU20'
result = session_requests.get(
	url, 
	headers = dict(referer = url)
)

#tree = html.tostring(result.content)
#print(result.content)

cleantext = BeautifulSoup(result.text, "lxml")
rows = []
for tr in cleantext.find_all('table'):
    cols = []
    for td in tr.find_all(['td','FONT']):
        td_text = td.get_text(strip=True)
        if len(td_text):
            cols.append(td_text)
    rows.append(cols)

#print (cleantext)

extractor = Extractor(cleantext)
extractor.parse()
#print(extractor.return_list())
ans =[]
for i in extractor.return_list():
    t =[]
    for j in i:
        if j ==  "<class \'str\'>":
            continue
        print(type(j))
        j.strip()
        j.strip('\xa0')
        t.append(j)
    ans.append(t)

print(ans)
