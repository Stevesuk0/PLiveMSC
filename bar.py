import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
}

def get(url, path, desc):
    response = requests.get(url, stream=True, headers=headers)
    filesize = int(int(response.headers["Content-Length"]) / 1024)
    now_mb = 0
    now_percent = 0
    with open(path, "wb") as f:
        for i in response.iter_content(1024):
            f.write(i)
            print(f"\r{desc}: {'='*int(now_percent / 5) + ' '*int(20-int(now_percent/5))} {now_percent}% {int(now_mb / 1000)} MB / {int(filesize / 1000)} MB", end="")
            now_mb += 1
            now_percent = int((now_mb / filesize) * 100)
            
        print()

def ins(url, path):
    response = requests.get(url, stream=True, headers=headers)
    with open(path, "wb") as f:
        for i in response.iter_content(1024):
            f.write(i)