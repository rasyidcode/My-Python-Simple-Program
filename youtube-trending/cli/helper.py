from termcolor import cprint

def print_detail(video):
    cprint('Trending        :   ', 'yellow', end='#' + str(video['num_trending']))
    print('')
    cprint('Title           :   ', 'yellow', end=video['title'])
    print('')
    cprint('Desc            :   ', 'yellow', end=video['description'])
    print('')
    cprint('Channel         :   ', 'yellow', end=video['channel'])
    print('')
    cprint('Views           :   ', 'yellow', end=str(to_juta_format(video['views'])))
    print('')
    cprint('Uploaded        :   ', 'yellow', end=video['uploaded'])
    print('')
    cprint('Duration        :   ', 'yellow', end=video['duration'].strip())
    print('')
    cprint('Image URL       :   ', 'yellow', end=video['image_url'])
    print('')
    cprint('Watch URL       :   ', 'yellow', end='https://www.youtube.com/watch?v=' + video['video_id'])
    print('')

def to_local_format(timestamp):
    result = timestamp
    # result = _weekday_to_string(timestamp.weekday) + "," + timestamp.day + " " + timestamp.month + " " + timestamp.year + " " + timestamp.hour + ":" + timestamp.minute + ":" + timestamp.second
    return result

def _weekday_to_string(weekday):
    if weekday == 0:
        return 'Minggu'
    elif weekday == 1:
        return 'Senin'
    elif weekday == 2:
        return 'Selasa'
    elif weekday == 3:
        return 'Rabu'
    elif weekday == 4:
        return 'Kamis'
    elif weekday == 5:
        return 'Juma\'t'
    elif weekday == 6:
        return 'Sabtu'
    else:
        return None

def to_juta_format(views):
    result = 0
    total_digit = _count_digit(views)
    if total_digit <= 6:
        result = str(round(views / 1000, 2)) + ' k'
    else:
        result = str(round(views / 1000000, 2)) + ' jt'
        
    return result

def _count_digit(number):
    counter = 0

    while(number > 0):
        number = number // 10
        counter += 1

    return counter