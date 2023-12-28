import requests
from bs4 import BeautifulSoup
import json
import time

url = 'https://mbasic.facebook.com/'  
cookies_file = 'cookie.json'


with open(cookies_file, 'r') as f:
    cookies = requests.utils.cookiejar_from_dict(json.load(f))

response = requests.get(url, cookies=cookies)


if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')


    like_links = set()

    for link in soup.find_all('a', href=True):
        if '/a/like.php' in link['href']:
            like_links.add(url + link['href'])  

    print(f"Jumlah Link Post : {len(like_links)}")


    jumlah_like_ulang = int(input("Masukkan jumlah like yang akan diulang: "))

    for _ in range(jumlah_like_ulang):
        print(f"\nMencoba melakukan aksi like ke-{_ + 1}:")
        

        for link in like_links:
            time.sleep(2.5) 
            response = requests.get(link, cookies=cookies)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                if "Error Facebook" in soup.title.text: 
                    print(f"Gagal melakukan like pada post {link}. Terjadi error.")
                else:
                    print(f"Berhasil melakukan like pada post")
            else:
                print(f"Gagal melakukan like pada {link}")

        response = requests.get(url, cookies=cookies)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            like_links = set()
            for link in soup.find_all('a', href=True):
                if '/a/like.php' in link['href']:
                    like_links.add(url + link['href'])  
        else:
            print(f"Gagal memperbarui halaman. Kode status: {response.status_code}")

else:
    print(f"Gagal mengakses halaman. Kode status: {response.status_code}")
