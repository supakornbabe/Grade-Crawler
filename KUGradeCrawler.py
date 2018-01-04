import requests
import imgkit
import time
import os
from lxml import html
from bs4 import BeautifulSoup
from html_table_extractor.extractor import Extractor
from line_notify import LineNotify

Line_token = ''
KU_id = ''
KU_pass = ''

def main():
    payload = {
        "form_username": KU_id,
        "form_password": KU_pass,
    }
    session_requests = requests.session()
    login_url = "https://std.regis.ku.ac.th/_Login.php"
    result = session_requests.get(login_url)
    result = session_requests.post(
        login_url, data=payload, headers=dict(referer=login_url))
    url = 'https://std.regis.ku.ac.th/_Student_RptKu.php?mode=KU20'
    result = session_requests.get(url, headers=dict(referer=url))
    soup = BeautifulSoup(result.text, 'html.parser')
    soup_table = BeautifulSoup(
        str(soup.find_all("table", class_="table")), 'lxml')
    tag = soup_table.table
    imgkit.from_string(str(tag), 'GRADEKUout.jpg')
    notify = LineNotify(Line_token)
    notify.send("Grade", image_path='./GRADEKUout.jpg')
    os.remove("GRADEKUout.jpg")

if __name__ == '__main__':
    while (True):
        main()
        time.sleep(60)