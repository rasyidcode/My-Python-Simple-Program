import os

import prettytable
import click
import webbrowser
from termcolor import cprint
import sys

core_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '\\core\\'
sys.path.append(core_path)

from ytrending import YTrending as YoutubeTrending
import helper as Helper

yt = YoutubeTrending()

os.system('color')


@click.group()
def main():
    """
    simple program to check youtube current trending
    """
    pass


@main.command(help='Print out the current trending on youtube in table format.')
@click.option('--limit', '-l', default=0, help='Limit the trending video shows in the table.', type=int)
def trending(limit):
    listVideo = yt.get_all(limit=limit)

    table = prettytable.PrettyTable(['Trending', 'Title', 'Channel', 'Views', 'Uploaded', 'Duration'])

    for video in listVideo:
        row = [
            '#' + str(video['id'] + 1),
            video['title'],
            video['channel'],
            video['views'],
            video['uploaded'],
            video['duration']
        ]
        table.add_row(row)
    
    click.echo(table)


@main.command(help='Show individual youtube trending by it\'s number.')
@click.option('--number', '-n', help='Number of the trending video.', type=int)
def detail(number):
    if number > 0:
        video = yt.get_video(number)
        Helper.print_detail(video)
    else:
        click.echo('invalid number, try again.')



@main.command(help='Watch the trending video by it\'s number.')
@click.option('--number', '-n', help='Number of the trending video.', type=int)
def watch(number):
    if number > 0:
        watch_url = yt.get_watch_url(number)
        webbrowser.open(watch_url)
    else:
        click.echo('invalid number, try again.')


@main.command(help='Find what\'s trending.')
@click.option('--channel', '-c', help='Channel name to find.', type=str)
def find(channel):
    result = yt.get_video_by_channel_name(channel)

    if result != None:
        Helper.print_detail(result)
    else:
        cprint(channel, 'red', end=' currently is not in trending list right now.')
    
if __name__ == "__main__":
    main()
