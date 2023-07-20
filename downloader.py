import os
import requests

def DownLoadFile(url, file_name="file.mkv"):
    if os.path.exists(f"./downloads/{file_name}"):
        os.remove(f"./downloads/{file_name}")

    chunk_size=1024*10
    r = requests.get(url, allow_redirects=True, stream=True, verify=False)
    downloaded_size = 0
    with open(f"./downloads/{file_name}", 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                fd.write(chunk)
                downloaded_size += chunk_size
                
    return f"./downloads/{file_name}"