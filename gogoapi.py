import requests
from bs4 import BeautifulSoup


class Gogo:
    def __init__(self, gogoanime_token: str, auth_token: str, host: str):
        self.gogoanime_token = gogoanime_token
        self.auth_token = auth_token
        self.host = host

    def get_bookmarks(self):
        url = f"https://www.{self.host}/user/bookmark"
        cookies = {"gogoanime": self.gogoanime_token, "auth": self.auth_token}
        response = requests.get(url=url, cookies=cookies)
        soup = BeautifulSoup(response.text, "lxml")
        anime = soup.find_all("div", {"class":"column_left_1"})
        anime = anime[1:]
        result = []
        for i in anime:
            anime_name = i.find("a").text.strip()
            ep_num = int(i.find("p").text.strip().split()[-1])
            link = i.find("p").find("a")["href"]
            result.append(
                {
                    "Anime": anime_name, 
                    "Episode": ep_num,
                    "Link": link
                }
            )
        return result

    def get_download_link(self, animeid, episode_num):
        url = f'https://{self.host}/{animeid}-episode-{episode_num}'
        cookies = {
            'gogoanime': self.gogoanime_token,
            'auth': self.auth_token
        }
        response = requests.get(url=url, cookies=cookies)
        plaintext = response.text
        soup = BeautifulSoup(plaintext, "lxml")
        download_div = soup.find("div", {'class': 'cf-download'}).findAll('a')
        result = {}
        
        url = f'https://{self.host}/category/{animeid}'
        response = requests.get(url=url, cookies=cookies)
        plaintext = response.text
        soup = BeautifulSoup(plaintext, "lxml")
        img = soup.find("div", {'class':'anime_info_body_bg'}).find('img')['src']
        result["thumb"] = img        
        for links in download_div:
            download_link = links['href']
            quality_name = links.text.strip().split('x')[1]
            result[quality_name] = download_link
        return result