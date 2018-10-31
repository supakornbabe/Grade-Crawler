import requests
import time
import os
from lxml import html
from bs4 import BeautifulSoup
from html_table_extractor.extractor import Extractor
from line_notify import LineNotify
import getpass
KU_id = 'tmp'
KU_pass = 'tmp'
Line_token = ''

def main():
    payload = {
        "form_username": KU_id,
        "form_password": KU_pass,
    }
    session_requests = requests.session()
    login_url = "https://stdregis.ku.ac.th/_Login.php"
    result = session_requests.get(login_url)
    result = session_requests.post(
        login_url, data=payload, headers=dict(referer=login_url))
    url = 'https://stdregis.ku.ac.th/_Student_RptKu.php?mode=KU20'
    result = session_requests.get(url, headers=dict(referer=url))
    soup = BeautifulSoup(result.text, 'html.parser')
    soup_table = BeautifulSoup(
        str(soup.find_all("table", class_="table")), 'lxml')
    tag = soup_table.table
    notify = LineNotify(Line_token)
    tag = tag.text
    tag = tag.split("Second Semester 2017")[1]
    tag = tag.replace("CodeCourse", "")
    tag = tag.replace("Course", "")
    tag = tag.replace("TitleGradeCredit", "")
    tag = tag.replace("01", "\n01")
    tag = tag.replace("sem. G.P.A.", "\nsem. G.P.A.")
    tag = tag.replace("cum. G.P.A.", "\ncum. G.P.A.")
    check = False
    for t in tag.split("\n"):
        check = False
        revt = ''.join(reversed(t))
        o = 0
        for i in revt:
            if o == 1:
                if i == 'N':
                    check = True
                break
            o += 1
        if check:
            continue

        if str(t)[0] == '0':
            print(t)
            notify.send(t)
            print()

if __name__ == '__main__':
    KU_id = input("KU_id: ")
    KU_pass = getpass.getpass("KU_pass: ")
    while (True):
        main()
        time.sleep(60)
