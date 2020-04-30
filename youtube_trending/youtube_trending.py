import os

import bs4
import prettytable
import requests
import click
import webbrowser
from termcolor import cprint


class YoutubeTrending:

    def __init__(self):
        os.system('color')

        res = requests.get('https://www.youtube.com/feed/trending')

        if res.status_code == 200:
            soup = bs4.BeautifulSoup(res.text, 'html.parser')

            self.lis = soup.find_all('li', {'class': 'expanded-shelf-content-item-wrapper'})

            if not self.lis:
                print("something error occured")
            else:
                my_table = ['Trending', 'Title', 'Channel', 'Views', 'Uploaded', 'Duration']
                self.pt = prettytable.PrettyTable(my_table)
                no = 1

                for li in self.lis:
                    data = [
                        '#' + str(no),
                        self.__title(li),
                        self.__channel(li),
                        self.__views(li),
                        self.__uploaded(li),
                        self.__duration(li),
                    ]
                    self.pt.add_row(data)
                    no += 1
        else:
            print("someting error occured.")

    def first_row(self):
        print(self.lis[0].prettify())

    def generate_table(self):
        click.echo(self.pt)

    def trending_detail(self, num):
        try:
            row = self.lis[num - 1]

            cprint('Trending        :   ', 'yellow', end='#' + str(num))
            print('')
            cprint('Title           :   ', 'yellow', end=self.__title(row))
            print('')
            cprint('Desc            :   ', 'yellow', end=self.__desc(row))
            print('')
            cprint('Channel         :   ', 'yellow', end=self.__channel(row))
            print('')
            cprint('Views           :   ', 'yellow', end=self.__views(row))
            print('')
            cprint('Uploaded        :   ', 'yellow', end=self.__uploaded(row))
            print('')
            cprint('Duration        :   ', 'yellow', end=self.__duration(row))
            print('')
            cprint('Image URL       :   ', 'yellow', end=self.__imageUrl(row))
            print('')
            cprint('Watch URL       :   ', 'yellow', end=self.__watchUrl(row))
            print('')

        except:
            print('Error : 404 Not found')

    def watch_trending(self, number):
        try:
            row = self.lis[number - 1]
            webbrowser.open(self.__watchUrl(row))
        except:
            print('Error : 404 Not found')

    def __title(self, row):
        return row.find('h3', {'class': 'yt-lockup-title'}).find('a').get('title')

    def __desc(self, row):
        return row.find('div', {'class': 'yt-lockup-description'}).getText()

    def __channel(self, row):
        return row.find('div', {'class': 'yt-lockup-byline'}).find('a').getText()

    def __views(self, row):
        return row.find('ul', {'class': 'yt-lockup-meta-info'}).find_all('li')[1].getText().replace('x ditonton', '')

    def __uploaded(self, row):
        return row.find('ul', {'class': 'yt-lockup-meta-info'}).find_all('li')[0].getText()

    def __duration(self, row):
        return row.find('span', {'class': 'accessible-description'}).getText().replace('- Durasi: ', '')[:-1].replace(
            '.', ':')

    def __imageUrl(self, row):
        return row.find('img').get('src')

    def __watchUrl(self, row):
        return 'https://www.youtube.com' + row.find('a', {'class': 'yt-uix-sessionlink'}).get('href')


yt = YoutubeTrending()


@click.group()
def main():
    """
    simple program to check youtube current trending
    """
    pass


@main.command(help='Print out the current trending on youtube in table format.')
def trending():
    yt.generate_table()


@main.command(help='Show individual youtube trending by it\'s number.')
@click.option('--number', '-n', help='Number of the trending video.', type=int)
def detail(number):
    yt.trending_detail(number)


@main.command(help='Watch the trending video by it\'s number.')
@click.option('--number', '-n', help='Number of the trending video.', type=int)
def watch(number):
    yt.watch_trending(number)


# @click.command()
# @click.argument('name')
# @click.option('--greeting', '-g')
# def main(name, greeting):
#     click.echo("{}, {}".format(greeting, name))

if __name__ == "__main__":
    main()
