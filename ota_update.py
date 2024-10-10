import json
import machine
import ubinascii
from pathlib import Path
from time import sleep as zzz

version_file = 'versions.txt'
token = '?token=GHSAT0AAAAAACYYMDYGQZ6JA34AMNB5WFAEZYIDYQQ'
repo_url = f'https://raw.githubusercontent.com/Selebs/tjawe.cameras/refs/heads/main/'
version_url = f'{repo_url}/{version_file}{token}'

if version_file in os.listdir():
    with open(version_file) as f:
        current_versions = json.load(f)
else:
    current_versions = {}
    with open(version_file, 'w') as f:
        json.dump(version_file, f)

print('Current versions (on Pico W) ', current_versions)

response = urequests.get(version_url)

if response.status_code == 200:
    latest_version = {}
    test2 = response.text.split(',')
    for x in test2:
        x = x.replace(' ', '')
        y = x.split(':')
        latest_version[y[0]] = int(y[1])
elif response.status_code == 404:
    print(f'directory or version file not found on repo')
    latest_version = {}

response.close()