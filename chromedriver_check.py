# coding=utf-8
"""
@Project: myWorkspace
@File: /chromedriver_check.py
@Author: Dustin Lin
@Created on: 2023/5/15 14:55:21
"""
import os
import winreg
import zipfile
import requests
from io import BytesIO
from bs4 import BeautifulSoup
from selenium import webdriver


def get_current_chromedriver_vers() -> str:
    # print(chromedriver_autoinstaller.install())
    browser = webdriver.Chrome()
    chromedriver_vers = browser.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
    browser.quit()
    main_vers = chromedriver_vers.split(".")[0]
    print(f"Current chromedriver version: {main_vers}")
    return main_vers


def get_chrome_vers() -> str:
    chrome_vers: str = ""
    platform: str = os.name
    if platform == "nt":

        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
        value, _ = winreg.QueryValueEx(key, 'version')
        chrome_vers: str = value.split(".")[0]
    print(f"Current chrome version: {chrome_vers}")
    return chrome_vers


def find_match_chromedriver_vers(vers: str):
    url = 'https://chromedriver.chromium.org/downloads'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    versions = soup.find_all('a', class_='XqQF9c', limit=3, href=True)
    for item in versions:
        version = item.getText().split(" ")[1]
        item_vers = version.split(".")[0]
        if vers == item_vers:
            print(f"vers: {vers} || match_vers: {item_vers} || {item['href']}")
            # return item["href"]
            return version


def download_chromedriver(version: str):
    url = f'https://chromedriver.storage.googleapis.com/{version}/chromedriver_win32.zip'
    response = requests.get(url, stream=True)
    print(response.content)
    zipf = zipfile.ZipFile(BytesIO(response.content))
    zipf.extractall()


if __name__ == '__main__':
    current_chromedriver_version: str = get_current_chromedriver_vers()
    current_chrome_version: str = get_chrome_vers()
    if current_chromedriver_version != current_chrome_version:
        online_version: str = find_match_chromedriver_vers(current_chrome_version)
        download_chromedriver(online_version)
        print("Done")
    else:
        print("Version match, no need to upgrade")
