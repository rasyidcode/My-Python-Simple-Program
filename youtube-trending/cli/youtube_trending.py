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
import converter as Converter

yt = YoutubeTrending()
yt.setup_db()
yt.init_data()

os.system('color')

@click.group()
def main():
    """
    simple program to check youtube current trending
    """

@main.command(help='Print out the current trending on youtube in table format.')
@click.option('--limit', '-l', default=0, help='Limit the trending video shows in the table.', type=int)
@click.option('--start', '-s', default=0, help='Starts trending.', type=int)
def trending(limit, start):
    result = yt.get_trending(limit=limit, start=start)

    if isinstance(result, str):
        print('Something wrong occured. Please check core library')
        print('Error : ' + result)
    else:
        table = prettytable.PrettyTable(['Trending', 'Title', 'Channel', 'Views', 'Uploaded', 'Duration'])

        for video in result:
            row = [
                '#' + str(video['num_trending']),
                video['title'],
                video['channel'],
                Helper.to_juta_format(video['views']),
                Helper.to_local_format(video['uploaded']),
                video['duration']
            ]
            table.add_row(row)
        
        f = '%Y-%m-%d'
        current_date = result[0]['trending_date'].strftime(f)
        total_row = len(result)

        click.echo(table)

        cprint('Date generated : ', 'cyan', end=current_date)
        print('')
        cprint('Total row : ', 'cyan', end=str(total_row))


@main.command(help='Show individual youtube trending by it\'s number.')
@click.option('--number', '-n', default=0, help='Number of the trending video.', type=int)
def detail(number):
    if number > 0:
        video = yt.get_video(number)

        if video != None:
            Helper.print_detail(video)
        else:
            click.echo('invalid trending number, try again.')
    else:
        click.echo('invalid number, try again.')



@main.command(help='Watch the trending video by it\'s number.')
@click.option('--number', '-n', default=0, help='Number of the trending video.', type=int)
def watch(number):
    if number > 0:
        video = yt.get_video(number)
        
        if video != None:
            watch_url = 'https://www.youtube.com/watch?v=' + video['video_id']
            webbrowser.open(watch_url)
        else:
            click.echo('invalid trending number, try again.')
    else:
        click.echo('invalid number, try again.')


@main.command(help='Find what\'s trending.')
@click.option('--channel', '-c', help='Channel name to find.', type=str)
def find(channel):
    result = yt.find_video_by_channel(channel)

    if result != None:
        Helper.print_detail(result)
    else:
        cprint(channel, 'red', end=' currently is not in trending list right now.')

@main.command(help='Generate trending list to JSON, CSV, XLS, XLSX, HTML, XML or YAML.')
@click.option('--ext', '-ex', help='File type.', type=str)
def generate(ext):
    data = yt.get_all()

    switcher = {
        'json': Converter.to_json,
        'csv': Converter.to_csv,
        'xls': Converter.to_xls,
        'xlsx': Converter.to_xlsx,
        'html': Converter.to_html,
        'xml': Converter.to_xml,
        'yaml': Converter.to_yaml,
    }

    generator = switcher.get(ext, lambda : print('invalid'))
    
    if not os.path.exists('./cli/files'):
        os.mkdir('./cli/files')
    
    generator(data)
    
if __name__ == "__main__":
    main()
