import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

# Fungsi untuk mengunduh file
def download_file(url, dest_folder):
    try:
        response = requests.get(url, stream=True, timeout=10)  
        response.raise_for_status() 
        if response.status_code == 200:
            file_name = os.path.basename(url)
            file_path = os.path.join(dest_folder, file_name)
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"Downloaded: {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download: {url}. Error: {e}")

# Fungsi untuk mengunduh direktori
def download_directory(dir_url, dest_folder):
    try:
        response = requests.get(dir_url, timeout=10) 
        response.raise_for_status()
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                if href == '../' or href == './' or href.endswith('/'):
                    continue
                file_url = urljoin(dir_url, href)
                download_file(file_url, dest_folder)
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch directory: {dir_url}. Error: {e}")

def main(base_url, dest_folder):
    try:
        response = requests.get(base_url, timeout=10) 
        response.raise_for_status()
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
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch base URL: {base_url}. Error: {e}")

if __name__ == "__main__":
    base_url = "http://example.com/berkas/"
    dest_folder = "downloaded_files"
    os.makedirs(dest_folder, exist_ok=True)
    
    max_retries = 3
    retries = 0
    while retries < max_retries:
        try:
            main(base_url, dest_folder)
            break  
        except Exception as e:
            retries += 1
            print(f"Retrying ({retries}/{max_retries})...")
            time.sleep(5) 

