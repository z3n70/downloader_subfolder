import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_file(url, dest_folder):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        file_name = os.path.basename(url)
        file_path = os.path.join(dest_folder, file_name)
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded: {file_path}")
    else:
        print(f"Failed to download: {url}")

def download_directory(dir_url, dest_folder):
    response = requests.get(dir_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href == '../' or href == './' or href.endswith('/'):
                continue
            file_url = urljoin(dir_url, href)
            download_file(file_url, dest_folder)
    else:
        print(f"Failed to fetch directory: {dir_url}")

def main(base_url, dest_folder):
    response = requests.get(base_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href.endswith('/'):
                dir_url = urljoin(base_url, href)
                subdir_name = href.rstrip('/')
                subdir_dest = os.path.join(dest_folder, subdir_name)
                os.makedirs(subdir_dest, exist_ok=True)
                download_directory(dir_url, subdir_dest)
    else:
        print(f"Failed to fetch base URL: {base_url}")

if __name__ == "__main__":
    base_url = "http://example.com/berkas/"
    dest_folder = "downloaded_files"
    os.makedirs(dest_folder, exist_ok=True)
    main(base_url, dest_folder)

