import bs4
import requests
# from datetime import datetime
import datetime


class YTrending:

    def __init__(self):
        self.__data = []
        
        res = requests.get('https://www.youtube.com/feed/trending')

        if res.status_code == 200:
            soup = bs4.BeautifulSoup(res.text, 'html.parser')

            raw_data = soup.find_all('li', {'class': 'expanded-shelf-content-item-wrapper'})

            # debug purpose -> to check the first row of the html
            # print(raw_data[0].prettify())

            number = 0
            for raw_item in raw_data:
                item = {
                    'id': number,
                    'title': self.__title(raw_item),
                    'desc': self.__desc(raw_item),
                    'channel': self.__channel(raw_item),
                    'views': self.__views(raw_item),
                    'uploaded': self.__uploaded(raw_item),
                    'duration': self.__duration(raw_item),
                    'image_url': self.__image_url(raw_item),
                    'watch_url': self.__watch_url(raw_item),
                }
                self.__data.append(item)
                number += 1

            self.__number_of_video = number + 1

            if not raw_data:
                print("something error occured.")
        else:
            print("someting error occured.")

    def number_of_video(self):
        return self.__number_of_video

    def get_all(self, limit=None):
        if limit != None:
            newList = []

            for index, item in enumerate(self.__data):
                if index == limit:
                    break
                
                newList.append(item)
            
            return newList
        
        else:
            return self.__data

    def get_video(self, id):
        return self.__data[id-1]

    def get_watch_url(self, id):
        return self.__data[id-1]['watch_url']

    def get_video_by_channel_name(self, channel):
        for item in self.__data:
            if channel.lower() == item['channel'].lower():
                return item

        return None

    def get_video_by_title(self, title):
        print('test')

    # private method start here
    def __title(self, row):
        return row.find('h3', {'class': 'yt-lockup-title'}).find('a').get('title')

    def __desc(self, row):
        desc = row.find('div', {'class': 'yt-lockup-description'})
        if desc != None:
            return desc.getText()
        else:
            return ''

    def __channel(self, row):
        return row.find('div', {'class': 'yt-lockup-byline'}).find('a').getText()

    def __views(self, row):
        strViews = row.find('ul', {'class': 'yt-lockup-meta-info'}).find_all('li')[1].getText().replace('x ditonton', '').replace('.', '')
        return int(strViews)
        # return row.find('ul', {'class': 'yt-lockup-meta-info'}).find_all('li')[1].getText().replace('x ditonton', '')

    def __uploaded(self, row):
        uploaded = row.find('ul', {'class': 'yt-lockup-meta-info'}).find_all('li')[0].getText()
        # now = datetime.datetime.now()

        # number = 0

        # for char in uploaded:
        #     if char.isdigit():
        #         number = int(char)

        # if 'minggu' in uploaded:
        #     days = 7 * number
        #     result = now - datetime.timedelta(days=days)
        # elif 'hari' in uploaded:
        #     result = now - datetime.timedelta(days=number)
        # elif 'jam' in uploaded:
        #     result = now - datetime.timedelta(hours=number)
        return uploaded

    def __duration(self, row):
        return row.find('span', {'class': 'accessible-description'}).getText().replace('- Durasi: ', '')[:-1].replace('.', ':')

    def __image_url(self, row):
        return row.find('img').get('src')

    def __watch_url(self, row):
        video_path_uri = row.find('a', {'class': 'yt-uix-sessionlink'}).get('href')
        return 'https://www.youtube.com' + video_path_uri