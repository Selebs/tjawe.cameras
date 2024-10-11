import os
import json
import urequests
from pathlib import Path
from machine import reset
from time import sleep as zzz
from secrets import GITHUB_URL

def check_and_run_updates():
    repo_url = GITHUB_URL
    version_file = 'versions.txt'
    version_url = f'{repo_url}{version_file}'

    if version_file in os.listdir():
        with open(version_file) as f:
            current_versions = json.load(f)
    else:
        current_versions = {}
        with open(version_file, 'w') as f:
            json.dump(current_versions, f)

    print('Current versions (on Pico W) ', current_versions)

    print(f'GET HTTP:\n{version_url}')
    response = urequests.get(version_url)

    if response.status_code == 200:
        latest_versions = {}
        test2 = response.text.split(',')
        for x in test2:
            x = x.replace(' ', '')
            y = x.split(':')
            latest_versions[y[0]] = int(y[1])
    elif response.status_code == 404:
        print(f'directory or version file not found on repo')
        latest_versions = {}

    print(f'Version from GitHub:\n{str(latest_versions)}')
    response.close()


    something_done = False
    for filename in latest_versions:
        if filename not in current_versions or latest_versions.get(filename) != current_versions.get(filename):    
            file_url = repo_url + filename
            response = urequests.get(file_url)

            if response.status_code == 404:
                print(filename, ' not found on repo')
                response.close()
                continue
            
            split_pos = filename.rfind('/')
            if split_pos == -1:
                path = ''
                fn = filename
            else:
                path = filename[:split_pos]
                fn = filename[split_pos + 1]

            try:
                if fn in os.listdir(path):
                    if filename in current_versions:
                        if current_versions[filename] != latest_versions[filename]:
                            print(f'{filename} is up to date.')
                            continue
                        print(f'Updating {filename}...')
                else:
                    print(f'Adding {filename}...')
            except OSError:
                new_path = Path(path)
                new_path.mkdir(parents=True, exist_ok=True)
            finally:
                latest_code = response.text
                response.close()

                with open('latest_code.py', 'w') as f:
                    f.write(latest_code)
                os.rename('latest_code.py', filename)
                current_versions[filename] = latest_versions.get(filename)
                something_done = True

    if something_done:
        print('Update completed...')
        with open(version_file, 'w') as f:
            json.dump(latest_versions, f)

        print('Restarting device - Ignore error messages')
        zzz(.5)
        reset()
    else:
        print('No new updates available...')