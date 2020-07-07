import bs4
import requests
# from datetime import datetime
import datetime
import mysql.connector
import time


class YTrending:

    def setup_db(self):
        self.__mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="ytrending_db"
        )
        self.__mycursor = self.__mydb.cursor(dictionary=True)
        self.__table_name = "trending_videos"

    def init_data(self):
        if self.__mydb != None:
            if self.__res.status_code == 200:
                soup = bs4.BeautifulSoup(self.__res.text, 'html.parser')

                f = open('./testyoutube.html', 'w', encoding="utf-8")
                f.write(soup.prettify())
                f.close()
                return

                raw_data = soup.find_all('li', {'class': 'expanded-shelf-content-item-wrapper'})

                # debug purpose -> to check the first row of the html
                # print(raw_data[0].prettify())

                number = 1
                for raw_item in raw_data:
                    video_id = self.__video_id(raw_item)
                    title = self.__title(raw_item)
                    desc = self.__desc(raw_item)
                    channel = self.__channel(raw_item)
                    views = self.__views(raw_item)
                    uploaded = self.__uploaded(raw_item)
                    duration = self.__duration(raw_item)
                    image_url = self.__image_url(raw_item)
                    trending_date = self.__current_date()

                    check_query = "SELECT video_id FROM " + self.__table_name + " WHERE video_id = %s AND trending_date = %s"
                    check_values = (video_id, trending_date)
                    self.__mycursor.execute(check_query, check_values)

                    result = self.__mycursor.fetchall()

                    if not result:
                        columns = "(num_trending, title, description, channel, views, uploaded, duration, image_url, video_id, created_at, updated_at, trending_date)"
                        values = "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        insert_query = "INSERT INTO " + self.__table_name + " " + columns + " VALUES " + values

                        created_at = self.__current_timestamp()
                        updated_at = created_at

                        t_video_item = (number, title, desc, channel, views, uploaded, duration, image_url, video_id, created_at, updated_at, trending_date)

                        self.__mycursor.execute(insert_query, t_video_item)
                        self.__mydb.commit()
                    else:
                        updated_at = self.__current_timestamp()

                        update_query = "UPDATE " + self.__table_name + " SET "
                        update_query += "num_trending = %s, "
                        update_query += "title = %s, "
                        update_query += "description = %s, "
                        update_query += "channel = %s, "
                        update_query += "views = %s, "
                        update_query += "uploaded = %s, "
                        update_query += "duration = %s, "
                        update_query += "image_url = %s, "
                        update_query += "updated_at = %s "
                        update_query += "WHERE video_id = %s"
                        
                        t_video_item = (number, title, desc, channel, views, uploaded, duration, image_url, updated_at, video_id)

                        self.__mycursor.execute(update_query, t_video_item)
                        self.__mydb.commit()

                    number += 1

                if not raw_data:
                    print(len(raw_data))
                    # print("something error occured.")
            else:
                print("Error fetching data")
        else:
            print('You need to setup database first.')

    def __init__(self):
        self.__mydb = None
        self.__res = requests.get('https://www.youtube.com/feed/trending')

        time.sleep(5)

        print(self.__res.text)
        return

    # def number_of_video(self):
    #     return self.__number_of_video

    def get_all(self):
        if self.__mydb != None:
            current_date = self.__current_date()

            get_all_query = "SELECT * FROM " + self.__table_name + " WHERE trending_date = %s"
            get_all_values = (current_date, )
            
            self.__mycursor.execute(get_all_query, get_all_values)
            all_data = self.__mycursor.fetchall()

            return list(all_data)
        else:
            return 'You need to setup database first.'

    def get_trending(self, limit, start):
        if self.__mydb != None:
            today_trending_query = ""

            current_date = self.__current_date()

            if limit != 0:
                today_trending_query = "SELECT num_trending, title, channel, views, uploaded, duration, trending_date FROM " + self.__table_name + " WHERE trending_date = %s ORDER BY num_trending LIMIT %s,%s"
                today_trending_values = (current_date, start, limit)
            else:
                today_trending_query = "SELECT num_trending, title, channel, views, uploaded, duration, trending_date FROM " + self.__table_name + " WHERE trending_date = %s ORDER BY num_trending"
                today_trending_values = (current_date, )
            
            self.__mycursor.execute(today_trending_query, today_trending_values)
            trending_videos = self.__mycursor.fetchall()

            return list(trending_videos)
        else:
            return 'You need to setup database first.'

    def get_video(self, number):
        if self.__mydb != None:
            current_date = self.__current_date()
            
            get_video_query = "SELECT * FROM " + self.__table_name + " WHERE num_trending = %s AND trending_date = %s"
            get_video_values = (number, current_date)

            self.__mycursor.execute(get_video_query, get_video_values)
            video = self.__mycursor.fetchone()

            if video:
                return video
            else:
                return None
        else:
            return 'You need to setup database first.'

    def find_video_by_channel(self, channel):
        if self.__mydb != None:
            current_date = self.__current_date

            find_video_by_channel_query = "SELECT * FROM "+ self.__table_name + " WHERE channel LIKE %" + channel + "% AND trending_date = " + current_date
            self.__mycursor.execute(find_video_by_channel_query)

            video = self.__mycursor.fetchone()

            if video:
                return video
            else:
                return None

    def find_video_by_title(self, title):
        if self.__mydb != None:
            current_date = self.__current_date

            find_video_by_title_query = "SELECT * FROM " + self.__table_name + " WHERE title LIKE %" + title + "% AND trending_date = " + current_date
            self.__mycursor.execute(find_video_by_title_query)

            video = self.__mycursor.fetchone()

            if video:
                return video
            else:
                return None

    # private method start here
    def __title(self, row):
        return row.find('h3', {'class': 'yt-lockup-title'}).find('a').get('title').strip()

    def __desc(self, row):
        desc = row.find('div', {'class': 'yt-lockup-description'})
        if desc != None:
            return desc.getText().strip()
        else:
            return ''

    def __channel(self, row):
        return row.find('div', {'class': 'yt-lockup-byline'}).find('a').getText().strip()

    def __views(self, row):
        strViews = row.find('ul', {'class': 'yt-lockup-meta-info'}).find_all('li')[1].getText().replace('x ditonton', '').replace('.', '')
        return int(strViews)

    def __uploaded(self, row):
        uploaded = row.find('ul', {'class': 'yt-lockup-meta-info'}).find_all('li')[0].getText().strip()
        return uploaded

    def __duration(self, row):
        return row.find('span', {'class': 'accessible-description'}).getText().replace('- Durasi: ', '')[:-1].replace('.', ':').strip()

    def __image_url(self, row):
        return row.find('img').get('src').strip()

    def __video_id(self, row):
        video_path_uri = row.find('a', {'class': 'yt-uix-sessionlink'}).get('href')
        return video_path_uri.split('v=')[1].strip()

    def __current_timestamp(self):
        now = datetime.datetime.now()
        f = '%Y-%m-%d %H:%M:%S'
        return now.strftime(f)

    def __current_date(self):
        now = datetime.datetime.now()
        f = '%Y-%m-%d'
        return now.strftime(f)